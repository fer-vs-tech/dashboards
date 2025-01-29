#ifrs17/layout/modal_filters.py

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
import cm_dashboards.demo_ifrs17.layout.component_styles as styles

filters = dbc.Modal(
    [
        dbc.ModalHeader(
            dbc.Label("Filters", style=styles.label_style_title),
            #"Filters",
            close_button=False,
        ),
        dbc.ModalBody(
            id="modal-body",
            children=[
                    html.Div([
                        dcc.Loading(
                            type="dot",
                            color="#2741BC",
                            children=[
                        dash_table.DataTable(
                              id='params-goc-table',
                              style_table={
                                  'overflowY': 'scroll',
                                  'height': 500,
                              },
                              style_data_conditional = [{'textAlign':'center'}],
                            css=[
                                {
                                    "selector":
                                        ".dash-spreadsheet-container .Select-value-label",
                                    "rule": "color: #2741BC"
                                },
                                {
                                    "selector": ".dash-spreadsheet .Select-option",
                                    "rule": "color: #2741BC",
                                },
                            ],
                              page_size=10,
                              fixed_rows={'headers': True, 'data': 0},
                              #editable=True,
                            ),
                        ]),
                        ])
                  ]
        ),
        dbc.ModalFooter(
            [
            dbc.Button(
                "Apply",
                id="apply-filters",
                n_clicks=0,
                outline=True, color="primary",
            )
            ]
        ),
    ],
    id="modal-filters",
    backdrop='static',
    keyboard=False,
    centered=True,
    is_open=False,
)