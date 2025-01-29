import sys

sys.path.append("..")

import dash
import dash_bootstrap_components as dbc
import plotly.io as plt_io
from dash import dash_table, dcc, html, no_update
from dash.dependencies import Input, Output

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.nonlife_standalone.box_plot_outliers as box_plot_outliers
import cm_dashboards.nonlife_standalone.claim_costs_results as claim_costs_results
import cm_dashboards.nonlife_standalone.claim_costs_summary as claim_costs_summary
import cm_dashboards.nonlife_standalone.cumulative_incurred_claims_projected as cumulative_incurred_claims_projected
import cm_dashboards.nonlife_standalone.development_factors_chart as development_factors_chart
import cm_dashboards.nonlife_standalone.generic_lic_line_chart as generic_lic_line_chart
import cm_dashboards.nonlife_standalone.incremental_incurred_claims_projected as incremental_incurred_claims_projected
import cm_dashboards.nonlife_standalone.lic_inc_paid_claims_chart as inc_paid_claims
import cm_dashboards.nonlife_standalone.link_ratios_post_data_analysis as link_ratios_post_data_analysis
import cm_dashboards.nonlife_standalone.link_ratios_post_outlier_analysis as link_ratios_post_outlier_analysis
import cm_dashboards.nonlife_standalone.link_ratios_pre_outlier_chart as link_ratios_pre_outlier_chart
import cm_dashboards.nonlife_standalone.lrc_evaluate_table as lrc_evaluate_table
import cm_dashboards.nonlife_standalone.outlier_analysis_pvalue as outlier_analysis_pvalue
import cm_dashboards.nonlife_standalone.outlieranalysis_mean_ratios as outlieranalysis_mean_ratios
import cm_dashboards.nonlife_standalone.parameterization as parameterization
import cm_dashboards.nonlife_standalone.ultimate_development_factors as ultimate_development_factors
import cm_dashboards.utilities as utilities
from cm_dashboards.custom_template import custom_template
from cm_dashboards.server import server

DB_ENGINE = None
DB_METADATA = None
WVR_PATH = None
Session = None

# External scripts and CSS stylesheets
external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/bootstrap.css", "../static/css/styles.css"]
# Apply our custome template
plt_io.templates["cloud_manager"] = custom_template

# App configuration for the Nonlife Dashboard
app = dash.Dash(
    name="nonlife_solo",
    title="Nonlife Solo Dashboard",
    update_title="Nonlife Solo Dashboard - updating...",
    server=server,
    eager_loading=True,
    url_base_pathname="/dash/nonlife_solo/",
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

# Define app layout
app.layout = dbc.Container(
    fluid="md",
    className="dbc",
    children=[
        dcc.Location(id="url", refresh=True),
        html.Div(
            className="logo-container",
            # className="p-8 mb-8",
            children=[
                html.Img(src="/dash/static/assets/wm_logo.svg"),
            ],
        ),
        # html.Br(),
        dcc.Input(
            id="confirmed-wvr-path",
            value="",
            placeholder="C:\\temp\\results.wvr",
            style={"width": "50%", "display": "none"},
        ),
        html.Div(
            className="body-container",
            children=[
                html.Div(
                    className="title-container",
                    children="Assumption (NLSC) Validation results",
                ),
                html.Div(
                    children=[
                        dbc.Tabs(
                            children=[
                                dbc.Tab(
                                    id="tab-1",
                                    label="LIC Model",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        html.Div(
                                            className="body-content",
                                            children=[
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="inc-paid-claims-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="inc-paid-claims-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="inc-paid-claims-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            className="line-break"
                                                        ),
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="inc-case-reserves-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="inc-case-reserves-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="inc-case-reserves-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="cum-incurred-claims-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="cum-incurred-claims-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="cum-incurred-claims-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            className="line-break"
                                                        ),
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="inc-incurred-claims-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="inc-incurred-claims-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="inc-incurred-claims-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="claim-costs-results-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="claim-costs-results-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="claim-costs-results-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="claim-costs-payment-status-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="claim-costs-payment-status-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="claim-costs-payment-status-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="link-ratios-pre-outlier-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="link-ratios-pre-outlier-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="link-ratios-pre-outlier-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="box-plot-outliers-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="box-plot-outliers-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="box-plot-outliers-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="outlier-analysis-mean-ratios-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="outlier-analysis-mean-ratios-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="outlier-analysis-mean-ratios-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            className="line-break"
                                                        ),
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="outlier-analysis-pvalue-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="outlier-analysis-pvalue-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="outlier-analysis-pvalue-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="link-ratios-post-outlier-analysis-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="link-ratios-post-outlier-analysis-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="link-ratios-post-outlier-analysis-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            className="line-break"
                                                        ),
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="link-ratios-post-data-analysis-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="link-ratios-post-data-analysis-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="link-ratios-post-data-analysis-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="development-factors-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="development-factors-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="development-factors-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            className="line-break"
                                                        ),
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="ult-development-factors-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="ult-development-factors-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="ult-development-factors-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(className="line-break"),
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="cumulative-incurred-claims-ppfia-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="cumulative-incurred-claims-ppfia-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="cumulative-incurred-claims-ppfia-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            className="line-break"
                                                        ),
                                                        html.Div(
                                                            className="one-half column custom-table",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="incremental-incurred-claims-projected-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="incremental-incurred-claims-projected-chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="incremental-incurred-claims-projected-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Br(),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Tab(
                                    id="tab-2",
                                    label="LIC Fit",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        html.Div(
                                            className="body-content",
                                            children=[
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column table-without-graph parameterization",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="parameterization-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "Parameterization table"
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="parameterization-table",
                                                                            merge_duplicate_headers=True,
                                                                            export_format="xlsx",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                                "textAlign": "center",
                                                                            },
                                                                            # fixed_columns={'headers': True, 'data': 1}, export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Br(),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Tab(
                                    id="tab-3",
                                    label="LIC Eval",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        html.Div(
                                            className="body-content",
                                            children=[
                                                html.Div(
                                                    className="row table-without-graph",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="lrc-evaluate-table-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "LIC Evaluate"
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="lrc-evaluate-v1-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="lrc-evaluate-v2-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            fixed_columns={
                                                                                "headers": True,
                                                                                "data": 1,
                                                                            },
                                                                            export_format="xlsx",
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Br(),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
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


### Charts ###


@app.callback(
    [
        Output("inc-paid-claims-chart", "figure"),
        Output("inc-paid-claims-table", "data"),
        Output("inc-paid-claims-table", "columns"),
        Output("inc-paid-claims-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Incremental Paid Claims
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return inc_paid_claims.get_chart(WVR_PATH, "Incremental Paid Claims")


# Incremental Case Reserves
@app.callback(
    [
        Output("inc-case-reserves-chart", "figure"),
        Output("inc-case-reserves-table", "data"),
        Output("inc-case-reserves-table", "columns"),
        Output("inc-case-reserves-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Incremental Case Reserves
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return generic_lic_line_chart.get_chart(
        WVR_PATH, "Incremental Case Reserves", "Tri_Claim_Costs_By_Year"
    )


# Cumulative Incurred Claims Projected (Post-Future Inflation Adj)
@app.callback(
    [
        Output("cum-incurred-claims-chart", "figure"),
        Output("cum-incurred-claims-table", "data"),
        Output("cum-incurred-claims-table", "columns"),
        Output("cum-incurred-claims-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Cumulative Incurred Claims Projected (Post-Future Inflation Adj)
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return generic_lic_line_chart.get_chart(
        WVR_PATH,
        "Cumulative Incurred Claims Projected (Post-Future Inflation Adj)",
        "Tri_Claim_Costs_Proj",
    )


# Incremental Incurred Claims Projected
@app.callback(
    [
        Output("inc-incurred-claims-chart", "figure"),
        Output("inc-incurred-claims-table", "data"),
        Output("inc-incurred-claims-table", "columns"),
        Output("inc-incurred-claims-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Incremental Incurred Claims Projected
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return generic_lic_line_chart.get_chart(
        WVR_PATH,
        "Incremental Incurred Claims Projected",
        "Tri_Claim_Costs_Proj_By_Year",
    )


# Claim Costs Results
@app.callback(
    [
        Output("claim-costs-results-chart", "figure"),
        Output("claim-costs-results-table", "data"),
        Output("claim-costs-results-table", "columns"),
        Output("claim-costs-results-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Claim Costs Results
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return claim_costs_results.get_chart(WVR_PATH, "Claim Costs Results")


# Claim Costs Results (Payment Status)
@app.callback(
    [
        Output("claim-costs-payment-status-chart", "figure"),
        Output("claim-costs-payment-status-table", "data"),
        Output("claim-costs-payment-status-table", "columns"),
        Output("claim-costs-payment-status-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Claim Costs Results
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return claim_costs_summary.get_chart(
        WVR_PATH, "Claim Costs Results (Payment Status)"
    )


# Link Ratios (Pre Outlier)
@app.callback(
    [
        Output("link-ratios-pre-outlier-chart", "figure"),
        Output("link-ratios-pre-outlier-table", "data"),
        Output("link-ratios-pre-outlier-table", "columns"),
        Output("link-ratios-pre-outlier-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Link Ratios (Pre Outlier) chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return link_ratios_pre_outlier_chart.get_chart(
        WVR_PATH,
        "Link Ratios (Pre Outlier) chart",
    )


# Box Plot - Outliers (ATA factors) chart
@app.callback(
    [
        Output("box-plot-outliers-chart", "figure"),
        Output("box-plot-outliers-table", "data"),
        Output("box-plot-outliers-table", "columns"),
        Output("box-plot-outliers-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def prepare_link_ratios_pre_outlier(n_clicks):
    """
    Box Plot - Outliers (ATA factors) chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return box_plot_outliers.get_chart(
        WVR_PATH,
        "Box Plot - Outliers (ATA factors) chart",
    )


# Outlier Analysis Mean Ratios chart
@app.callback(
    [
        Output("outlier-analysis-mean-ratios-chart", "figure"),
        Output("outlier-analysis-mean-ratios-table", "data"),
        Output("outlier-analysis-mean-ratios-table", "columns"),
        Output("outlier-analysis-mean-ratios-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Outlier Analysis Mean Ratios chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return outlieranalysis_mean_ratios.get_chart(
        WVR_PATH,
        "Outlier Analysis Mean Ratios chart",
    )


# Outlier Analysis p-Value (Pre-Outlier) chart
@app.callback(
    [
        Output("outlier-analysis-pvalue-chart", "figure"),
        Output("outlier-analysis-pvalue-table", "data"),
        Output("outlier-analysis-pvalue-table", "columns"),
        Output("outlier-analysis-pvalue-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Outlier Analysis p-Value (Pre-Outlier) chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return outlier_analysis_pvalue.get_chart(
        WVR_PATH,
        "Outlier Analysis p-Value (Pre-Outlier) chart",
    )


# Link Ratios (Post Outlier) chart
@app.callback(
    [
        Output("link-ratios-post-outlier-analysis-chart", "figure"),
        Output("link-ratios-post-outlier-analysis-table", "data"),
        Output("link-ratios-post-outlier-analysis-table", "columns"),
        Output("link-ratios-post-outlier-analysis-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Link Ratios (Post Outlier Analysis) chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return link_ratios_post_outlier_analysis.get_chart(
        WVR_PATH,
        "Link Ratios (Post Outlier Analysis) chart",
    )


# Link Ratios (Post Data Analysis) chart
@app.callback(
    [
        Output("link-ratios-post-data-analysis-chart", "figure"),
        Output("link-ratios-post-data-analysis-table", "data"),
        Output("link-ratios-post-data-analysis-table", "columns"),
        Output("link-ratios-post-data-analysis-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Link Ratios (Post Data Analysis) chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return link_ratios_post_data_analysis.get_chart(
        WVR_PATH,
        "Link Ratios (Post Data Analysis) chart",
    )


# Development Factors (Post Data Analysis) chart
@app.callback(
    [
        Output("development-factors-chart", "figure"),
        Output("development-factors-table", "data"),
        Output("development-factors-table", "columns"),
        Output("development-factors-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Development Factors (Post Data Analysis) chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return development_factors_chart.get_chart(
        WVR_PATH,
        "Development Factors (Post Data Analysis) chart",
    )


# Ultimate Development Factors (Cumulative)) chart
@app.callback(
    [
        Output("ult-development-factors-chart", "figure"),
        Output("ult-development-factors-table", "data"),
        Output("ult-development-factors-table", "columns"),
        Output("ult-development-factors-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Ultimate Development Factors (Cumulative) chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return ultimate_development_factors.get_chart(
        WVR_PATH,
        "Ultimate Development Factors (Cumulative) chart",
    )


# Ultimate Development Factors (Cumulative) chart
@app.callback(
    [
        Output("cumulative-incurred-claims-ppfia-chart", "figure"),
        Output("cumulative-incurred-claims-ppfia-table", "data"),
        Output("cumulative-incurred-claims-ppfia-table", "columns"),
        Output("cumulative-incurred-claims-ppfia-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Cumulative Incured Claims (Projected Post-Future Inflation Adj) chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return cumulative_incurred_claims_projected.get_chart(
        WVR_PATH,
        "Cumulative Incured Claims (Projected Post-Future Inflation Adj) chart",
    )


# Incremental Incurred Claims Projected chart
@app.callback(
    [
        Output("incremental-incurred-claims-projected-chart", "figure"),
        Output("incremental-incurred-claims-projected-table", "data"),
        Output("incremental-incurred-claims-projected-table", "columns"),
        Output("incremental-incurred-claims-projected-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Incremental Incurred Claims Projected  chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update
    return incremental_incurred_claims_projected.get_chart(
        WVR_PATH,
        "Incremental Incurred Claims Projected chart",
    )


# Value At Risk chart
# @app.callback(
#     [
#         Output("value-at-risk-chart", "figure"),
#         Output("value-at-risk-table", "data"),
#         Output("value-at-risk-table", "columns"),
#     ],
#     [Input("confirmed-wvr-path", "value")],
# )
# def update_figure(n_clicks):
#     """
#     Value At Risk  chart
#     """
#     if WVR_PATH is None or WVR_PATH == "":
#         return no_update, no_update, no_update
#     return value_at_risk_chart.get_chart(
#         WVR_PATH,
#         "Value At Risk chart",
#     )


# LRC Evaluation table
@app.callback(
    [
        Output("lrc-evaluate-v1-table", "data"),
        Output("lrc-evaluate-v1-table", "columns"),
        Output("lrc-evaluate-v1-table", "style_cell_conditional"),
        Output("lrc-evaluate-v2-table", "data"),
        Output("lrc-evaluate-v2-table", "columns"),
        Output("lrc-evaluate-v2-table", "style_cell_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_figure(n_clicks):
    """
    Value At Risk  chart
    """
    if WVR_PATH is None or WVR_PATH == "":
        return no_update, no_update, no_update, no_update, no_update, no_update
    return lrc_evaluate_table.get_table(WVR_PATH)


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
