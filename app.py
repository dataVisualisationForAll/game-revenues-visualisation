import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

game_df = pd.read_csv(r'./datasets/video_game_sales.csv')

tweets_df = pd.read_csv(r'./datasets/tweets_frequency.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

top_games_agg = game_df.groupby(['Publisher','Name']).agg({'Global_Sales':'sum'}).reset_index()

top_20_games = top_games_agg.groupby('Publisher').apply(lambda x: x.sort_values('Global_Sales', ascending=False)).reset_index(drop=True).groupby('Publisher').head(20)

publisher_names = top_20_games.Publisher.unique()

sales = game_df.groupby('Publisher')[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().reset_index()

platform_revenues = game_df.groupby(['Platform','Name']).agg({'Global_Sales':'sum'}).reset_index()

platform_revenues = platform_revenues.groupby('Platform').apply(lambda x: x.sort_values('Global_Sales', ascending=False)).reset_index(drop=True).groupby('Platform').head(100)

platforms = platform_revenues.Platform.unique()

year_sales = game_df.groupby(['Publisher','Year_of_Release']).agg({'Global_Sales':'sum',
                                                                   'EU_Sales':'sum',
                                                                   'NA_Sales':'sum',
                                                                   'JP_Sales':'sum',
                                                                   'Other_Sales':'sum'}).reset_index().groupby('Publisher').apply(lambda x: x.sort_values('Year_of_Release')).reset_index(drop=True)
def fix_labels_design(fig):
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

colors = {
    'background': '#111111',
    'text': '#ffffff'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


app.layout = html.Div(

    children=[

        html.Div(
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'backgroundColor': colors['background']
            },

            children=[
                html.H1(
                    children='Games Revenues Visualisation Demo',
                    style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'backgroundColor': colors['background']
                    }
                ),

                html.Div(children='A web application for data visualisation.', style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'backgroundColor': colors['background']
                })
            ]),

        html.Div(style={'display': 'flex',
                        'flex-direction': 'row'}, children=[

            html.Div(style={'width': '49%'}, children=[



                html.H3("Publisher's Top 20 Games Revenue"),

                html.Div("Select a Publisher"),
                dcc.Dropdown(id='publisher-select',
                             options=[{'label': i, 'value': i}
                                      for i in publisher_names],
                             value='Take-Two Interactive',
                             style={
                                 'width': '400px',
                             }),

                html.Div('Units are in millions', style={'margin-top': '20px'}),
                dcc.Graph(id="pie-chart")
            ]),

            html.Div(style={'width': '49%'}, children=[



                html.H3("Publisher's Sales By Region",
                        style={'margin-top': '20px'}),


                dcc.RadioItems(id='region-select',
                               options=[
                                   {'label': 'Europe', 'value': 'EU_Sales'},
                                   {'label': 'North America', 'value': 'NA_Sales'},
                                   {'label': 'Japan', 'value': 'JP_Sales'},
                                   {'label': 'Rest of the World',
                                       'value': 'Other_Sales'}
                               ],
                               value='EU_Sales'
                               ),
                dcc.Graph(id="pie-chart-region")
              ]
            )
          ]
        ),
         html.Div(style={'display': 'flex',
                         'flex-direction': 'row'}, children = [
         html.Div(style={'width':'49%'},children = [
         html.Div(style = {'margin-top':'50px'}, children = [
            html.H3('Yearly Sales By Publisher'),
            html.Div([
            html.Div('Select Publisher'),
            dcc.Dropdown(id='publisher-y-select',
                         options=[{'label': i, 'value': i}
                                  for i in publisher_names],
                         value='Take-Two Interactive',
                        style={
                            'width':'400px'
                        }),
            dcc.RadioItems(id='time-region-select',
                           style={'margin-top':'10px'},
                          options=[
                                   {'label': 'Global','value': 'Global_Sales'},
                                   {'label': 'Europe', 'value': 'EU_Sales'},
                                   {'label': 'North America', 'value': 'NA_Sales'},
                                   {'label': 'Japan', 'value': 'JP_Sales'},
                                   {'label': 'Rest of the World','value': 'Other_Sales'},




                               ],
                               value='Global_Sales')]),

            dcc.Graph(id='time-bar-chart')

        ])
        ]),
            html.Div(style={'width':'49%'}, children = [
                html.Div(style = {'margin-top':'50px'},children = [
                    html.H3('SocialPoint Twitter Trend Analysis'),
                    html.Div('Select hashtags'),
                    dcc.Checklist(id='hashtag-checklist',
                        style={'margin-top':'10px', 'margin-bottom':'30px'},
                        options=[
                            {'label': '#socialpoint', 'value': 'socialpoint'},
                            {'label': '#dragoncity', 'value': 'dragoncity'},
                            {'label': '#monsterlegends', 'value': 'monsterlegends'},
                            {'label': '#wordlife', 'value': 'wordlife'},
                            {'label': '#tastytown', 'value': 'tastytown'}
                        ],

                        value=['socialpoint', 'dragoncity','monsterlegends','wordlife','tastytown']
                    ),
                    dcc.Graph(id="hashtag-chart")
                ])
            ]
            )
        ]),

        html.Div(style = {'margin-top':'50px'},children = [

            html.H3('Top 100 Selling Games by Platform'),
            html.Div('Select Platform'),
            dcc.Dropdown(id='platform-select',
                         options=[{'label': i, 'value': i}
                                  for i in platforms],
                         value='PS4',
                        style={
                            'width':'400px'
                        }),
            html.Div('loading may take a while',style = {'margin-top':'15px'}),
            dcc.Graph(id='stacked-bar-chart')
        ])

    ]
)


@app.callback(
    Output('pie-chart', 'figure'),
    [Input('publisher-select', 'value')]
)
def update_graph(grpname):
    import plotly.express as px
    fig = px.pie(top_20_games[top_20_games.Publisher == grpname], values='Global_Sales', names='Name')
    fix_labels_design(fig)
    return fig

@app.callback(
    Output('pie-chart-region', 'figure'),
    [Input('region-select', 'value')]
)
def update_graph_region(grpname):
    import plotly.express as px
    fig = px.pie(sales, values=grpname, names='Publisher')
    fix_labels_design(fig)
    return fig


@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('platform-select', 'value')]
)
def update_stacked_bar(grpname):
    import plotly.express as px
    fig = px.bar(platform_revenues[platform_revenues.Platform == grpname], x='Global_Sales', y='Platform',color='Name', orientation='h')
    fix_labels_design(fig)
    return fig

@app.callback(
    Output('time-bar-chart', 'figure'),
    [Input('publisher-y-select', 'value'),
     Input('time-region-select', 'value')]
)
def update_time_bar(grpname,rgsales):
    import plotly.express as px
    fig = px.bar(year_sales[year_sales.Publisher == grpname], x='Year_of_Release', y=rgsales)
    max_range = year_sales[year_sales.Publisher == grpname]['Global_Sales'].max()
    fig.update_yaxes(range=[0,max_range+5])
    fix_labels_design(fig)
    return fig

@app.callback(
    Output('hashtag-chart', 'figure'),
    [Input('hashtag-checklist', 'value')]
)
def update_twitter_bar(grplist):
    import plotly.express as px
    fig = px.bar(tweets_df, x='time', y=grplist, labels={
                     "value": "Number of Tweets containing hashtag",
                     "time" : "Day"

                 })
    fig.update_yaxes(range=[0,35])

    return fig



if __name__ == '__main__':
    app.run_server(debug=False)
