from flask import Flask, request, redirect, session
import os
import requests
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

data = {
    'POSITIVE': [0.1, 0.5, 0.8, 0.6, 0.3],
    'NEGATIVE': [0.9, 0.5, 0.2, 0.4, 0.7],
    'FREQS': [10, 20, 30, 40, 50],
    'ORG': ['A', 'B', 'C', 'D', 'E'],
    'SCORE': [0.7, 0.3, 0.8, 0.9, 0.6]
}
df = pd.DataFrame(data)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random key for session encryption
dash_app = dash.Dash(__name__, server=app, 
                    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                    external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname='/dashboard/')

dash_app.title = "ReddiTagger"

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'


# Create Dash layout
dash_app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            # Top 5 rows in a table
            dbc.Table.from_dataframe(df.head(), striped=True, bordered=True, hover=True)
        ], width=6),

        dbc.Col([
            # Slider for filtering data based on SCORE
            html.Label("Filter by SCORE:"),
            dcc.RangeSlider(
                id='score-slider',
                min=0,
                max=1,
                step=0.1,
                value=[0, 1],
                marks={i/10: str(i/10) for i in range(11)},
                tooltip={"placement": "bottom"}
            )
        ], width=6),
    ]),
    
    dbc.Row([
        dbc.Col([
            # Interactive histogram
            dcc.Graph(id='histogram')
        ], width=4),

        dbc.Col([
            # Interactive bar plot
            dcc.Graph(id='bar-plot')
        ], width=4),

        dbc.Col([
            # Interactive pie chart
            dcc.Graph(id='pie-chart')
        ], width=4),
    ]),
])

# Callbacks to update the plots dynamically based on slider value
@dash_app.callback(
    [Output('histogram', 'figure'),
     Output('bar-plot', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('score-slider', 'value')]
)

def update_graphs(score_range):
    filtered_df = df[df['SCORE'].between(score_range[0], score_range[1])]
    
    histogram = px.histogram(filtered_df, x='SCORE', nbins=10, title="Score Distribution")
    bar_plot = px.bar(filtered_df, x='ORG', y='FREQS', title="Frequency per Organization")
    pie_chart = px.pie(filtered_df, names='ORG', values='FREQS', title="Frequency Distribution")
    
    return histogram, bar_plot, pie_chart

@app.route('/')
def homepage():
    auth_url = f"https://www.reddit.com/api/v1/authorize?client_id={CLIENT_ID}&response_type=code&state=random_string&redirect_uri={REDIRECT_URI}&scope=identity"
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
    return redirect('/dashboard')

# @app.route('/fetch_data')
# def fetch_data():
#     headers = {
#         'Authorization': f"bearer {session['access_token']}",
#         "User-Agent": "EntityTaggerev0.0.1 by anthony_tobi"
#     }
#     response = requests.get('https://oauth.reddit.com/r/investing/new', headers=headers, params={"limit": 100})
#     user_data = response.json()
#     # You can fetch more data and process as needed
#     return str(user_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
