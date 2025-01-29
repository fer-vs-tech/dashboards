"""
@author: graham.howarth
"""

import dash
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign
from dash.dependencies import Input, Output

import cm_dashboards.utilities as utilities
from cm_dashboards.nonlife_standalone.nonlife_solo import WVR_PATH
from cm_dashboards.other_accounting import vfa_csm_handler as vc
from cm_dashboards.other_accounting import vfa_ir_handler as vi
from cm_dashboards.other_accounting import vfa_sm_handler as vs
from cm_dashboards.server import server

external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/dash.css", "../static/css/tab_styles.css"]

JOBRUN = "1"
WVR_PATH = None

app = dash.Dash(
    name="vfa",
    server=server,
    url_base_pathname="/dash/vfa/",
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    compress=server.config["COMPRESS_CONTENT"],
)

# Datatable shared default style settings
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
        html.H2(children="IFRS17 VFA IR Subledger", style={"color": "darkblue"}),
        html.Br(),
        dash_table.DataTable(
            id="vfa_ir",
            export_format="xlsx",
            export_columns="visible",
            css=[
                {
                    "selector": ".show-hide",
                    "rule": "display: none",
                }
            ],
            style_cell={"border": "0px"},
            style_header_conditional=style_header,
        ),
        html.Br(),
        html.H2(children="IFRS17 VFA SM Subledger", style={"color": "darkblue"}),
        html.Br(),
        dash_table.DataTable(
            id="vfa_sm",
            export_format="xlsx",
            export_columns="visible",
            css=[
                {
                    "selector": ".show-hide",
                    "rule": "display: none",
                }
            ],
            style_cell={"border": "0px"},
            style_header_conditional=style_header,
        ),
        html.Br(),
        html.H2(children="IFRS17 VFA CSM Subledger", style={"color": "darkblue"}),
        html.Br(),
        dash_table.DataTable(
            id="vfa_csm",
            export_format="xlsx",
            export_columns="visible",
            css=[
                {
                    "selector": ".show-hide",
                    "rule": "display: none",
                }
            ],
            style_cell={"border": "0px"},
            style_header_conditional=style_header,
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
    global WVR_PATH
    if input_jobrun:
        JOBRUN = utilities.get_jobrun_from_url(input_jobrun)
        WVR_PATH = utilities.get_wvr_path_from_url(input_jobrun)
    return JOBRUN


@app.callback(
    [
        Output("vfa_ir", "columns"),
        Output("vfa_ir", "data"),
        Output("vfa_ir", "style_data_conditional"),
        Output("vfa_ir", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def vfa_ir_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = vi.VfaIrHandler()
    handler.prepare_data_wvr(WVR_PATH, "IFRS17_VFA_IR_Proc")
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
        Output("vfa_sm", "columns"),
        Output("vfa_sm", "data"),
        Output("vfa_sm", "style_data_conditional"),
        Output("vfa_sm", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def vfa_sm_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = vs.VfaSmHandler()
    handler.prepare_data_wvr(WVR_PATH, "IFRS17_VFA_SM_Proc")
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
        Output("vfa_csm", "columns"),
        Output("vfa_csm", "data"),
        Output("vfa_csm", "style_data_conditional"),
        Output("vfa_csm", "hidden_columns"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def vfa_csm_callback(input_value):
    """
    Update the table listing database schemas
    """
    handler = vc.VfaCsmHandler()
    handler.prepare_data_wvr(WVR_PATH, "IFRS17_VFA_CSM_AMOR_Proc")
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
                "textAlign": "right",
            },
            {
                "if": {"column_id": "Description"},
                "border-right": "1px solid grey",
                "textAlign": "center",
            },
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
                "if": {
                    "filter_query": "{format_hidden} = 1",
                },
                "backgroundColor": "rgb(217, 250, 207)",
            },
            {
                "if": {"column_id": "Group"},
                "display": "None",
                "hidden": "True",
            },
        ]
    )
    return style_cell_conditional
