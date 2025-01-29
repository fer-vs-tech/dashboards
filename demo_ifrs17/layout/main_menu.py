#ifrs17/layout/main_menu.py

import dash_bootstrap_components as dbc
from dash import html
import cm_dashboards.demo_ifrs17.layout.dashboards as dashboards
import cm_dashboards.demo_ifrs17.layout.disclosures as disclosures
import cm_dashboards.demo_ifrs17.layout.breakdowns as breakdowns
import cm_dashboards.demo_ifrs17.layout.variables as variables
import cm_dashboards.demo_ifrs17.layout.bs_summary as bs_summary
import cm_dashboards.demo_ifrs17.layout.subledger as subledger

main =  dbc.Tabs(
                        id="menu-tabs",
                        #active_tab="dashboard-tab",
                        children=[
                            dbc.Tab(
                                id="dashboard-tab",
                                label="Dashboard",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                #disabled=True,
                                children=[
                                    dashboards.menu
                                ]
                            ),
                            dbc.Tab(
                                id="variables-tab",
                                label="R3S Output",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                #disabled=True,
                                children=[
                                    variables.menu,
                                ]
                            ),
                            dbc.Tab(
                                id="breakdown-main-tab",
                                label="Breakdowns",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[
                                    breakdowns.menu
                                ]
                            ),
                            dbc.Tab(
                                id="summary-bs-tab",
                                label="BS Summary",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                #disabled=True,
                                children=[
                                    html.Hr(),
                                    dbc.Row([
                                        dbc.Col([
                                            bs_summary.drivers,
                                            bs_summary.results
                                        ]),
                                    ]),
                                ]
                            ),
                            dbc.Tab(
                                id="disclosures-main-tab",
                                label="Disclosures",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                # disabled=True,
                                children=[
                                    #html.Hr(),
                                    disclosures.menu
                                ]
                            ),
                            dbc.Tab(
                                id="subledger-logic-tab",
                                label="Subledger Logic",
                                tab_class_name="unactive-tab",
                                label_class_name="unactive-tab-label",
                                active_tab_class_name="active-tab",
                                active_label_class_name="active-tab-label",
                                #disabled=True,
                                children=[
                                    subledger.drivers,
                                    subledger.results
                                ]
                            ),
                ],
            )