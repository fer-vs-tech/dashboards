import sys

sys.path.append("..")

import importlib.resources as pkg_resources

import dash
import plotly.express as px
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign
from dash.dependencies import Input, Output

import cm_dashboards.nonlife
import cm_dashboards.nonlife.assumption_manager as excel_handler
import cm_dashboards.nonlife.excel_tools as excel_tools
from cm_dashboards.server import server

DB_ENGINE = None
DB_METADATA = None
Session = None


external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/dash.css"]

app = dash.Dash(
    name="nonlife_pivot",
    server=server,
    url_base_pathname="/dash/nonlife/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    compress=server.config["COMPRESS_CONTENT"],
)

# HTML layout

app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        html.H2(children="R3S Cloud Manager"),
        html.H3(children="Liability for Incurred Claims"),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="one-half column",
                    children=[
                        dcc.Graph(config={"displaylogo": False}, id="claim-cost-chart"),
                        dcc.Graph(config={"displaylogo": False}, id="cum-claims-chart"),
                    ],
                ),
                html.Div(
                    className="one-half column",
                    children=[
                        dcc.Graph(config={"displaylogo": False}, id="dev-factors-chart"),
                        dcc.Graph(config={"displaylogo": False}, id="ult-dev-factors-chart"),
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
                        dcc.Graph(config={"displaylogo": False}, id="var-by-scenario-chart"),
                    ],
                ),
            ],
        ),
    ]
)
"""
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="one-half column",
                            children=[dash_table.DataTable(id="claim-cost-table")],
                        ),
                        html.Div(
                            className="one-half column",
                            children=[
                                dash_table.DataTable(id="cum-claims-table"),
                            ],
                        ),
                    ],
                ),
"""


@app.callback(
    [
        Output("claim-cost-chart", "figure"),
        Output("cum-claims-chart", "figure"),
        Output("dev-factors-chart", "figure"),
        Output("ult-dev-factors-chart", "figure"),
        Output("var-by-scenario-chart", "figure"),
        # Output("claim-cost-table", "data"),
        # Output("claim-cost-table", "columns"),
        # Output("cum-claims-table", "data"),
        # Output("cum-claims-table", "columns"),
    ],
    [dash.dependencies.Input("url", "search")],
)
def update_figure(input_url):
    """
    Update the chart with the database query results from this customer
    """
    temp = None
    excel_filepath = "Nonlife_Output Report_Sample2.xlsx"
    excel_file = pkg_resources.open_binary(cm_dashboards.nonlife, excel_filepath)
    book = excel_tools.load_workbook(excel_file, read_only=True, data_only=True)
    # Extract data in pivoted format as it would be in a database
    claim_cost_data, claim_cost_table_data = extract_data(book, "Claim_Cost_Results")
    cum_claims_data, cum_claims_table_data = extract_data(book, "Cum_Claims_Projected")
    dev_factors_data, temp = extract_data(book, "Dev_Factors")
    ult_dev_factors_data, temp = extract_data(book, "Ultimate_Dev_Factors")
    var_by_scenario_data, temp = extract_data(book, "VaR_by_Scenario")
    book.close()

    claim_cost_chart = prepare_claim_cost_chart(claim_cost_data)
    cum_claims_chart = prepare_cum_claims_chart(cum_claims_data)
    dev_factors_chart = prepare_dev_factors_chart(dev_factors_data)
    ult_dev_factors_chart = prepare_ult_dev_factors_chart(ult_dev_factors_data)
    var_by_scenario_chart = prepare_var_by_scenario_chart(var_by_scenario_data)

    claim_cost_dict = claim_cost_table_data.to_dict("records")
    claim_cost_column_names = set_column_names(claim_cost_table_data.columns)

    cum_claims_dict = cum_claims_table_data.to_dict("records")
    cum_claims_column_names = set_column_names(cum_claims_table_data.columns)
    return (
        claim_cost_chart,
        cum_claims_chart,
        dev_factors_chart,
        ult_dev_factors_chart,
        var_by_scenario_chart,
        # claim_cost_dict,
        # claim_cost_column_names,
        # cum_claims_dict,
        # cum_claims_column_names,
    )


def prepare_claim_cost_chart(chart_data):
    """
    Claim Cost Results
    """
    # We have to convert this dataframe to a dictionary else we get a strange chart!
    claim_cost_dict = chart_data[chart_data.Costs.isin(["Paid to date", "Outstanding"])].to_dict("records")
    chart = px.bar(
        claim_cost_dict,
        x="AY",
        y="Val",
        color="Costs",
        title="Claim Costs Results",
        labels={"Val": "Claim Costs"},
    )
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")
    return chart


def prepare_cum_claims_chart(chart_data):
    """
    Cumulative Claims Projected
    """
    chart = px.line(
        chart_data,
        x="DY",
        y="Val",
        color="AY",
        title="Cumulative Claims Projected",
        labels={"Val": "Claims"},
    )
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")
    return chart


def prepare_dev_factors_chart(chart_data):
    """
    Development Factors
    """
    chart = px.line(
        chart_data,
        x="Dev Year",
        y="Val",
        color="Factors",
        title="Development Factors",
        labels={"Val": "Factors"},
    )
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")
    return chart


def prepare_ult_dev_factors_chart(chart_data):
    """
    Ultimate Development Factors
    """
    chart = px.line(
        chart_data,
        x="DY",
        y="Val",
        color="AY",
        title="Ultimate Development Factors",
        labels={"Val": "Factors"},
    )
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")
    return chart


def prepare_var_by_scenario_chart(chart_data):
    """
    VaR by Scenario
    """
    chart = px.line(
        chart_data,
        x="Confidence Level",
        y="Val",
        color="Step",
        title="VaR by Scenario",
        labels={"Val": "VaR", "Step": "Scenario"},
    )  # .update_traces(mode="markers+lines")
    chart.add_vline(
        x=0.75,
        line_width=0.5,
        line_color="gray",
        line_dash="dash",
        annotation_text="0.75",
    )
    chart.update_yaxes(autotypenumbers="strict")
    return chart


def extract_data(book, range):
    """
    Get dataframe from an excel named range in pivoted format that matches database table layout
    """
    unpivot_data = None
    # Data in same shape as in Excel named range
    initial_data, dimensions = excel_handler.get_data_from_named_range(book, range)
    # Data in pivoted format
    pivot_data = excel_handler.pivot_data(initial_data, dimensions)
    unpivot_data = excel_handler.unpivot_data(pivot_data, dimensions)
    print(pivot_data)
    print(unpivot_data)
    return pivot_data, unpivot_data


def set_column_names(columns):
    """
    Apply the column names for the table
    """
    column_names = [
        {
            "name": i,
            "id": i,
            "type": "numeric",
            "deletable": False,
            "format": Format(group=",", precision=0, scheme=Scheme.fixed, sign=Sign.parantheses),
        }
        for i in columns
    ]
    return column_names
