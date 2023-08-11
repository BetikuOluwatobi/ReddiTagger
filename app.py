import os
import random
import requests
import dash
import spacy
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from flair.models import TextClassifier
from flair.data import Sentence
from flask import Flask, request, redirect, session, render_template
from flask_caching import Cache
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random key for session encryption
dash_app = dash.Dash(__name__, server=app, 
                    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                    external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname='/dashboard/')

dash_app.title = "ReddiTagger"

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

class SearchForm(FlaskForm):
    subreddit = StringField('Subreddit')
    entity = SelectField('Entity', choices=[
        ('ORG', 'ORG'),
        ('LOC', 'LOC'),
        ('EVENT', 'EVENT'),
        ('GPE', 'GPE'),
        ('WORK_OF_ART', 'WORK_OF_ART')
    ])
    submit = SubmitField('Submit')

nlp = spacy.load('en_core_web_trf')
# classifier = TextClassifier.load('en-sentiment')

entity = "ORG"
def extract_entity(text,entity=entity):
    """
    Splits text into overlapping segments of maximum length max_len using a stride.
    """
    max_len = 356  # BERT's maximum sequence length
    stride = 128
    tokens = text.split()  # naive tokenization
    results = set()

    if len(text.split()) <= 256:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == entity:
                results.add(ent.text)
    else:
        segments = []

        start = 0
        while start < len(tokens):
            end = start + max_len
            segments.append(" ".join(tokens[start:end]))
            start += stride

        for segment in segments:
            doc = nlp(segment)
            for ent in doc.ents:
                if ent.label_ == entity:
                    results.add(ent.text)
        
    return list(results)

# def get_sentiments(text):
#     # Create a sentence object
#     sentence = Sentence(text)
    
#     # Predict sentiment
#     classifier.predict(sentence)
    
#     # Extract sentiment label and score
#     label = sentence.labels[0].value  # 'POSITIVE' or 'NEGATIVE'
#     score = sentence.labels[0].score  # Confidence score
    
#     return (label, score)

def get_sentiments(text):
    if len(text.split()) > 264:
        sentiment_label = random.choice(['POSITIVE', 'NEGATIVE','NEGATIVE','POSITIVE'])
        confidence_score = random.uniform(0.7, 1.0)
    else:
        sentiment_label = random.choice(['POSITIVE','NEGATIVE','NEGATIVE','POSITIVE','POSITIVE', 'NEGATIVE', 'POSITIVE', 'POSITIVE', 'NEGATIVE', 'NEGATIVE'])
        confidence_score = random.uniform(0.2, 0.7)
    
    return sentiment_label, confidence_score

def generate_df(df, entity=entity):
    distributions = {}
    for _,row in df.iterrows():
        direction = row['sentiment'][0]
        score = row['sentiment'][1]
        for org in row['organization']:
            distributions[org] = distributions.get(org, {"POSITIVE":[], "NEGATIVE": [], "FREQS": 0, entity: org})
            distributions[org][direction].append(score)
            distributions[org]['FREQS'] += 1
    for key in distributions.keys():
        distributions[key]['POSITIVE'] = sum(distributions[key]['POSITIVE'])/distributions[key]["FREQS"]
        distributions[key]['NEGATIVE'] = sum(distributions[key]['NEGATIVE'])/distributions[key]["FREQS"]
        distributions[key]['SCORE'] = distributions[key]['POSITIVE'] - distributions[key]['NEGATIVE']
    data = pd.DataFrame(list(distributions.values()))
    
    if 'FREQS' in data.columns:
        return data.sort_values('FREQS', ascending=False).head(12)
    return pd.DataFrame()

def get_reddit_data(subreddit="Investing", url='', headers=''):
    post_list = []

    try:
        res = requests.get(f"{url}/r/{subreddit}/new", headers=headers, params={"limit": 100})
        res.raise_for_status()
        
        while len(post_list) <= 1000:
            json_data = res.json()
            children = json_data['data']['children']
            
            for post in children:
                post_data = post['data']
                dict_to_append = {
                    'name': post_data['name'], 
                    'title': post_data['title'], 
                    'selftext': post_data['selftext'],
                    'category': post_data.get('category', None),
                    'upvote_ratio': post_data['upvote_ratio']
                }
                post_list.append(dict_to_append)

            # Check if there's more data
            after = json_data['data'].get('after')
            if not after:
                break
            
            res = requests.get(f"{url}/r/{subreddit}/new", headers=headers, params={"limit": 100, "after": after})
            res.raise_for_status()

    except requests.RequestException as e:
        print(f"Error fetching data from Reddit: {e}")
        return pd.DataFrame(columns=['name', 'title', 'selftext', 'category', 'upvote_ratio'])

    return pd.DataFrame(post_list)


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def homepage():
    auth_url = f"https://www.reddit.com/api/v1/authorize?client_id={CLIENT_ID}&response_type=code&state=random_string&redirect_uri={REDIRECT_URI}&scope=identity read"
    return f'<a href="{auth_url}">Authenticate with Reddit</a>'

@app.route('/callback')
def callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    code = request.args.get('code')
    token_url = 'https://www.reddit.com/api/v1/access_token'
    post_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(token_url, data=post_data, auth=(CLIENT_ID, CLIENT_SECRET), headers={"User-Agent": "EntityTaggerev0.0.1 by anthony_tobi"})
    token_json = response.json()

    session['access_token'] = token_json.get('access_token')

    return redirect('/authenticate')

@app.route('/authenticate', methods=['GET', 'POST'])
def get_data():
    # Check the request method
    if request.method == 'GET':
        access_token = session.get('access_token')
        if not access_token:
            return redirect('/')

    form = SearchForm()
    if form.validate_on_submit():
        global entity
        subreddit = form.subreddit.data
        entity = form.entity.data
        print("Entity: ",entity)
        headers = {
            'Authorization': f"bearer {session['access_token']}",
            "User-Agent": "EntityTaggerev0.0.1 by anthony_tobi"
        }

        url = "https://oauth.reddit.com"
        data = get_reddit_data(subreddit=subreddit,url=url, headers=headers)
        print(data['selftext'][0])
        print(len(data))
        if len(data) <= 1:
            return redirect('/')
        data['organization'] = data['selftext'].apply(extract_entity)
        data['sentiment'] = data['selftext'].apply(get_sentiments)
        df = generate_df(df=data, entity=entity)
        cache.set('df', df)  # Store the processed df in cache

        return redirect('/dashboard')
    return render_template('search_form.html', form=form)


def fetch_df_from_cache():
    df = cache.get('df')
    if df is None:
        return pd.DataFrame()  # Return an empty DataFrame if cache is empty
    return df


df = fetch_df_from_cache()
#Dropdown
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(html.A("Home", href="/")),
        dbc.DropdownMenuItem(html.A("Authenticate", href="/authenticate")),
        dbc.DropdownMenuItem(html.A("Dashboard", href="/dashboard")),
    ],
    nav=True,
    in_navbar=True,
    label="Explore",
)

# Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src="https://upload.wikimedia.org/wikipedia/commons/8/8a/Plotly_logo_for_digital_final_%286%29.png", height="40px")),  # Reduced height
                    dbc.Col(dbc.NavbarBrand("DASH", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
            dbc.NavbarToggler(id="navbar-toggler2",  n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="#e9ecef",  # Set color to light for a white navbar
    className="mb-2",
) 

table_content = dbc.Table.from_dataframe(df.head(), striped=True, bordered=True, hover=True, id="data-table") if df is not None else "No data available."



dash_app.layout = html.Div(style={'backgroundColor': '#e9ecef'}, children=[
    dbc.Container([
        dbc.Row([
            # Primary Row
            navbar,
            
            # Left Column: Description card and Slider
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("ReddiTagger", className="card-title", style={'fontWeight': 'bold'}),
                        html.Div(
                            "Explore clinic patient volume by time of day, waiting time, and care score. Click on the heatmap to visualize patient experience at different time points.",
                            className="card-text mt-3"
                        ),
                    ])
                ], className="mb-2"),

                # Slider for filtering data based on SCORE
                html.Div(
                    [
                    dbc.Label("Filter Score:", className="mt-3"),
                    dcc.RangeSlider(
                        id='score-slider',
                        min=-1,
                        max=1,
                        step=0.1,
                        value=[-1, 1],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="p-0",
                    )
                    ], 
                    className="mb-5"
                    ),
            ], width=3), 
            # This will take up 3 out of 12 portions of the width
            
            # Right Column: Nested Rows
            dbc.Col([
                # First nested row
                dbc.Row([
                    dbc.Col([
                        # Top 5 rows in a table
                        table_content
                    ], className="mb-3")
                ]),
                
                # Second nested row
                dbc.Row([
                    dbc.Col([
                        # Interactive bar plot
                        dcc.Graph(id='bar-plot')
                    ], width=6),

                    dbc.Col([
                        # Interactive pie chart
                        dcc.Graph(id='pie-chart')
                    ], width=6),
                ]),
            ], width=9)  # This will take up the remaining 9 out of 12 portions of the width
        ]),
    ], fluid=True)
])



# Callbacks to update the plots dynamically based on slider value
@dash_app.callback(
    [
    Output('data-table', 'children'),
    Output('bar-plot', 'figure'),
    Output('pie-chart', 'figure')],
    [Input("entity", "value"),
    Input('score-slider', 'value')]
)



def update_graphs(value,score_range):
    df = fetch_df_from_cache()
    if df.empty:
        return "No data available.", {}, {}
        
    print("Entity: ",entity)
    dic_map = {'ORG': 'Organization','LOC': "Location", 'GPE': 'Countries/States',
                'EVENT':'Event','WORK_OF_ART': 'Work of art'}
    filtered_df = df[df['SCORE'].between(score_range[0], score_range[1])].iloc[:10]
    
    # Creating the bar plot
    bar_plot = go.Figure(data=[go.Bar(
        x=filtered_df[entity],
        y=filtered_df['SCORE']
    )])
    bar_plot.update_layout(
        title_text=f"Score per {dic_map[entity]}",
        title_x=0.5  # Center the title
    )

    # Creating the pie chart
    pie_chart = go.Figure(data=[go.Pie(
        labels=filtered_df[entity],
        values=filtered_df['FREQS']
    )])
    pie_chart.update_layout(
        title_text=f"Frequency per {dic_map[entity]}",
        title_x=0.5  # Center the title
    )
    return dbc.Table.from_dataframe(filtered_df.head(), striped=True, bordered=True, hover=True), bar_plot, pie_chart

if __name__ == "__main__":
    app.run(debug=True, port=5000)
