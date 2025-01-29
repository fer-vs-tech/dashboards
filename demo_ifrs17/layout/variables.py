#ifrs17/layout/variables.py

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
import cm_dashboards.demo_ifrs17.layout.component_styles as styles


menu = dbc.Tabs(
                        id="variable-options-tabs",
                        active_tab="bba-tab",
                        children=[
                            dbc.Tab(
                                id="bba-tab",
                                label="BBA Variables",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[
                                    html.Hr(),
                                    dash_table.DataTable(id="table-r3s-bba-variables"),
                                ]
                            ),
                            dbc.Tab(
                                id="paa-tab",
                                label="PAA Variables",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[
                                    html.Hr(),
                                    dash_table.DataTable(id="table-r3s-paa-variables"),
                                ]
                            ),
                        ],
    style={'margin-top': '10px'}
)
