#ifrs17/layout/subledger.py

import dash_bootstrap_components as dbc
from dash import dash_table, dcc
import cm_dashboards.demo_ifrs17.layout.component_styles as styles

drivers = dbc.Stack(id = "subledger-drivers",
                                direction="horizontal",
                                gap = 1,
                                children=[
                                dbc.Label("Group of Contracts", style=styles.net_label_style),
                                dcc.Dropdown(
                                    id="subledger-groups",
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
                                ),
                                    dbc.Label("Primary / Secondary", style=styles.net_label_style),
                                    dcc.Dropdown(
                                        id="subledger-primary",
                                        placeholder="Select type ...",
                                        persistence=True,
                                        clearable=False,
                                        options=["New Business", "Premium", "Revenue (PAA)", "Revenue (Claims)", "Revenue (Expenses)",
                                                 "Incurred", "Financial", "Past Services", "Non-Performance Risk", "Future Services",
                                                 "Loss Reversals", "Investment Component", "DAC", "OCI"],
                                        value="New Business",
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

results = dash_table.DataTable(
    id='subledger-table',
    style_table={
        'overflowY': 'auto',
        'height': 600
    },
    style_data_conditional=styles.subledger_cond_style
)