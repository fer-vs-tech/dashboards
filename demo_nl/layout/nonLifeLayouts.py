import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table

lightHstyle = {'fontFamily': 'calibri', 'color': '#5DADE2'}
darkHstyle = {'fontFamily': 'calibri', 'color': '#3498DB'}

lightTabStyle = {'padding': '0', 'line-height': '5vh'}
lightTabSelectedStyle = {'padding': '0', 'line-height': '5vh'}
darkTabStyle = {"backgroundColor":"#616A6B", 'padding': '0', 'line-height': '5vh'}
darkTabSelectedStyle = {"backgroundColor":"#707B7C", 'padding': '0', 'line-height': '5vh'}


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#d6d6d6',
    'color': 'white',
    'padding': '6px'
}

licLayout = html.Div([
    #html.Br(),
    dcc.Store(id="localTheme"),
    html.Div(id="dummy-fer"),
    #dbc.Switch(id='my-boolean-switch'),
    #html.Br(),
    dbc.Row([
        dbc.Col("",width=4),
        dbc.Col(html.Div(children=html.H4('Variable'), id="run-off-var-label", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width":"100%"}, justify=True),
    html.Br(),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style=lightHstyle),
    html.Br(),
    html.H5('Program', style=lightHstyle),
    dcc.Dropdown(id='dd-inclaim-program', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Portfolio', style=lightHstyle),
    #dbc.Select(id='dd-inclaim-portfolio', options=['fer'], value='fer', style={"backgroundColor":"#616A6B", "textColor":"white"}),
    dcc.Dropdown(id='dd-inclaim-portfolio', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('LDF Method', style=lightHstyle),
    dcc.Dropdown(id='dd-inclaim-method', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Variable', style=lightHstyle),
    # dcc.Dropdown(id='dd-inclaim-variable', options=['Claims Numbers (Incremental)', 'Incremental Paid Claims (Pre-inflation Adj)',
    #                                                'Incremental Case Reserves (Pre-Inflation Adj)', 'Incremental Incurred Claims (Pre-Inflation Adj)',
    #                                                'Incremental Paid Claims', 'Incremental Case Reserves', 'Incremental Incurred Claims',
    #                                                 'Cumulative Paid Claims', 'Cumulative Incurred Claims', 'Link Ratios (Pre-Outlier)'],
    #              value='Incremental Paid Claims', optionHeight=55, clearable=False),
    dcc.Dropdown(id='dd-inclaim-variable', options=[
        {'label': '1. Incrementals', 'value': 'none', 'disabled': True},
        {'label': 'Tri_Paid_Claims_By_Year', 'value': 'Tri_Paid_Claims_By_Year', 'disabled': False},
        {'label': 'Tri_Claim_Costs_By_Year', 'value': 'Tri_Claim_Costs_By_Year', 'disabled': False},
        {'label': 'Tri_Case_Reserves_By_Year', 'value': 'Tri_Case_Reserves_By_Year', 'disabled': False},
        #{'label': 'Tri_Claim_Numbers_By_Year', 'value': 'Tri_Claim_Numbers_By_Year', 'disabled': True},
        #{'label': 'Tri_Claim_Average_By_Year', 'value': 'Tri_Claim_Average_By_Year', 'disabled': True},
        {'label': '2. Cumulatives', 'value': 'none', 'disabled': True},
        {'label': 'Tri_Paid_Claims', 'value': 'Tri_Paid_Claims', 'disabled': False},
        {'label': 'Tri_Case_Reserves', 'value': 'Tri_Case_Reserves', 'disabled': False},
        {'label': 'Tri_Claim_Costs', 'value': 'Tri_Claim_Costs', 'disabled': False},
        #{'label': 'Tri_Claim_Numbers', 'value': 'Tri_Claim_Numbers', 'disabled': False},
        #{'label': 'Tri_Claim_Average', 'value': 'Tri_Claim_Average', 'disabled': False},
        ],
        value='Tri_Paid_Claims_By_Year', searchable=False, clearable=False),
    html.Br(),

    html.Div([html.H5('Dev Period Position', style=lightHstyle)
                 , dcc.RangeSlider(id='slider-dev-inclaim'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ]),
    html.Div([html.H5('Origin Period Position', style=lightHstyle)
                 , dcc.RangeSlider(id='slider-origin-inclaim'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ])

    ], style={'marginLeft': 20}), width=2)
    , dbc.Col(html.Div([
    dcc.Tabs(id='tabs-lic', value='', children=[
        dcc.Tab(label='Data', value='tab-lic-data', style=lightTabStyle, selected_style=lightTabSelectedStyle),
        dcc.Tab(label='Graphics', value='tab-lic-graph', style=lightTabStyle, selected_style=lightTabSelectedStyle),
    ], style={"height":"5vh"})
    , html.Div(id='tabs-lic-content-inclaim', style={"display":"overflow"})#, "backgroundColor": "black"})
    # , html.Div(dcc.Loading(id="loading-1",type="default"), id="divLoad"),
    ], style={'marginRight': 20}), width=10)], style={'width':'100%'} )
    ], id="lic-interactive", style={"overflow":"visible", "paddingLeft":"10px"})

analysisLayout = html.Div([
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H4("Data Analysis", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width": "100%"}, justify=True),
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(dbc.RadioItems(
            options=[
                {"label": "Outlier Analysis", "value": 1},
                {"label": "Trend Analysis", "value": 2},
            ],
            value=1,
            id="radioitems-input-data-analysis",
            inline=True,
        ), width=6),
        dbc.Col("", width=2),
    ], style={"textAlign":"center", 'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Br(),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Hr(),
    html.H5('Program', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-analysis-program', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Portfolio', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-analysis-portfolio', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('LDF Method', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-analysis-method', options=[''], value='', clearable=False),
    html.Br(),
    html.Div([html.H5('Dev Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'})
                 , dcc.RangeSlider(id='slider-dev-analysis'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ]),
    html.Div([html.H5('Origin Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'})
                 , dcc.RangeSlider(id='slider-origin-analysis'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ])

    ], style={'marginLeft': 20}), width=2)
    , dbc.Col(html.Div([
    dcc.Tabs(id='tabs-analysis', value='tab-analysis-graph', children=[
        dcc.Tab(label='Pre-Outlier ATA Factors', id="pre-ata", value='tab-analysis-preoutlier', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
        dcc.Tab(label='Outlier Analysis', id="middle-ata", value='tab-analysis-graph', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
        dcc.Tab(label='Post-Outlier ATA Factors', id="post-ata", value='tab-analysis-postoutlier', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
    ], style={"height":"5vh"})
    , html.Div(id='tabs-lic-content-analysis')
    # , html.Div(dcc.Loading(id="loading-1",type="default"), id="divLoad"),
    ], style={'marginRight': 20}), width=10)], style={'width':'100%'} )
    ])

ataLayout = html.Div([
    #html.Br(),
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H4("Age-To-Age Factors (Post Data Analysis)", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width": "100%"}, justify=True),
    html.Br(),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Hr(),
    html.H5('Program', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-ata-program', options=[''], optionHeight=55, value='', clearable=False),
    html.Br(),
    html.H5('Portfolio', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-ata-portfolio', options=[''], value='', optionHeight=55, clearable=False),
    html.Br(),
    html.H5('LDF Method', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-ata-method', options=[''], value='', optionHeight=55, clearable=False),
    html.Br(),
    html.Div([html.H5('Dev Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'})
                 , dcc.RangeSlider(id='slider-dev-ata'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ]),
    html.Div([html.Br(),
        html.H5('Origin Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
        dcc.RangeSlider(id='slider-origin-ata'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
        ], style={"display":"block"}, id="ata-origin-slider"),
    ], style={'marginLeft': 20}), width=2)
    , dbc.Col(html.Div([
    dcc.Tabs(id='tabs-ata', value='tab-ata-graph', children=[
        dcc.Tab(label='ATA Factors Statistics', value='tab-ata-statistics', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
        dcc.Tab(label='ATA Factors Graphic', value='tab-ata-graph', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
    ], style={"height":"5vh"})
    , html.Div(id='tabs-lic-content-ata')
    # , html.Div(dcc.Loading(id="loading-1",type="default"), id="divLoad"),
    ], style={'marginRight': 20}), width=10)], style={'width':'100%'} )
    ])


lrcFitStatisticsLayout = html.Div([
    #html.Br(),
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H4("GoF Test Statistics & Test Results", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width": "100%"}, justify=True),
    html.Br(),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Hr(),
    html.H5('Portfolio', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrcstats-portfolio', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Method', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrcstats-method', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Distribution', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrcstats-distribution', options=[''], value='', clearable=False),
    html.Br(),
        html.H5('Variable', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
        dcc.Dropdown(id='dd-lrcstats-variable', options=[''], value='', clearable=False),
    ]),width=2),
    dbc.Col(
        html.Div([
            dcc.Tabs(id='tabs-lrcstats', value='tab-lrc-stats-results', children=[
                dcc.Tab(label='Test Statistics', value='tab-lrc-stats', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
                dcc.Tab(label='Test Results', value='tab-lrc-stats-results', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'})
            ], style={"height": "5vh"})
            , html.Div(id='lrc-stats-content')
        ], style={'marginRight': 20})
        ,width=10)
    ]),
    ], style={"overflow":"visible", "paddingLeft":"10px"})

lrcFitRisksLayout = html.Div([
    #html.Br(),
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H4("Best Fit Selection", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width": "100%"}, justify=True),
    html.Br(),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Hr(),
    html.H5('Portfolio', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrcrisk-portfolio', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Method', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrcrisk-method', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Distribution', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrcrisk-distribution', options=[''], value='', clearable=False),
    html.Br(),
        html.H5('Variable', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
        dcc.Dropdown(id='dd-lrcrisk-variable', options=['Combined Ratio'], value='Combined Ratio', clearable=False),
    ]),width=2),
    dbc.Col(
        html.Div([
            dcc.Tabs(id='tabs-lrcrisk', value='tab-lrcrisk-spiders', children=[
                dcc.Tab(label='', value='tab-lrcrisk-spiders', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'})            ], style={"height": "5vh"})
            , html.Div(id='lrc-risk-content',style={"display":"inline", "width":"80%", "textAlign":"center"})
        ], style={'marginRight': 20})
        ,width=10)
    ]),
    ], style={"overflow":"visible", "paddingLeft":"10px"})


lrcEvalLayout = html.Div([
    #html.Br(),
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H4("LRC Evaluate Results", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width": "100%"}, justify=True),
    html.Br(),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Hr(),
    html.H5('Portfolio', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrceval-portfolio', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Method', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrceval-method', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Variable', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-lrceval-variable', options=[''], value='', clearable=False),
    ]),width=2),
    dbc.Col(
        html.Div([
            dcc.Tabs(id='tabs-lrceval', value='tab-lrceval-graph', children=[
                dcc.Tab(label='Results', value='tab-lrceval-stats', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
                dcc.Tab(label='Chart', value='tab-lrceval-graph', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'})
            ], style={"height": "5vh"})
            , html.Div(id='lrc-eval-content',style={"display":"inline", "width":"80%", "textAlign":"center"})
        ], style={'marginRight': 20})
        ,width=10)
    ]),
    ], style={"overflow":"visible", "paddingLeft":"10px"})

#
# lrcEvalLayout = html.Div([html.Br(),
#     html.H3("LRC Evaluate", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkblue'}), html.Br(),
#     dbc.Row([
#         dbc.Col("",width=3),
#         dbc.Col(dcc.Dropdown(id='dd-lrc-eval-portfolio', options=[''], value='', searchable=False, clearable=False),
#                 width=3, style={"textAlign": "center"}),
#         dbc.Col(dcc.Dropdown(id='dd-lrc-eval-variable', options=[''], value='', searchable=False, clearable=False),
#             width=3, style={"textAlign": "center"}),
#         dbc.Col("", width=3),
#     ]),
#     dbc.Row([
#         html.Br(),html.P(),
#         dbc.Col(html.Div("", id="lrc-evaluate-container"), width=12)
#     ])
#
# ])

devFactorLayout = html.Div([
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H4("Development Factors", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width": "100%"}, justify=True),
    dbc.Row([dbc.Col("", width=4), dbc.Col([dbc.RadioItems(
        options=[
            {"label": "Data", "value": 1},
            {"label": "Chart", "value": 2},
        ],
        value=2,
        id="radioitems-input-dev",
        inline=True,
    )], width=6), dbc.Col("", width=2)], style={"textAlign":"center", 'fontFamily': 'calibri', 'color': 'darkblue'}),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Hr(),
    html.H5('Program', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-factor-program', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Portfolio', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-factor-portfolio', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Dev Factor', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-factor-method', options=[''], value='', clearable=False),
    html.Br(),
    html.Div([
        html.H5('All Methods', style={"display":"inline-block", 'fontFamily': 'calibri', 'color': 'darkblue', "paddingRight":"10px"}),
        dbc.Switch(id="switch-all-factors",
                   label="",
                   value=True,
                   style={"display":"inline-block", "width": "10px"},
                   ),
        html.Br()
        ], id="div-switch-all-factors", style={"display":"none"}),
    html.Br(),
    html.Div([html.H5('Dev Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'})
                 , dcc.RangeSlider(id='slider-dev-factor'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ]),
    html.Br(),
    html.Div([html.H5('Origin Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'})
                     , dcc.RangeSlider(id='slider-origin-factor'
                                       , min=1
                                       , max=2
                                       , marks={1: {'label': '1'},
                                                2: {'label': '2'}}
                                       )
                  ], style={"display":"none"}, id="dev-factors-origin-menu")
    ], style={'marginLeft': 20}), width=2),
        dbc.Col(html.Div([
    html.Br(),
    dcc.Tabs(id='tabs-factor', value='tab-factor-content', children=[
        dcc.Tab(label='Loss Development Factors', value='tab-factor-content', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
        dcc.Tab(label='Ultimate Development Factors', value='tab-ultimate-factor-content', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
    ], style={"height":"5vh"})
    , html.Div(id='tabs-lic-content-factor')
    # , html.Div(dcc.Loading(id="loading-1",type="default"), id="divLoad"),
    ], style={'marginRight': 20}), width=10)], style={'width':'100%'} )
    ])

projectedLayout = html.Div([
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H4("Projected Results", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width": "100%"}, justify=True),
    dbc.Row([dbc.Col("", width=4), dbc.Col([dbc.RadioItems(
        options=[
            {"label": "Data", "value": 1},
            {"label": "Chart", "value": 2},
        ],
        value=2,
        id="radioitems-projected",
        inline=True,
    )], width=6), dbc.Col("", width=2)], style={"textAlign": "center", 'fontFamily': 'calibri', 'color': 'darkblue'}),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Hr(),
    html.H5('Program', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-projected-program', options=[''], optionHeight=55, value='', clearable=False),
    html.Br(),
    html.H5('Portfolio', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-projected-portfolio', options=[''], value='', optionHeight=55, clearable=False),
    html.Br(),
    html.H5('LDF Method', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-projected-method', options=[''], value='', optionHeight=55, clearable=False),
    html.Br(),
    html.H5('Variable', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-projected-variable', options=[], value='', clearable=False),
                 # options=[{'label': 'Cumulatives', 'value': 'none', 'disabled': True},
                 #      {'label': 'Tri_Claim_Costs_Proj', 'value': 'Tri_Claim_Costs_Proj', 'disabled': False},
                 #      {'label': 'Tri_Claim_Numbers_Proj', 'value': 'Tri_Claim_Numbers_Proj', 'disabled': False}],
                 # value='Tri_Claim_Costs_Proj', optionHeight=55, clearable=False),
    html.Br(),
    html.Div([html.H5('Dev Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'})
                 , dcc.RangeSlider(id='slider-dev-projected'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ]),
    html.Div([html.H5('Origin Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'})
                 , dcc.RangeSlider(id='slider-origin-projected'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ])

    ], style={'marginLeft': 20}), width=2)
    , dbc.Col(html.Div([
    html.Br(),
    dcc.Tabs(id='tabs-projected', value='cumulative-projected', children=[
        dcc.Tab(label='Cumulative Incurred Claims Projected', value='cumulative-projected', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
        dcc.Tab(label='Incremental Incurred Claims Projected', value='incremental-projected', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
    ], style={"height":"5vh"})
    , html.Div(id='tabs-lic-content-projected')
    # , html.Div(dcc.Loading(id="loading-1",type="default"), id="divLoad"),
    ], style={'marginRight': 20}), width=10)], style={'width':'100%'} )
    ])

licSummaryLayout = html.Div([
    #html.Br(),
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H4("Claim Costs Summary", style={'textAlign': 'center', 'fontFamily': 'calibri', 'color': 'darkorange'}), width=6),
        dbc.Col("", width=2)
    ], style={"width": "100%"}, justify=True),
    html.Br(),
    dbc.Row([dbc.Col(
    html.Div([
    html.H2('Filters', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    html.Hr(),
    html.H5('Program', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-summary-program', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('Portfolio', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-summary-portfolio', options=[''], value='', clearable=False),
    html.Br(),
    html.H5('LDF Method', style={'fontFamily': 'calibri', 'color': 'darkblue'}),
    dcc.Dropdown(id='dd-summary-method', options=[''], value='', clearable=False),
    html.Br(),
    html.Div([html.H5('Origin Period Position', style={'fontFamily': 'calibri', 'color': 'darkblue'})
                 , dcc.RangeSlider(id='slider-origin-summary'
                                   , min=1
                                   , max=2
                                   , marks={1: {'label': '1'},
                                            2: {'label': '2'}}
                                   )
              ], id="lic-summary-orig-slider", style={"display":"block"})

    ], style={'marginLeft': 20}), width=2)
    , dbc.Col(html.Div([
    dcc.Tabs(id='tabs-summary', value='tab-summary-graph', children=[
        dcc.Tab(label='Claim Costs Results', value='tab-summary-results', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
        dcc.Tab(label='Results Chart', value='tab-summary-graph', style={'padding': '0', 'line-height': '5vh'}, selected_style={'padding': '0', 'line-height': '5vh'}),
    ])
    , html.Div(id='tabs-lic-content-summary')
    # , html.Div(dcc.Loading(id="loading-1",type="default"), id="divLoad"),
    ], style={'marginRight': 20}), width=10)], style={'width':'100%'} )
    ])

dbcTabs = html.Div([
html.Br(),
dbc.Row(dbc.Col(
dbc.Nav(
    [
        dbc.DropdownMenu(
            #, style={"backgroundColor":"#424949", "color":"#5DADE2"}
            [dbc.DropdownMenuItem("Run-off Triangles Input", id="first-section", n_clicks=0),
             dbc.DropdownMenuItem("Data Analysis", id="data-analysis", n_clicks=0),
             dbc.DropdownMenuItem("Age-to-Age Factors", id="ata-factors", n_clicks=0),
             dbc.DropdownMenuItem("Development Factor", id="dev-factor", n_clicks=0),
             dbc.DropdownMenuItem("Projected Results", id="projected-result", n_clicks=0),
             dbc.DropdownMenuItem("LIC Summary", id="lic-summary", n_clicks=0),
             html.Hr(),
             html.P(
                 "Non Life LIC Model information available",
                 className="text-muted px-4 mt-4",
             ),
             ],
            label="NL_LIC_Model",
            nav=True,
            direction="down",
            id="nav-menu",
            #align_end=True,
        ),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("GoF Test Statistics & Test Results", id="lrc-statistics", n_clicks=0),
             dbc.DropdownMenuItem("Best Fit Selection", id="lrc-risk", n_clicks=0),
             html.Hr(),
             html.P(
                 "Non Life LRC Fitting Information available",
                 className="text-muted px-4 mt-4",
             ),
             ],
            label="NL_LRC_Fit",
            nav=True,
            direction="down",
            id="fit-menu"
            # align_end=True,
        ),
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem("Evaluation Summary", id="eval-summary", n_clicks=0),
             html.Hr(),
             html.P(
                 "Non Life LRC Evaluation Information available",
                 className="text-muted px-4 mt-4",
             ),
             ],
            label="NL_LRC_Eval",
            nav=True,
            direction="down",
            id="eval-menu"
            # align_end=True,
        ),
        dbc.NavItem(dbc.NavLink("NL_Data_Prep", id="data-prep", n_clicks=0, disabled=True),
                    style={"backgroundColor":"#E3E3E4", "color":"black", "fontSize":"18px", 'textAlign': 'center',
                           "border":"2px solid", "borderColor":"grey", "borderRadius":"15px", 'fontFamily': 'calibri'})

    ],
    pills=False, justified=True,
), width=12), style={"marginLeft":"5px", "marginRight":"5px"}),
    dbc.Row([
        dbc.Col(html.Div("", id="run-off-submenu"), width=3),
        dbc.Col(html.Div("", id="lrc-fit-submenu"), width=3),
        dbc.Col(html.Div("", id="lrc-eval-submenu"), width=3),
        dbc.Col("", width=3),
    ]),
    dbc.Row(dbc.Col(html.Hr(style={'borderWidth': "5vh", "borderColor": "#B4E1FF", "opacity":"unset"}), width=12)),
    dbc.Row(dbc.Col(html.Div(id="content-fer"), width=12))
],style={"width":"100%", "display":"block"})


newNonLifeLayout = html.Div([
    html.Div([
    dbc.Row([
         dbc.Col("", width=4),
         dbc.Col([
             html.H3('RNA Analytics R³S Report Demo', style={'textAlign': 'center', 'fontFamily': 'arial', "color":"darkblue"}),
             html.Br()]
             ,width=4),
         dbc.Col([
             html.A('Home', href='/report'),
             dbc.Label(" | "),
             html.A('Logout', href='/logout'),
             html.Br(),
             dbc.Switch(id='my-boolean-switch', style={"display":"none"})
         ],
        style={"textAlign":"right", 'fontFamily': 'calibri', 'color': 'darkblue'}, width=4)
     ], style={'width':'100%', "backgroundColor":"#F2F3F4"}),
    #dbc.Row(dbc.Col(dbcTabs, width=12), style={"backgroundColor":"white", 'width':'100%'})
        ], id="he", style={"width":"100%", "backgroundColor":"#F2F3F4"}),
    html.Div(id="licinteractive", style={"width":"100%", "backgroundColor":"white"})
    ]), dbc.Row(dbc.Col(html.Div(dbcTabs, style={"width":"100%", "backgroundColor":"white"}), width=12))



first_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container',className="five columns")], size="lg", color="primary", type="border")
)

second_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-outlier', className="five columns")], size="lg", color="primary", type="border")
        )

ata_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-ata', className="five columns")], size="lg", color="primary", type="border")
        )

cumulative_projected_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-cumulative-projected', className="five columns")], size="lg", color="primary", type="border")
        )

incremental_projected_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-incremental-projected', className="five columns")], size="lg", color="primary", type="border")
        )

summary_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-summary', className="five columns")], size="lg", color="primary", type="border")
        )

lrc_risk_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-lrc-left', className="five columns", style={"width":"39%", "display":"inline-block"}),
                  html.Div(id='table-paging-with-graph-container-lrc-right', className="five columns", style={"width":"39%", "display":"inline-block"})]
            , size="lg", color="primary", type="border")
        )

lrc_stats_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-lrc-stats', className="five columns")], size="lg", color="primary", type="border")
        )

ultimate_dev_factor_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-ultimate', className="five columns")], size="lg", color="primary", type="border")
        )

lrc_eval_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-lrc-eval', className="five columns")], size="lg", color="primary", type="border")
        )

third_graph_layout = html.Div(
        dbc.Spinner (
        children=[html.Div(id='table-paging-with-graph-container-pvalue', className="five columns")], size="lg", color="primary", type="border")
        )


trendStatisticsReportLayout = dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-trend-table',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "Dev Year"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= 6,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )


analysis_trend_graph_layout = html.Div(
        dbc.Spinner (
        children=[
            html.Br(),
            dbc.Row([
                dbc.Col("", width=4),
                dbc.Col(dbc.RadioItems(
                    options=[
                        {"label": "Statistics", "value": 1},
                        {"label": "Chart", "value": 2},
                    ],
                    value=2,
                    id="radioitems-input-analysis-embbeded",
                    inline=True,
                    style={"display":"block"}
                ), width=4),
                dbc.Col("", width=4),
            ], style={"textAlign": "center", 'fontFamily': 'calibri', 'color': 'darkblue'}),
            html.Br(),
            html.Div(trendStatisticsReportLayout, id="trend-table-div", style={"display":"none"}),
            html.Div([
                    html.Div(id='table-paging-with-graph-analysis-embbeded-left', className="five columns", style={"float":"left", "marginRight": "5px"}),
                    html.Div(id='table-paging-with-graph-analysis-embbeded-right', className="five columns", style={"float":"left", "marginLeft": "5px"}),
                ],id="container-trend-analysis", style={"display":"inline-block"})
        ], size="lg", color="primary", type="border")
        )



PAGE_SIZE = 15
first_report_layout =html.Div(
                            dbc.Spinner(
                                    children=
                            [dash_table.DataTable(
                            id='table-sorting-filtering',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            #export_format='xlsx',
                            #export_headers='display',
                            #merge_duplicate_headers=True,
                            style_header={'fontWeight':'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)'
                                } for x in range(0, PAGE_SIZE)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional=[{
                                'if': {
                                    'column_id': '↓ Orig - Dev →'
                            },
                            'fontWeight':'bold',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                            ],
                            page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            ))


second_report_layout =html.Div(
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-outlier',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': '↓ Variable - Dev →'
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            ))

preOutlier_report_layout =html.Div([
                            html.Br(),
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-pre-outlier',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'1\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'darkgrey',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "↓ Origin - Dev →"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            #page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )])

preOutlier_statistics_report_layout =html.Div([
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-pre-outlier-stats',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'100px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'1\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'darkgrey',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "Statistics"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= 2,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )])


postOutlier_report_layout =html.Div([
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-post-outlier',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'1\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'darkgrey',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "↓ Origin - Dev →"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )])


postOutlier_statistics_report_layout =html.Div([
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-post-outlier-stats',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'100px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'1\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'darkgrey',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "Statistics"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= 2,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )])

ata_report_layout =html.Div([
                            html.Br(),
                            html.P(),
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-ata',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "Statistics"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )])


summary_report_layout =html.Div([
                            html.Br(),
                            html.P(),
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-summary',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "Origin"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )])


lrc_stats_report_layout =html.Div([
                            html.Br(),
                            html.P(),
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-lrc-stats',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "Test_Group"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )])

projected_report_layout =html.Div(
                            dbc.Spinner(
                                    children=
                            [dash_table.DataTable(
                            id='table-sorting-filtering-projected',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            #export_format='xlsx',
                            #export_headers='display',
                            #merge_duplicate_headers=True,
                            style_header={'fontWeight':'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} contains ' + '\'[\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'darkgrey'
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional=[{
                                'if': {
                                    'column_id': '↓ Orig - Dev →'
                            },
                            'fontWeight':'bold',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                            ],
                            page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            ))


ultimate_dev_report_layout =html.Div([
                            html.Br(),
                            html.P(),
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-ultimate',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)',
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'1.0000\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(200, 200, 200)',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "↓ Origin - Dev →"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )])



devFactorChartLayout = dbc.Spinner (
                            children=[html.Div(id='table-paging-with-graph-container-dfactor', className="five columns")], size="lg", color="primary", type="border"
                            )

devFactorTableLayout = dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-dfactor',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "Dev Factor Method"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            )


#dev_factor_report_layout = html.Div([devFactorChartLayout, html.Br(), devFactorTableLayout])




lrc_eval_double_report_layout = dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-lrc-eval',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'500px'
                                #,'overflowX': 'scroll'
                                ,'overflowY': 'auto'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)',
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'1.0000\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(200, 200, 200)',
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': "Variable"
                            },
                            'fontWeight': 'bold',
                            'fontFamily': 'calibri',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= 50,
                            page_action='none',
                            filter_action='none',
                            filter_query='',
                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[],

                                                    )
                                ], size="lg", color="primary", type="border"
                            )

third_report_layout =html.Div(
                            dbc.Spinner (
                            children=[dash_table.DataTable(
                            id='table-sorting-filtering-pvalue',
                            #data  = mola,
                            columns=[
                                #{'name': i, 'id': i, 'deletable': True} for i in headers
                                #{'name': str(key), 'id': str(key), 'deletable': True} for key in di
                                {'name': str(key), 'id': str(key), 'deletable': True} for key in range(0,1)
                            ],
                            style_header={'fontWeight': 'bold',
                                          'color': 'darkblue',
                                          'backgroundColor': 'rgb(230, 236, 252)',
                                          'textAlign': 'center'},
                            style_table={'height':'350px'
                                #,'overflowX': 'scroll'
                                #,'overflowY': 'scroll'
                                         },
                                style_data_conditional=[{
                                    'if': {
                                        'column_id': str(x),
                                        'filter_query': '{' + str(x) + '} eq ' + '\'-\''
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'color': 'rgb(240, 240, 240)'
                                } for x in range(0, 20)],
                            style_cell={
                                'height': '90',
                                # all three widths are needed
                                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'textAlign': 'left'
                                ,'whiteSpace': 'normal'
                            },
                            style_cell_conditional = [{
                            'if': {
                                'column_id': '↓ Orig - Dev →'
                            },
                            'fontWeight': 'bold',
                            'color': 'darkblue',
                            'backgroundColor': 'rgb(230, 236, 252)',
                            'textAlign': 'center'}
                                                     ]
                            , page_current= 0,
                            page_size= PAGE_SIZE,
                            page_action='none',
                            filter_action='none',
                            filter_query='',

                            sort_action='none',
                            sort_mode='multi',
                            sort_by=[]
                                                    )
                                ], size="lg", color="primary", type="border"
                            ))



chartLabelPrintStyle = {"fontFamily":"arial", "color":"darkblue", "textAlign":"center", "display":"inline"}
categoryLabelPrintStyle = {"fontFamily":"arial", "color":"darkblue", "textAlign":"center", "textSize":"14"}
variableLabelPrintStyle = {"fontFamily":"arial", "color":"orange", "textAlign":"center", "display":"inline", "textSize":"14"}

headerPDF = dbc.Row([
        dbc.Col(html.Img(src='assets/RNATransparent.png', style={'height': '100%', 'width': '50%', 'marginLeft': '5px', "display": "block-inline"}), width=2),
        dbc.Col(html.Div(id="final-report-title"),
                width=8, style={'borderRadius': '15px', "borderWeight": "40px"}),
        dbc.Col("", width=2)], style={'width': '100%'}), \
        dbc.Row(dbc.Col(html.Hr(), width=12))

pdfContentsLayout = html.Div([
                html.Br(),
                dbc.Row([
                dbc.Col(html.Img(src='assets/RNATransparent.png', style={'height': '100%', 'width': '50%', 'marginLeft': '5px', "display": "block-inline"}), width=2),
                dbc.Col(html.Div(id="killme"),
                        width=8, style={'borderRadius': '15px', "borderWeight": "40px"}),
                dbc.Col("", width=2)], style={'width': '100%', "display":"block"}), \
                dbc.Row(dbc.Col(html.Hr(), width=12)),
                # REPORT HEADER
                #dbc.Row(dbc.Col(headerPDF, width=12), style={'width': '100%', "textAlign": "center"}),
                html.Br(), html.Br(),
                  html.H5("RUN-OFF TRIANGLES INPUT", style=categoryLabelPrintStyle), html.Br(), html.Br(), html.Br(),
                  html.Div([dbc.Label("Incremental: ", style=chartLabelPrintStyle), dbc.Label("Tri_Paid_Claims_By_Year", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(), html.Br(),
                  html.Div(id='inc-runoff-Tri_Paid_Claims_By_Year-graph2', className="five columns"),
                  html.Br(),
                  html.Div([dbc.Label("Incremental: ", style=chartLabelPrintStyle), dbc.Label("Tri_Case_Reserves_By_Year", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(), html.Br(),
                  html.Div(id='inc-runoff-Tri_Case_Reserves_By_Year-graph2', className="five columns"),
                  html.Br(),html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),
                  html.Div([dbc.Label("Cumulative: ", style=chartLabelPrintStyle), dbc.Label("Tri_Paid_Claims", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(),
                  html.Div(id='inc-runoff-Tri_Paid_Claims-graph2', className="five columns"),
                  html.Br(),
                  html.Div([dbc.Label("Cumulative: ", style=chartLabelPrintStyle), dbc.Label("Tri_Case_Reserves", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(),
                  html.Div(id='inc-runoff-Tri_Case_Reserves-graph2', className="five columns"),
                  html.Br(),
                  html.Div([dbc.Label("Cumulative: ", style=chartLabelPrintStyle), dbc.Label("Tri_Claim_Costs", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(),
                  html.Div(id='inc-runoff-Tri_Claim_Costs-graph2', className="five columns"),
                  #NEW CATEGORY
                  html.Br(), html.Hr(), html.Br(),
                  html.H5("DATA ANALYSIS", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Outlier", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='outlier-graph2', className="five columns"),
                  #NEW CATEGORY
                  html.Br(), html.Hr(), html.Br(),
                  html.H5("ATA FACTORS", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Data Analysis", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='ata-graph2', className="five columns"),
                  # NEW CATEGORY
                  html.Br(), html.Br(),
                  html.Br(),html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),
                  html.Hr(),
                  html.H5("DEVELOPMENT FACTORS", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Post Analysis", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='dev-graph2', className="five columns"), html.Br(), html.Br(),
                  html.H6("Ultimate Development Factors2", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='ult-dev-graph2', className="five columns"),
                  # NEW CATEGORY
                  html.Br(), html.Br(),
                  html.Br(),html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),
                  html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),
                  html.Hr(),
                  html.H5("PROJECTED RESULTS", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Cumulative Incurred Claims Projected", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='cum-cl-graph2', className="five columns"), html.Br(), html.Br(),
                  html.H6("Incremental Incurred Claims Projected", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='inc-cl-graph2', className="five columns"),
                  # NEW CATEGORY
                  html.Br(), html.Br(),
                  html.Br(),html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),
                  html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),html.P(), html.Br(),
                  html.Hr(),
                  html.H5("LIC SUMMARY", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Claim Costs Summary", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='sum-graph2', className="five columns"), html.Br(), html.Br()],
    style={"width":"100%", "paddingLeft":"50px", "paddingRight":"50px", "display":"fluid", "overflow":"visible", "textAlign":"center"}, id="pdf-contents")


printableContentsLayout = html.Div([
                html.Br(),
                dbc.Row([
                dbc.Col(html.Img(src='assets/RNATransparent.png', style={'height': '100%', 'width': '50%', 'marginLeft': '5px', "display": "block-inline"}), width=2),
                dbc.Col("", width=2),
                dbc.Col(html.H2("Non Life Report", style={"fontFamily":"arial", "color":"darkblue", "textAlign":"center", "textSize":"18"}),
                        width=6, style={"textAlign":"center"}),
                dbc.Col("", width=2)], style={"textAlign":"center", 'width': '100%', "display":"block"}),
                dbc.Row(dbc.Col(html.Hr(), width=12)),
                # REPORT HEADER
                #dbc.Row(dbc.Col(headerPDF, width=12), style={'width': '100%', "textAlign": "center"}),
                  html.H5("RUN-OFF TRIANGLES INPUT", style=categoryLabelPrintStyle), html.Br(),
                  html.Div([html.H6("Incremental: ", style=chartLabelPrintStyle), html.H5("Tri_Paid_Claims_By_Year", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(),
                  html.Div(id='inc-runoff-Tri_Paid_Claims_By_Year-graph', className="five columns",
                           style={"display":"flex", "alignItems":"center", "justifyContent":"center"}),
                  html.Br(), html.Br(),
                  html.Div([html.H6("Incremental: ", style=chartLabelPrintStyle), html.H5("Tri_Case_Reserves_By_Year", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(),
                  html.Div(id='inc-runoff-Tri_Case_Reserves_By_Year-graph', className="five columns",
                           style={"display":"flex", "alignItems":"center", "justifyContent":"center"}),
                  html.Br(), html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
                  html.Div([html.H6("Cumulative: ", style=chartLabelPrintStyle), html.H5("Tri_Paid_Claims", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(),
                  html.Div(id='inc-runoff-Tri_Paid_Claims-graph', className="five columns",
                           style={"display":"flex", "alignItems":"center", "justifyContent":"center"}), html.Br(),
                  html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
                  html.Div([html.H6("Cumulative: ", style=chartLabelPrintStyle), html.H5("Tri_Case_Reserves", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(),
                  html.Div(id='inc-runoff-Tri_Case_Reserves-graph', className="five columns",
                           style={"display":"flex", "alignItems":"center", "justifyContent":"center"}),
                  html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
                  html.Div([html.H6("Cumulative: ", style=chartLabelPrintStyle), html.H5("Tri_Claim_Costs", style=variableLabelPrintStyle)],
                           style={"display":"block-inline"}),
                  html.Br(),
                  html.Div(id='inc-runoff-Tri_Claim_Costs-graph', className="five columns",
                           style={"display":"flex", "alignItems":"center", "justifyContent":"center"}),
                  #NEW CATEGORY
                  html.Br(), html.Hr(), html.Br(), html.Br(), html.Br(),
                  html.H5("DATA ANALYSIS", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Outlier", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='outlier-graph', className="five columns",
                                      style={"display":"flex", "alignItems":"center", "justifyContent":"center"}),
                  #NEW CATEGORY
                  html.Br(), html.Hr(), html.Br(), html.Br(), html.Br(),
                  html.H5("ATA FACTORS", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Data Analysis", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='ata-graph', className="five columns",
                                      style={"display":"flex", "alignItems":"center", "justifyContent":"center"}),
                  # NEW CATEGORY
                  html.Br(), html.Hr(), html.Br(), html.Br(), html.Br(),
                  html.H5("DEVELOPMENT FACTORS", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Post Analysis", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='dev-graph', className="five columns",
                                      style={"display":"flex", "alignItems":"center", "justifyContent":"center"}), html.Br(), html.Br(),
                  html.H6("Ultimate Development Factors", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='ult-dev-graph', className="five columns",
                                      style={"display":"flex", "alignItems":"center", "justifyContent":"center"}),
                  # NEW CATEGORY
                  html.Br(), html.Hr(), html.Br(), html.Br(), html.Br(), html.Br(),
                  html.H5("PROJECTED RESULTS", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Cumulative Incurred Claims Projected", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='cum-cl-graph', className="five columns",
                                      style={"display":"flex", "alignItems":"center", "justifyContent":"center"}), html.Br(), html.Br(),
                  html.Br(), html.Br(),html.Br(), html.Br(),
                  html.H6("Incremental Incurred Claims Projected", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='inc-cl-graph', className="five columns",
                                      style={"display":"flex", "alignItems":"center", "justifyContent":"center"}),
                  # NEW CATEGORY
                  html.Br(), html.Hr(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),
                  html.H5("LIC SUMMARY", style=categoryLabelPrintStyle), html.Br(),
                  html.H6("Claim Costs Summary", style=chartLabelPrintStyle),
                  html.Br(), html.Div(id='sum-graph', className="five columns",
                                      style={"display":"flex", "alignItems":"center", "justifyContent":"center"}), html.Br(), html.Br()],
    style={"width":"100%", "paddingLeft":"50px", "paddingRight":"50px", "display":"fluid", "overflow":"visible"}, id="visible-pdf-contents")

#
# printableMenu = html.Div([
#     dbc.Row(dbc.Col(html.H1("Preview Selection", style=categoryLabelPrintStyle), width=12)),
#     dbc.Row([
#             dbc.Col(dbc.Label("Program"), width=2),dbc.Col(dbc.Label("Portfolio"), width=2), dbc.Col(dbc.Label("Method"), width=2),
#             dbc.Col(dbc.Label("Dev Position"), width=2), dbc.Col(dbc.Label("Origin Position"), width=2),
#             dbc.Col(dbc.Label(html.Div("Generating...",id="status-save")), width=1),
#             dbc.Col(dbc.Label("Report type"), width=1)]),
#     dbc.Row([
#         dbc.Col(dcc.Dropdown(options=[], value=[], id="dd-program-printable", clearable=False), width=2),
#         dbc.Col(dcc.Dropdown(options=[], value=[], id="dd-portfolio-printable", clearable=False), width=2),
#         dbc.Col(dcc.Dropdown(options=[], value=[], id="dd-method-printable", clearable=False), width=2),
#         dbc.Col(dcc.RangeSlider(id='slider-dev-printable', min=1, max=2, marks={1: {'label': '1'},2: {'label': '2'}}),width=2),
#         dbc.Col(dcc.RangeSlider(id='slider-origin-printable', min=1, max=2, marks={1: {'label': '1'},2: {'label': '2'}}),width=2),
#         dbc.Col([
#             html.Div([dbc.Button("Generate PDF", id='save-pdf', n_clicks=0, style={"backgroundColor":"darkblue"})]),
#             html.Div([
#                 dbc.Spinner(size="sm")], id="spinnerContainer", style={"display":"none"})], width=1),
#         dbc.Col(dcc.Dropdown(options=["Landscape", "Portrait"], value=["Landscape"], id="dd-report-style-printable", clearable=False), width=1),
#     ]),
#     ], style={"display":"block"})


nonLifePrintableLayout = html.Div([
    dcc.Store(id="statusGen", data=0),
    dcc.Download(id="dcc-download-pdf-report"),
    dbc.Row([
        dbc.Col("", width=4),
        dbc.Col(html.H1('Non-Life Printable Version', style={'textAlign': 'center', 'fontFamily': 'arial'}), width=4),
        dbc.Col([html.A('Home', href='/report'), " | ", html.A('Logout', href='/logout')],
                 style={"textAlign":"right", 'fontFamily': 'calibri', 'color': 'darkblue'}, width=4)
    ], style={'width':'100%', "textAlign":"center"}),
    #PREVIEW MENU INTERACTIVE
    html.Br(),
    dbc.Row([
        dbc.Col(html.H5('Preview parameters', style={'textAlign': 'center', 'fontFamily': 'arial'}), id="dummy-check-label", width=12)
    ], style={'width':'100%', "textAlign":"center"}),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Label("Program"), width=2, style={"paddingLeft":"50px"}), dbc.Col(dbc.Label("Portfolio"), width=2), dbc.Col(dbc.Label("Method"), width=2),
        dbc.Col(dbc.Label("Dev Position"), width=2), dbc.Col(dbc.Label("Origin Position"), width=2),
        #dbc.Col(dbc.Label("Report Title"), width=2),
        #dbc.Col(dbc.Label("Report Orientation"), width=1),
        dbc.Col(dbc.Label(html.Div("Generating...", id="status-save")), width=2)
    ], style={'width': '100%', "textAlign": "center"}),
    dbc.Row([
        dbc.Col(dcc.Dropdown(options=[], value=[], id="dd-program-printable", clearable=False), width=2, style={"paddingLeft":"50px"}),
        dbc.Col(dcc.Dropdown(options=[], value=[], id="dd-portfolio-printable", clearable=False), width=2),
        dbc.Col(dcc.Dropdown(options=[], value=[], id="dd-method-printable", clearable=False), width=2),
        dbc.Col(dcc.RangeSlider(id='slider-dev-printable', min=1, max=2, marks={1: {'label': '1'}, 2: {'label': '2'}}), width=2),
        dbc.Col(dcc.RangeSlider(id='slider-origin-printable', min=1, max=2, marks={1: {'label': '1'}, 2: {'label': '2'}}), width=2),
        # dbc.Col([
        #     dbc.Input(type="text", placeholder="RNA Analytics - Non Life Report", id="parameter-report-title"),
        #     html.Div(id="killme2")
        # ], width=2),
        # dbc.Col(dcc.Dropdown(options=["Landscape", "Portrait"], value="Landscape", id="dd-report-style-printable", clearable=False), width=1),
        dbc.Col(dbc.Button("Generate PDF", id='save-pdf', n_clicks=0, style={"backgroundColor": "darkblue"}), width=1),
        dbc.Col(dbc.Button("Test PDF", id='save-html-pdf', n_clicks=0, style={"backgroundColor": "darkblue"}), width=1),
    ], style={'width':'100%', "textAlign":"center"}),
    html.Br(),
    dbc.Row([
        dbc.Col("", width=1),
        dbc.Col(html.Hr(), width=10),
        dbc.Col("", width=1)
    ], style={'width':'100%', "textAlign":"center"}),
    html.Br(),
    #REPORT LOADING SPINNER
    dbc.Row(dbc.Col(dbc.Spinner(
        children=[
            html.Div(id="dummySpinner")], size="lg", color="primary", type="border")
    ,width=12), style={'width':'100%', "textAlign":"center"}),
    html.Br(),
    #REPORT CONTENTS
    dbc.Row(dbc.Col(printableContentsLayout, width=12), id="row-pdf", style={'width':'100%', "textAlign":"center", "display":"none"}),
    dbc.Row(dbc.Col(pdfContentsLayout, width=12), style={"width":"100%", "textAlign":"center","display":"none"})

], style={"width":"100%", "overflow":"auto"})


