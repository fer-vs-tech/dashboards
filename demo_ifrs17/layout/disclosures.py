#ifrs17/layout/disclosures.py

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
import cm_dashboards.demo_ifrs17.layout.component_styles as styles

menu = dbc.Tabs(
                        id="disclosure-options-tabs",
                        active_tab="ins-bba-vfa-tab",
                        children=[
                            dbc.Tab(
                                id="disclosure-ins-bba-vfa-tab",
                                label="Ins_BBA.VFA",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                #disabled=True,
                                children=[styles.label_no_data]
                            ),
                            dbc.Tab(
                                id="disclosure-reins-bba-tab",
                                label="Reins_BBA",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                #disabled=True,
                                children=[styles.label_no_data]
                            ),
                            dbc.Tab(
                                id="disclosure-ins-paa-tab",
                                label="Ins_PAA",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                #disabled=True,
                                children=[styles.label_no_data]
                            ),
                            dbc.Tab(
                                id="disclosure-reins-paa-tab",
                                label="Reins_PAA",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                #disabled=True,
                                #children=[html.Hr(), accordion_menu_reins]
                                children=[styles.label_no_data]
                            ),
                            dbc.Tab(
                                id="disclosure-net-all-tab",
                                label="Net All",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                # children=[html.Hr(), accordion_menu_reins]
                                children=[styles.label_no_data]
                            ),

                ],
    style={'margin-top':'10px'}
            )