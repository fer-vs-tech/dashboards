#ifrs17/layout/bs_summary.py

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
import cm_dashboards.demo_ifrs17.layout.component_styles as styles

drivers = dbc.Stack(id = "summary-drivers",
                                direction="horizontal",
                                gap = 1,
                                children=[
                                    dbc.Label("Summary type", style=styles.net_label_style),
                                    dcc.Dropdown(
                                    id="summary-options",
                                    placeholder="Select Option ...",
                                    persistence=True,
                                    clearable=False,
                                    options=["Insurance Only", "Reinsurance Only", "Net Position"],
                                    value="Net Position",
                                    style={
                                        "width": 200,
                                        # "height": "2px",
                                        "font-size": 12,
                                        "fontWeight": "normal",
                                    }
                                    # disabled=True,
                                ),
                                dbc.Label("Group of Contracts", style=styles.net_label_style),
                                dcc.Dropdown(
                                    id="summary-groups",
                                    placeholder="Select Group ...",
                                    persistence=True,
                                    clearable=False,
                                    options=["Aggregated All"],
                                    value="Aggregated All",
                                    style={
                                        "width": 400,
                                        # "height": "2px",
                                        "font-size": 12,
                                        "fontWeight": "normal",
                                    }
                                    # disabled=True,
                                )
                               ]
                           )

results = html.Div(id="summary-bs-container", children=[styles.label_no_data])