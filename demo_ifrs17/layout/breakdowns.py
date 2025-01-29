#ifrs17/layout/breakdowns.py

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
import cm_dashboards.demo_ifrs17.layout.component_styles as styles


menu = dbc.Tabs(
                        id="breakdown-options-tabs",
                        active_tab="BS-Ins-BBA-VFA-tab",
                        children=[
                            dbc.Tab(
                                id="BS-Ins-BBA-VFA-tab",
                                label="BS_Ins_BBA.VFA",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[styles.label_no_data]
                            ),
                            dbc.Tab(
                                id="BS-Reins-BBA-tab",
                                label="BS_Reins_BBA",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[styles.label_no_data]
                            ),
                            dbc.Tab(
                                id="BS-Ins-PAA-tab",
                                label="BS_Ins_PAA",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[styles.label_no_data]
                            ),
                            dbc.Tab(
                                id="BS-Reins-PAA-tab",
                                label="BS_Reins_PAA",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[styles.label_no_data]
                            )
                        ],
    style={'margin-top': '10px'}
)