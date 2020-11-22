import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

game_df = pd.read_csv(r'./datasets/video_game_sales.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


top_games_agg = game_df.groupby(['Publisher','Name']).agg({'Global_Sales':'sum'}).reset_index()
top_20_games = top_games_agg.groupby('Publisher').apply(lambda x: x.sort_values('Global_Sales', ascending=False)).reset_index(drop=True).groupby('Publisher').head(20)
publisher_names = top_20_games.Publisher.unique()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server



app.layout = html.Div([
    html.Div([dcc.Dropdown(id='publisher-select', options=[{'label': i, 'value': i} for i in publisher_names],
                          value='Take-Two Interactive', style={'width': '140px'})
             ]),
    dcc.Graph(id="pie-chart")                          
])

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('publisher-select', 'value')]
)

def update_graph(grpname):
    import plotly.express as px
    return px.pie(top_20_games[top_20_games.Publisher ==grpname], values='Global_Sales', names='Name')


if __name__ == '__main__':
    app.run_server(debug=False)





