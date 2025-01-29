"""
@author: graham.howarth
"""
import dash
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign
from dash.dependencies import Input, Output

from cm_dashboards.reinsurance import aoci_handler as aoci
from cm_dashboards.reinsurance import csm_handler as csm
from cm_dashboards.reinsurance import rqa_handler as rqa
from cm_dashboards.reinsurance import rqp_handler as rqp
from cm_dashboards.reinsurance import rwa_handler as rwa
from cm_dashboards.reinsurance import rwu_handler as rwu
from cm_dashboards.server import server

external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/dash.css", "../static/css/tab_styles.css"]

JOBRUN = "1"

app = dash.Dash(
    name="re_subledger",
    server=server,
    url_base_pathname="/dash/reinsurance/",
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
    }
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

# image_filename = "static/logo.png"
# encoded_image = base64.b64encode(open(image_filename, "rb").read())

app.layout = html.Div(
    children=[
        # html.Div(
        #    [html.Img(src="data:image/png;base64,{}".format(encoded_image.decode()))]
        # ),
        html.H1(children="R3S Cloud Manager", style={"color": "darkblue"}),
        # represents the URL bar, doesn't render anything
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                dcc.Input(id="jobrun", value="", type="hidden"),
            ]
        ),  # type="hidden"
        html.H2(children="Reinsurance Subledger", style={"color": "darkblue"}),
        html.Br(),
        dcc.Tabs(
            parent_className="custom-tabs",
            className="custom-tabs-container",
            children=[
                dcc.Tab(
                    label="RWA Subledger",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children=[
                        dash_table.DataTable(
                            id="rwaSubledger",
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
                ),
                dcc.Tab(
                    label="RWU Subledger",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children=[
                        dash_table.DataTable(
                            id="rwuSubledger",
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
                ),
                dcc.Tab(
                    label="RQP Subledger",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children=[
                        dash_table.DataTable(
                            id="rqpSubledger",
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
                ),
                dcc.Tab(
                    label="RQA Subledger",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children=[
                        dash_table.DataTable(
                            id="rqaSubledger",
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
                ),
                dcc.Tab(
                    label="CSM Subledger",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children=[
                        dash_table.DataTable(
                            id="csmSubledger",
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
                ),
                dcc.Tab(
                    label="AOCI Subledger",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                    children=[
                        dash_table.DataTable(
                            id="aociSubledger",
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
                ),
            ],
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
        Output("rwaSubledger", "columns"),
        Output("rwaSubledger", "data"),
        Output("rwaSubledger", "style_cell_conditional"),
        Output("rwaSubledger", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def rwa_subledger_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = rwa.RwaHandler()
    # Get data from database, rotate and format
    handler.prepare_data(JOBRUN)
    # Apply data to subledger template file
    pop_template = handler.subledger_apply_template()

    # Convert datatable into dictionary for display
    out_table = pop_template.to_dict("records")
    column_names = set_column_names(pop_template.columns)
    hidden_cols = pop_template.filter(regex="_hidden$").columns.tolist()
    style_cell_conditional = set_column_styles(pop_template.columns, hidden_cols)

    return column_names, out_table, style_cell_conditional, hidden_cols


@app.callback(
    [
        Output("rwuSubledger", "columns"),
        Output("rwuSubledger", "data"),
        Output("rwuSubledger", "style_cell_conditional"),
        Output("rwuSubledger", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def rwu_subledger_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = rwu.RwuHandler()
    # Get data from database, rotate and format
    handler.prepare_data(JOBRUN)
    # Apply data to subledger template file
    pop_template = handler.subledger_apply_template()

    # Convert datatable into dictionary for display
    out_table = pop_template.to_dict("records")
    column_names = set_column_names(pop_template.columns)
    hidden_cols = pop_template.filter(regex="_hidden$").columns.tolist()
    style_cell_conditional = set_column_styles(pop_template.columns, hidden_cols)

    return column_names, out_table, style_cell_conditional, hidden_cols


@app.callback(
    [
        Output("rqpSubledger", "columns"),
        Output("rqpSubledger", "data"),
        Output("rqpSubledger", "style_cell_conditional"),
        Output("rqpSubledger", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def rdp_subledger_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = rqp.RqpHandler()
    # Get data from database, rotate and format
    handler.prepare_data(JOBRUN)
    # Apply data to subledger template file
    pop_template = handler.subledger_apply_template()

    # Convert datatable into dictionary for display
    out_table = pop_template.to_dict("records")
    column_names = set_column_names(pop_template.columns)
    hidden_cols = pop_template.filter(regex="_hidden$").columns.tolist()
    style_cell_conditional = set_column_styles(pop_template.columns, hidden_cols)

    return column_names, out_table, style_cell_conditional, hidden_cols


@app.callback(
    [
        Output("rqaSubledger", "columns"),
        Output("rqaSubledger", "data"),
        Output("rqaSubledger", "style_cell_conditional"),
        Output("rqaSubledger", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def rqa_subledger_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = rqa.RqaHandler()
    # Get data from database, rotate and format
    handler.prepare_data(JOBRUN)
    # Apply data to subledger template file
    pop_template = handler.subledger_apply_template()

    # Convert datatable into dictionary for display
    out_table = pop_template.to_dict("records")
    column_names = set_column_names(pop_template.columns)
    hidden_cols = pop_template.filter(regex="_hidden$").columns.tolist()
    style_cell_conditional = set_column_styles(pop_template.columns, hidden_cols)

    return column_names, out_table, style_cell_conditional, hidden_cols


@app.callback(
    [
        Output("csmSubledger", "columns"),
        Output("csmSubledger", "data"),
        Output("csmSubledger", "style_cell_conditional"),
        Output("csmSubledger", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def csm_subledger_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = csm.CsmHandler()
    # Get data from database, rotate and format
    handler.prepare_data(JOBRUN)
    # Apply data to subledger template file
    pop_template = handler.subledger_apply_template()

    # Convert datatable into dictionary for display
    out_table = pop_template.to_dict("records")
    column_names = set_column_names(pop_template.columns)
    hidden_cols = pop_template.filter(regex="_hidden$").columns.tolist()
    style_cell_conditional = set_column_styles(pop_template.columns, hidden_cols)

    return column_names, out_table, style_cell_conditional, hidden_cols


@app.callback(
    [
        Output("aociSubledger", "columns"),
        Output("aociSubledger", "data"),
        Output("aociSubledger", "style_cell_conditional"),
        Output("aociSubledger", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def aoci_subledger_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = aoci.AociHandler()
    # Get data from database, rotate and format
    handler.prepare_data(JOBRUN)
    # Apply data to subledger template file
    pop_template = handler.subledger_apply_template()

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
            "format": Format(
                group=",", precision=0, scheme=Scheme.fixed, sign=Sign.parantheses
            ),
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
        + [
            {"if": {"column_id": c}, "display": "None", "hidden": "True"}
            for c in hidden_cols
        ]
        + [
            {
                "if": {
                    "filter_query": "{bottom_border_hidden} = 1",
                },
                "border-bottom": "1px solid grey",
            },
            {
                "if": {"column_id": "Group"},
                "display": "None",
                "hidden": "True",
            },
        ]
    )

    return style_cell_conditional
