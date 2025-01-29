import sys

sys.path.append("..")

import dash
from dash import dash_table, dcc, html, no_update
from dash.dependencies import Input, Output

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.ifrs17_paa.dash_utils as dash_utils
import cm_dashboards.ifrs17_paa.financial_position as financial_position
import cm_dashboards.ifrs17_paa.get_dropdown_data as get_dropdown_data
import cm_dashboards.ifrs17_paa.insurance_revenue as insurance_revenue
import cm_dashboards.ifrs17_paa.reconcile_icl as reconcile_icl
import cm_dashboards.ifrs17_paa.reconcile_pl as reconcile_pl
import cm_dashboards.utilities as utilities
from cm_dashboards.server import server

DB_ENGINE = None
DB_METADATA = None
WVR_PATH = None
Session = None


external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/dash.css"]


app = dash.Dash(
    name="ifrs17paa",
    server=server,
    url_base_pathname="/dash/ifrs17_paa/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    compress=server.config["COMPRESS_CONTENT"],
)

# Change the default favicon
app.index_string = custom_html_template.WM_TEMPLATE

# Enable dev mode if turned on in config
debug_mode = utilities.get_entry_from_config_file("dashboard", "debug_mode", False)
if debug_mode == "True":
    app.config.suppress_callback_exceptions = True
    app.enable_dev_tools(debug=True, dev_tools_ui=True, dev_tools_props_check=True)

# Datatable shared default style settings
style_data_conditional = [
    {
        "if": {
            "filter_query": "{format_hidden} = 1",
        },
        "backgroundColor": "rgb(217, 250, 207)",
    },
    {
        "if": {"column_id": "Category"},
        "border-right": "1px solid grey",
        "textAlign": "center",
        "backgroundColor": "white",
    },
]
style_header = (
    {
        "backgroundColor": "light grey",
        "fontSize": "14px",
        "fontWeight": "bold",
        "textAlign": "center",
        "border": "1px solid black",
        "border-right": "0px",
    },
)

# HTML layout

app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.H2(children="R3S Cloud Manager"),
        dcc.Input(
            id="confirmed-wvr-path",
            value="",
            placeholder="C:\\temp\\results.wvr",
            style={"width": "50%"},
            type="hidden",
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="two columns",
                    children=[
                        html.Label("Onerous Type"),
                        dcc.Dropdown(
                            id="grp_onerous_type_dd",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    className="two columns",
                    children=[
                        html.Label("Inception Year"),
                        dcc.Dropdown(
                            id="inception_year_dd",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    className="two columns",
                    children=[
                        html.Label("Model"),
                        dcc.Dropdown(
                            id="model_dd",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    className="two columns",
                    children=[
                        html.Label("Product"),
                        dcc.Dropdown(
                            id="product_dd",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    className="two columns",
                    children=[
                        html.Label("Step Date"),
                        dcc.Dropdown(
                            id="step_date_dd",
                            clearable=False,
                        ),
                    ],
                ),
            ],
        ),
        html.H3(children="Liability Contracts"),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="one-half column",
                    children=[
                        html.Label("Reconciliation of the insurance contract liability (full)"),
                        dash_table.DataTable(
                            id="reconcile-icl-table",
                            css=[
                                {
                                    "selector": ".show-hide",
                                    "rule": "display: none",
                                }
                            ],
                            style_cell={"border": "0px", "minWidth": "150px"},
                            style_header_conditional=style_header,
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="one-half column",
                    children=[
                        html.Label("Reconciliation of financial position and profit or loss"),
                        dash_table.DataTable(
                            id="reconcile-pl-table",
                            css=[
                                {
                                    "selector": ".show-hide",
                                    "rule": "display: none",
                                }
                            ],
                            style_cell={"border": "0px", "minWidth": "150px"},
                            style_header_conditional=style_header,
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="one-half column",
                    children=[
                        html.Label("Insurance Revenue"),
                        dash_table.DataTable(
                            id="insurance-revenue-table",
                            css=[
                                {
                                    "selector": ".show-hide",
                                    "rule": "display: none",
                                }
                            ],
                            style_cell={"border": "0px", "minWidth": "150px"},
                            style_header_conditional=style_header,
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="one-half column",
                    children=[
                        html.Label("Statement of Financial Position"),
                        dash_table.DataTable(
                            id="financial-position-table",
                            css=[
                                {
                                    "selector": ".show-hide",
                                    "rule": "display: none",
                                }
                            ],
                            style_cell={"border": "0px", "minWidth": "150px"},
                            style_header_conditional=style_header,
                        ),
                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("confirmed-wvr-path", "value"),
    [Input("url", "search")],
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    """
    global WVR_PATH
    if input_url:
        WVR_PATH = utilities.get_wvr_path_from_url(input_url)
    return WVR_PATH


@app.callback(
    [
        Output("grp_onerous_type_dd", "options"),
        Output("grp_onerous_type_dd", "value"),
        Output("inception_year_dd", "options"),
        Output("inception_year_dd", "value"),
        Output("model_dd", "options"),
        Output("model_dd", "value"),
        Output("product_dd", "options"),
        Output("product_dd", "value"),
        Output("step_date_dd", "options"),
        Output("step_date_dd", "value"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def get_dropdown_values(input_url):
    """
    Get dropdown values
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )
    grp_onerous_type_list = get_dropdown_data.get_dropdown_list_data(WVR_PATH, "IFRS_17_PAA", "Grp_Onerous_Type Value")

    inception_year_list = get_dropdown_data.get_dropdown_list_data(WVR_PATH, "IFRS_17_PAA", "Inception_Year Value")

    model_list = get_dropdown_data.get_dropdown_list_data(WVR_PATH, "IFRS_17_PAA", "Model Value")

    product_name_list = get_dropdown_data.get_dropdown_list_data(WVR_PATH, "IFRS_17_PAA", "Product_Name Value")
    step_date_list = get_dropdown_data.get_dropdown_list_data(WVR_PATH, "IFRS_17_PAA", "Step Date")

    return (
        grp_onerous_type_list,
        grp_onerous_type_list[0],
        inception_year_list,
        inception_year_list[0],
        model_list,
        model_list[0],
        product_name_list,
        product_name_list[0],
        step_date_list,
        step_date_list[0],
    )


### Charts ###


@app.callback(
    [
        Output("reconcile-icl-table", "data"),
        Output("reconcile-icl-table", "columns"),
        Output("reconcile-pl-table", "data"),
        Output("reconcile-pl-table", "columns"),
        Output("insurance-revenue-table", "data"),
        Output("insurance-revenue-table", "columns"),
        Output("financial-position-table", "data"),
        Output("financial-position-table", "columns"),
    ],
    [
        Input("grp_onerous_type_dd", "value"),
        Input("inception_year_dd", "value"),
        Input("model_dd", "value"),
        Input("product_dd", "value"),
        Input("step_date_dd", "value"),
    ],
)
def prepare_claim_costs_results(onerous_type, inception_year, model, product, step_date):
    """
    Claim Costs Results
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update

    reconcile_icl_df = reconcile_icl.get_data_from_wvr(
        WVR_PATH,
        "IFRS_17_PAA",
        "G_Portfolio",
        onerous_type,
        inception_year,
        model,
        product,
        step_date,
    )

    icl_table_data = reconcile_icl_df.to_dict("records")
    icl_columns = dash_utils.set_column_names(reconcile_icl_df.columns)

    pl_table_data, pl_columns = reconcile_pl.reconcile_pl_table(reconcile_icl_df)

    insurance_revenue_df = insurance_revenue.insurance_revenue_table(reconcile_icl_df)
    acquisition_cash_flows = insurance_revenue.get_data_from_wvr(
        WVR_PATH,
        "IFRS_17_PAA",
        "G_Portfolio",
        onerous_type,
        inception_year,
        model,
        product,
        step_date,
    )
    insurance_revenue_df.loc["Insurance acquisition cash flows"] = [
        "Insurance acquisition cash flows",
        acquisition_cash_flows,
    ]
    ir_table_data = insurance_revenue_df.to_dict("records")
    ir_columns = dash_utils.set_column_names(insurance_revenue_df.columns)

    financial_position_df = financial_position.get_data_from_wvr(
        WVR_PATH,
        "IFRS_17_PAA",
        "G_Portfolio",
        onerous_type,
        inception_year,
        model,
        product,
        step_date,
    )

    fp_table_data = financial_position_df.to_dict("records")
    fp_columns = dash_utils.set_column_names(financial_position_df.columns)

    return (
        icl_table_data,
        icl_columns,
        pl_table_data,
        pl_columns,
        ir_table_data,
        ir_columns,
        fp_table_data,
        fp_columns,
    )
