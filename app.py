# in browser: http://127.0.0.1:8050/

import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://herdiss.pythonanywhere.com/static/main.css'])

THEME = {
    'bgcol'      : '#22303c',
    'hcolor'     : '#ff5418',
    'white'      : '#ffffff',
    'font'       : 'Open Sans',
    'font-size1' : 22,
}

### LOAD AND EDIT DATA
df = pd.read_csv('/home/herdiss/mysite/lump_data.csv')
bdf = pd.read_csv('/home/herdiss/mysite/birds.csv')
mdf = pd.read_csv('/home/herdiss/mysite/mammals.csv')

col_df = pd.read_csv('/home/herdiss/mysite/parameter_names.txt')
df.columns = list(col_df.columns)
col_names = df.columns.values.tolist()

### MAKE A COLOR SCHEME BASED ON BOAT
colordict = {'Kongsey': '#636efa',
             'Saefugl': '#ef553b',
             'Fengsaell': '#00cc96',
             'Simma': '#ab63fa',
             'Arndis':'#ffa15a',
             'Sigurey':'#19d3f3',
             'Bara':'#ff6692'}

### APP LAYOUT
app.layout = dbc.Container([
    html.H1([
#        html.Span('2022  ', style={'color': THEME['hcolor']}),
        html.Span('húnaflói lumpfish fisheries ', style={'color': THEME['white']}),
        html.Span(' | ', style={'color': THEME['white']}),  #•
        html.Span(' bycatch analysis', style={'color': THEME['hcolor']}),
#        html.Span(' • ', style={'color': THEME['hcolor']}),

    ],
            style = {'font-family'  : 'Sans serif',
                     'font-variant' : 'small-caps',
                     'font-weight'  : 'lighter',
                     'font-size'    : '280%'},),

    html.Hr(style = {'color': THEME['white']}),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Label('select variable', style={'color'        : THEME['hcolor'],
                                                             'font-variant' : 'small-caps',
                                                             'font-size'    : THEME['font-size1']}),
                        dcc.Dropdown(
                            col_names[40:43],
                            col_names[40],
                            clearable=False,
                            id='dropy')
                    ])
                ],
                        width={'offset': 0},
                        md=4),

                dbc.Col([html.Div('CUMULATIVE CATCH BY BOAT', style={'color': 'white',
                                                                             'font-variant': 'small-caps',
                                                                             'font-size': 22,
                                                                             'font-weight': 'lighter'})
                         ])
            ],
                    align='end'
                    ),

            dbc.Row(dcc.Graph(id = 'cumsum_graph')),
        ]),
        dbc.Col(html.Img(src = 'https://herdiss.pythonanywhere.com/static/map.png', style={'margin-top': '15px'}), align='start')
    ]),


    dbc.Row([
        dbc.Col(
            html.Div([
                html.Label('select boat', style={'color'        : THEME['hcolor'],
                                                 'font-variant' : 'small-caps',
                                                 'font-size'    : THEME['font-size1'],
                                                 'margin-top'   : '10px'}
                           ),
                dcc.Dropdown(id='boat_menu',
                             value='Kongsey',
                             clearable=False,
                             options=[
                                 {'label' : 'A', 'value': 'Kongsey'},
                                 {'label' : 'B', 'value': 'Simma'},
                                 {'label' : 'C', 'value': 'Saefugl'},
                                 {'label' : 'D', 'value': 'Fengsaell'},
                                 {'label' : 'E', 'value': 'Arndis'},
                                 {'label' : 'F', 'value': 'Sigurey'},
                                 {'label' : 'G', 'value': 'Bara'}
                             ]),
            ]),
            width={'offset': 0},
            md=2
        ),

        dbc.Col(html.Div('BYCATCH BY SPECIES', style={'color': 'white',
                                                      'font-variant': 'small-caps',
                                                      'font-size': 22,
                                                      'font-weight': 'lighter'}))
    ],
            align='end'),
    dbc.Row(
        [dbc.Col(dcc.Graph(id='bar1')),
         dbc.Col(dcc.Graph(id='bar2')),
         ],
        align='top',
        className='g-0',
    ),
    html.Div(id='dd-output-container'),
],
                           fluid=True,
                           )

### APP LAYOUT ENDS

newnames = {'Kongsey':'A','Simma':'B','Saefugl':'C','Fengsaell':'D','Arndis':'E','Sigurey':'F','Bara':'G'}

@app.callback(Output('cumsum_graph', 'figure'),
              Input('dropy', 'value'))

def update_cumsum_graph(y):
    graph = px.line(df, x="Date", y=df[y],
                    width=900,
                    height=450,
                    markers=True,
                    color="Boat",
                    color_discrete_map=colordict,
                    category_orders={'Boat':['Kongsey','Simma','Saefugl','Fengsaell','Arndis','Sigurey','Bara']})

    # CHANGE NAMES OF ALL VARIABLES
    graph.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    graph.update_layout(paper_bgcolor='#22303c',
                        plot_bgcolor='#22303c',
                        legend=dict(
                            orientation="v",
                            yanchor="top",
                            y=1.055,
                            xanchor="right",
                            x=1.2,
                            font=dict(
                                size=16,
                                color="white"),)
                        )

    graph.update_xaxes(tickformat="%d/%m",
                     showline=True,
                     showgrid=False,
                     zeroline=False,
                     linewidth=2,
                     linecolor='white',
                     title_font=dict(size=16, color='white'),
                     tickfont=dict(size=14, color='white'),
                     title=dict(text="Date in 2022")
                     )


    graph.update_yaxes(showline=True,
                     showgrid=True,
                     gridcolor = 'grey',
                     zeroline=False,
                     linewidth=2,
                     linecolor='white',
                     title_font=dict(size=16, color='white'),
                     tickfont=dict(size=14, color='white'),
                     rangemode='tozero',
                     title=dict(text='Number (#)')
                     )

    return graph

@app.callback(
    [Output(component_id='bar1', component_property='figure'),
     Output(component_id='bar2', component_property='figure')],
    [Input(component_id='boat_menu', component_property='value')])

def update_bar_chart(boat):
    bdf1 = bdf[bdf['boat'] == boat]
    mdf1 = mdf[mdf['boat'] == boat]

    bar1 = px.bar(bdf1, x='bird', y='birds_total',
                  width=800,
                  height=420,
                  category_orders={'bird': ['common_eider', 'black_guillemot', 'common_murre', 'european_shag', 'northern_fulmar', 'long.tailed_duck', 'great_cormorant', 'red.throated_loon', 'atlantic_puffin']},
                  color='boat',
                  color_discrete_map=colordict)

    bar1.update_layout(paper_bgcolor='#22303c',
                       plot_bgcolor='#22303c',
                       showlegend=False,
                       )

    bar1.update_traces(width=0.75)

    bar1.update_xaxes(showline=True,
                      showgrid=False,
                      zeroline=False,
                      linewidth=2,
                      linecolor='white',
                      title_font=dict(size=16, color='white'),
                      tickfont=dict(size=14, color='white'),
                      title=dict(text=''),
                      tickvals=['common_eider', 'black_guillemot', 'common_murre', 'european_shag', 'northern_fulmar', 'long.tailed_duck', 'great_cormorant', 'red.throated_loon', 'atlantic_puffin'],
                      ticktext=['Common eider', 'Black guillemot', 'Common murre', 'European shag', 'Northern fulmar', 'Long-tailed duck', 'Great cormorant', 'Red-throated loon', 'Atlantic puffin']
                      )

    bar1.update_yaxes(showline=True,
                      showgrid=True,
                      gridcolor = 'grey',
                      zeroline=False,
                      linewidth=2,
                      linecolor='white',
                      title_font=dict(size=16, color='white'),
                      tickfont=dict(size=14, color='white'),
                      range=[0,51],
                     title=dict(text='Birds (#)')
                     )


    bar2 = px.bar(mdf1, x='mammal', y='mammals_total',
                  width=800,
                  height=423,
                  category_orders={'mammal': ['harbour_seal', 'grey_seal', 'harbour_porpoise', 'harp_seal', 'bottlenose_dolphin', 'white_beaked_dolphin']},
                  color='boat',
                  color_discrete_map=colordict)

    bar2.update_layout(paper_bgcolor='#22303c',plot_bgcolor='#22303c',showlegend=False)
    bar2.update_traces(width=0.5)

    bar2.update_xaxes(showline=True,
                      showgrid=False,
                      zeroline=False,
                      linewidth=2,
                      linecolor='white',
                      title_font=dict(size=16, color='white'),
                      tickfont=dict(size=14, color='white'),
                      title=dict(text=''),
                      tickvals=['harbour_seal', 'grey_seal', 'harbour_porpoise', 'harp_seal', 'bottlenose_dolphin', 'white_beaked_dolphin'],
                      ticktext=['Harbour seal', 'Grey seal', 'Harbour porpoise', 'Harp seal', 'Bottlenose dolph.', 'White-beaked dolph.']
                      )
    bar2.update_yaxes(showline=True,
                      showgrid=True,
                      gridcolor = 'grey',
                      zeroline=False,
                      linewidth=2,
                      linecolor='white',
                      title_font=dict(size=16, color='white'),
                      tickfont=dict(size=14, color='white'),
                      range=[0,7.1],
                      dtick=1,
                      title=dict(text='Marine mammals (#)')
                     )

    return bar1, bar2



if __name__ == '__main__':
    app.run_server(debug=False)
