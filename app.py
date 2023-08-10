from flask import Flask, request, redirect, session
import os
import requests
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd

data = {
    'POSITIVE': [0.1, 0.5, 0.8, 0.6, 0.3, 0.4, 0.7, 0.2, 0.5, 0.4],
    'NEGATIVE': [0.9, 0.5, 0.2, 0.4, 0.7, 0.6, 0.3, 0.8, 0.5, 0.6],
    'FREQS': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'ORG': ['Microsoft', 'Facebook', 'Google', 'Apple', 'Amazon', 'Netflix', 'Tesla', 'Adobe', 'Spotify', 'Twitter'],
    'SCORE': [0.7, 0.3, 0.8, -0.9, 0.6, -0.2, 0.9, -0.7, 0.1, 0.5]
}


df = pd.DataFrame(data)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random key for session encryption
dash_app = dash.Dash(__name__, server=app, 
                    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
                    external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname='/dashboard/')

dash_app.title = "ReddiTagger"

subreddit = [
    "Investing",
    "Events",
    "News",
    "Sunday",
]

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'

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

    return redirect('/authenticate')

@app.route('/authenticate')
def dashboard():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/')

    headers = {
        'Authorization': f"bearer {session['access_token']}",
        "User-Agent": "EntityTaggerev0.0.1 by anthony_tobi"
    }

    response = requests.get('https://oauth.reddit.com/r/investing/new', headers=headers, params={"limit": 100})
    user_data = response.json()
    # rest of your route logic...


# @app.route('/fetch_data')
# def fetch_data():
#     # You can fetch more data and process as needed
#     return str(user_data)



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


                dbc.Label("Select Entity:", className="mt-2"),
                dbc.Select(
                id="subreddit",
                options=[
                    {"label": "primary", "value": "primary"},
                    {"label": "secondary", "value": "secondary"},
                    {"label": "success", "value": "success"},
                    {"label": "danger", "value": "danger"},
                    {"label": "warning", "value": "warning"},
                    {"label": "info", "value": "info"},
                    {"label": "light", "value": "light"},
                    {"label": "dark", "value": "dark"},
                ],
                value="primary",
                ),

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
                        dbc.Table.from_dataframe(df.head(), striped=True, bordered=True, hover=True, id="data-table")
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
    [Input("subreddit", "value"),
    Input('score-slider', 'value')]
)



def update_graphs(subreddit,score_range):
    filtered_df = df[df['SCORE'].between(score_range[0], score_range[1])].iloc[:10]
    
    # Creating the bar plot
    bar_plot = go.Figure(data=[go.Bar(
        x=filtered_df['ORG'],
        y=filtered_df['SCORE']
    )])
    bar_plot.update_layout(
        title_text="Frequency per Organization",
        title_x=0.5  # Center the title
    )

    # Creating the pie chart
    pie_chart = go.Figure(data=[go.Pie(
        labels=filtered_df['ORG'],
        values=filtered_df['FREQS']
    )])
    pie_chart.update_layout(
        title_text="Frequency Distribution",
        title_x=0.5  # Center the title
    )
    return dbc.Table.from_dataframe(filtered_df.head(), striped=True, bordered=True, hover=True), bar_plot, pie_chart

if __name__ == "__main__":
    app.run(debug=True, port=5000)
