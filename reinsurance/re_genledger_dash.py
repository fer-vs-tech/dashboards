"""
@author: graham.howarth
"""

import dash
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign
from dash.dependencies import Input, Output

from cm_dashboards.reinsurance import re_genledger_handler as gl
from cm_dashboards.server import server

external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/dash.css", "../static/css/tab_styles.css"]

JOBRUN = "1"

app = dash.Dash(
    name="reGenledger",
    server=server,
    url_base_pathname="/dash/regenledger/",
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    compress=server.config["COMPRESS_CONTENT"],
)

# Datatable shared default style settings
style_data_conditional = [
    {
        "if": {
            "filter_query": "{format_hidden} = 1",
        },
        "backgroundColor": "rgb(217, 250, 207)",
    },
    {
        "if": {"column_id": "Group"},
        "border-right": "1px solid grey",
        "textAlign": "center",
        "backgroundColor": "white",
    },
]
style_header = (
    {
        "backgroundColor": "rgb(156, 156, 156)",
        "fontSize": "14px",
        "fontWeight": "bold",
        "border": "1px solid black",
        "border-right": "0px",
    },
)

app.layout = html.Div(
    children=[
        html.H1(children="R3S Cloud Manager", style={"color": "darkblue"}),
        # represents the URL bar, doesn't render anything
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                dcc.Input(id="jobrun", value="", type="hidden"),
            ]
        ),  # type="hidden"
        html.H2(children="Reinsurance General ledger", style={"color": "darkblue"}),
        html.Br(),
        dash_table.DataTable(
            id="generalLedger",
            export_format="xlsx",
            export_columns="visible",
            css=[
                {
                    "selector": ".show-hide",
                    "rule": "display: none",
                }
            ],
            style_cell={"border": "0px"},
            style_data_conditional=style_data_conditional,
            style_header=style_header,
        ),
    ],
)


@app.callback(
    Output("jobrun", "value"),
    [dash.dependencies.Input("url", "search")],
)
def update_jobrun(input_jobrun):
    """
    Update the jobrun
    """
    global JOBRUN
    if input_jobrun:
        # TODO: Improve this
        JOBRUN = input_jobrun.split("?jobrun=")[1]
    return JOBRUN


@app.callback(
    [
        Output("generalLedger", "columns"),
        Output("generalLedger", "data"),
        Output("generalLedger", "style_cell_conditional"),
        Output("generalLedger", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def general_ledger_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = gl.ReGenLedgerHandler()
    pop_template = handler.get_combined_ledger(JOBRUN)

    # Convert datatable into dictionary for display
    out_table = pop_template.to_dict("records")
    column_names = set_column_names(pop_template.columns)
    hidden_cols = pop_template.filter(regex="_hidden$").columns.tolist()
    style_cell_conditional = set_column_styles(pop_template.columns, hidden_cols)

    return column_names, out_table, style_cell_conditional, hidden_cols


def set_column_names(columns):
    """
    Apply the column names for the table
    """
    column_names = [
        {
            "name": i,
            "id": i,
            "type": "numeric",
            "format": Format(group=",", precision=0, scheme=Scheme.fixed, sign=Sign.parantheses),
        }
        for i in columns
    ]
    return column_names


def set_column_styles(columns, hidden_cols):
    """
    Set styling for columns and handle hidden columns
    """
    style_cell_conditional = (
        [{"if": {"column_id": c}, "textAlign": "left"} for c in columns.tolist()]
        + [
            {
                "if": {"column_id": "Description"},
                "border-right": "1px solid grey",
                "textAlign": "center",
            }
        ]
        + [{"if": {"column_id": c}, "display": "None", "hidden": "True"} for c in hidden_cols]
        + [
            {
                "if": {
                    "filter_query": "{bottom_border_hidden} = 1",
                },
                "border-bottom": "1px solid grey",
            },
            {
                "if": {"column_id": "Group"},
                "border-bottom": "0px",
            },
            {
                "if": {
                    "filter_query": "{bottom_border_hidden} = 2",
                },
                "border-bottom": "4px double grey",
            },
        ]
    )

    return style_cell_conditional
