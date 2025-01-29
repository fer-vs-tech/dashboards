import sys

sys.path.append("..")


import dash
import dash_bootstrap_components as dbc
import plotly.io as pio
from dash import dash_table, dcc, html, no_update
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.nonlife_standalone.parameterization as parameterization
import cm_dashboards.utilities as utilities
from cm_dashboards.server import server

DB_ENGINE = None
DB_METADATA = None
WVR_PATH = None
Session = None
pio.templates.default = "plotly_white"

templates = [
    "bootstrap",
    "cerulean",
    "cosmo",
    "flatly",
    "journal",
    "litera",
    "lumen",
    "lux",
    "materia",
    "minty",
    "pulse",
    "sandstone",
    "simplex",
    "sketchy",
    "spacelab",
    "united",
    "yeti",
    "cyborg",
    "darkly",
    "slate",
    "solar",
    "superhero",
    "morph",
    "quartz",
    "vapor",
    "zephyr",
]
load_figure_template(templates)

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
)
external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc_css, "../static/css/styles.css"]


app = dash.Dash(
    name="nonlife_solo_beta",
    server=server,
    eager_loading=True,
    url_base_pathname="/dash/nonlife_solo_beta/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    prevent_initial_callbacks=True,
    compress=server.config["COMPRESS_CONTENT"],
)

# Change the default favicon
app.index_string = custom_html_template.WM_TEMPLATE

# Enable dev mode if turned on in config
debug_mode = utilities.get_entry_from_config_file("dashboard", "debug_mode", False)
if debug_mode == "True":
    app.config.suppress_callback_exceptions = True
    app.enable_dev_tools(debug=True, dev_tools_ui=True, dev_tools_props_check=True)

# HTML layout

app.layout = dbc.Container(
    fluid="md",
    className="dbc",
    children=[
        dcc.Location(id="url", refresh=False),
        html.Div(
            style={"display": "inline-block", "font-size": "30px", "margin": "10px"},
            className="p-4 mb-2 text-left",
            children=[
                html.Img(
                    style={"height": "20%", "width": "20%"},
                    src="/dash/static/assets/wm_logo.svg",
                ),
                html.H1("R3S Cloud Manager"),
                html.H2("Assumption (NLSC) Validation results"),
            ],
        ),
        html.Br(),
        dcc.Input(
            id="confirmed-wvr-path",
            value="",
            placeholder="C:\\temp\\results.wvr",
            style={"width": "50%", "display": "none"},
        ),
        html.Div(
            className="row",
            children=[
                # html.Div(
                #     className="one-half column",
                #     children=[
                #         dcc.Graph(config={"displaylogo": False}, id="claims-data-loss-ratio-chart"),
                #         html.Label("Claims Data and Loss Ratio"),
                #         dash_table.DataTable(id="claims-data-loss-ratio-table"),
                #     ],
                # ),
                # html.Div(
                #     className="one-half column",
                #     children=[
                #         dcc.Graph(config={"displaylogo": False}, id="loss-ratio-chart"),
                #         html.Label("Loss Ratio"),
                #         dash_table.DataTable(id="loss-ratio-table"),
                #     ],
                # ),
                html.Div(
                    className="one-half column",
                    children=[
                        html.Label("Parameterization table"),
                        dash_table.DataTable(
                            id="parameterization-table", merge_duplicate_headers=True
                        ),
                    ],
                ),
            ],
        ),
    ],
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


# # Claims Data and Loss Ratio chart
# @app.callback(
#     [
#         Output("claims-data-loss-ratio-chart", "figure"),
#         Output("claims-data-loss-ratio-table", "data"),
#         Output("claims-data-loss-ratio-table", "columns"),
#     ],
#     [Input("confirmed-wvr-path", "value")],
# )
# def update_figure(n_clicks):
#     """
#     Claims Data and Loss Ratio chart
#     """
#     if WVR_PATH is None or WVR_PATH == "":
#         return no_update, no_update, no_update
#     return claims_data_loss_ratio.get_chart(
#         WVR_PATH,
#         "Claims Data and Loss Ratio chart",
#     )

# # Loss Ratio chart
# @app.callback(
#     [
#         Output("loss-ratio-chart", "figure"),
#         Output("loss-ratio-table", "data"),
#         Output("loss-ratio-table", "columns"),
#     ],
#     [Input("confirmed-wvr-path", "value")],
# )
# def update_figure(n_clicks):
#     """
#     Claims Data and Loss Ratio chart
#     """
#     if WVR_PATH is None or WVR_PATH == "":
#         return no_update, no_update, no_update
#     return loss_ratio.get_chart(
#         WVR_PATH,
#         "Claims Data and Loss Ratio chart",
#     )


# Parameterization table
@app.callback(
    [
        Output("parameterization-table", "data"),
        Output("parameterization-table", "columns"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Parameterization table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update
    return parameterization.get_table(
        WVR_PATH,
        "Parameterization table",
    )
