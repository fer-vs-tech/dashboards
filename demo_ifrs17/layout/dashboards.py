#ifrs17/layout/dashboards.py

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
import cm_dashboards.demo_ifrs17.layout.component_styles as styles


chart_contents = dbc.Row(children=[
                        dbc.Col([
                            dbc.Label("Summary type", style=styles.net_label_style),
                            dcc.Dropdown(
                                id="dashboards-options",
                                placeholder="Select Option ...",
                                persistence=True,
                                clearable=False,
                                options=["Insurance", "Reinsurance", "Net Position"],
                                value="Net Position",
                                style={
                                    "width": 200,
                                    # "height": "2px",
                                    "font-size": 12,
                                    "fontWeight": "normal",
                                }
                                # disabled=True,
                            ),
                        ], width="auto", style={'display': 'flex'}),
                    ], align="center")

menu = html.Div(id='dashboard-sub-menu',
                children=[
                    dbc.Tabs(
                        id="dashboard-tabs",
                        active_tab="dashboard-chart-tab",
                        children=[
                            dbc.Tab(
                                id="dashboard-chart-tab",
                                label="Charts",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=chart_contents
                            ),
                            dbc.Tab(
                                id="dashboard-info-tab",
                                label="Key Info",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[
                                    # dbc.Row([
                                    #     dbc.Col([
                                    #         dbc.Label("Key Summary Results", style=styles.key_summary_label_style)
                                    #     ], width="auto")
                                    # ], justify="center"),
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Slider(id='first-chart-slider', min=200, max=500, step=100, value=300,
                                                           #marks={x: str(x) for x in [200, 300, 400, 500]}),
                                                            marks={200:"Small", 300:"Medium", 400:"Large", 500:"Extra"}),
                                            dcc.Graph(id="first-pie-icl")
                                        ], width="4", style={"margin-top":"20px"}),
                                        dbc.Col([
                                            dcc.Slider(id='second-chart-slider', min=200, max=500, step=100, value=300,
                                                           #marks={x: str(x) for x in [200, 300, 400, 500]}),
                                                            marks={200:"Small", 300:"Medium", 400:"Large", 500:"Extra"}),
                                            dcc.Graph(id="second-pie-icl")
                                        ], width="4", style={"margin-top":"20px"}),
                                        dbc.Col([
                                            dcc.Slider(id='third-chart-slider', min=200, max=500, step=100, value=300,
                                                           #marks={x: str(x) for x in [200, 300, 400, 500]}),
                                                            marks={200:"Small", 300:"Medium", 400:"Large", 500:"Extra"}),
                                            dcc.Graph(id="third-pie-icl")
                                        ], width="4", style={"margin-top":"20px"}),
                                    ], justify="center"),
                                    dbc.Row([
                                        dbc.Col(id="key-summ-col",
                                                children=styles.label_no_data,
                                                width=6),
                                        dbc.Col(id="key-openings-col",
                                                children=styles.label_no_data,
                                                width=6),
                                    ],justify="center")
                                ]
                            ),
                            ],
                    ),
                    ], style={"padding-top":"10px"},
                )





                     #                                 dbc.Stack(
                     #                                     id='dashboard-drivers',
                     #                                     direction="horizontal",
                     #                                     gap=2,
                     #                                     children=[
                     #                                         dbc.Label("Summary type", style=styles.net_label_style),
                     #                                         dcc.Dropdown(
                     #                                             id="dashboards-options",
                     #                                             placeholder="Select Option ...",
                     #                                             persistence=True,
                     #                                             clearable=False,
                     #                                             options=["Insurance", "Reinsurance", "Net Position"],
                     #                                             value="Net Position",
                     #                                             style={
                     #                                                 "width": 200,
                     #                                                 # "height": "2px",
                     #                                                 "font-size": 12,
                     #                                                 "fontWeight": "normal",
                     #                                             }
                     #                                             # disabled=True,
                     #                                         ),
                     #                                     ]
                     #                                 ),
                     #                                 html.Hr(),
                     #                                 html.Details(
                     #                                     children=[
                     #                                         html.Summary("Main"),
                     #                                         html.Details(
                     #                                             children=[
                     #                                                 html.Summary("Secondary", style={'textIndent':'30px'}),
                     #                                                 dbc.Label("miai asmasfd"),
                     #                                                 dbc.Label("second")
                     #                                             ]
                     #                                         ),
                     #                                     ]
                     #                                 )
                     #                                 ],
                     # style={'padding-left': '1px', 'padding-top': '5px', 'display': 'inline-block'})

