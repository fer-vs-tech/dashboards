import sys

sys.path.append("..")

import dash
import pandas as pd
import plotly.express as px
import pyodbc
from dash import dcc, html
from dash.dependencies import Input, Output

import cm_dashboards.alchemy_db as db
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr
from cm_dashboards.server import server

JOBRUN_WVR_PATH = None

external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/dash.css"]


app = dash.Dash(
    name="nippon_ESR",
    server=server,
    url_base_pathname="/dash/nippon_ESR/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    compress=server.config["COMPRESS_CONTENT"],
)

# HTML layout
app.layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=False),
        dcc.Input(id="jobrun", value="", type="hidden"),
        dcc.Input(id="jobname", value=""),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="one-half column",
                    children=[
                        dcc.Graph(config={"displaylogo": False}, id="group-RC-chart"),
                        dcc.Graph(config={"displaylogo": False}, id="group-ESR-chart"),
                    ],
                ),
                html.Div(
                    className="one-half column",
                    children=[
                        dcc.Graph(config={"displaylogo": False}, id="group-CapReq-chart"),
                        dcc.Graph(config={"displaylogo": False}, id="group-OwnFund-chart"),
                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("jobrun", "value"),
    [dash.dependencies.Input("url", "search")],
)
def get_jobrun(input_url):
    """
    Get customer ID from URL parameters
    """
    if input_url:
        params = utilities.extract_url_params(input_url)
        jobrun = 0
        if "jobrun" in params:
            jobrun = params["jobrun"][0]
            print("Got JOBRUN: {0}".format(jobrun))
    return jobrun


@app.callback(
    Output("jobname", "value"),
    [Input(component_id="jobrun", component_property="value")],
)
def get_jobrun_name(input_jobrun):
    """
    Get name of this jobrun given the jobrun ID
    """
    jobrun_name = None
    global JOBRUN_WVR_PATH

    jobrun_name = db.get_jobrun_name_from_id(input_jobrun)
    JOBRUN_WVR_PATH = utilities.get_jobrun_path(jobrun_name)
    return jobrun_name


@app.callback(
    [
        Output("group-RC-chart", "figure"),
        Output("group-ESR-chart", "figure"),
        Output("group-CapReq-chart", "figure"),
        Output("group-OwnFund-chart", "figure"),
    ],
    [Input(component_id="jobname", component_property="value")],
)
def update_figure(input_jobname):
    """
    Update the chart with the database query results from this customer
    """
    global JOBRUN_WVR_PATH
    group_rc_df = None
    group_rc_chart = None
    group_esr_chart = None
    group_capreq_chart = None
    group_ownfund_chart = None
    column_names = list()
    table_data = list()

    if JOBRUN_WVR_PATH:
        model_url = wvr.get_wvr_connection_url(JOBRUN_WVR_PATH, "Group_ESR_Model_NipponLife")
        print(model_url)

        con = pyodbc.connect(model_url)
        # select a.Company_Name as entity, a.RC from A_ESR_Group a union
        group_rc_df = pd.read_sql(
            "select a.Group_Name as entity, a.RC, a.ESR, a.AC from A_ESR_Group a",
            con,
        )
        group_rc_df["color"] = "green"
        sub_ecr_df = pd.read_sql(
            "select b.[ESR_Level_1 Value] as entity, b.RC, b.ESR, b.AC from G_ESR_Level_1 b",
            con,
        )
        sub_ecr_df["color"] = "steelblue"
        group_rc_df = group_rc_df.append(sub_ecr_df)
        con.close()
        print(group_rc_df)
        # table_data = table_data_df.to_dict("records")
        # print(table_data)
        # column_names = set_column_names(table_data_df.columns)

        group_rc_chart = px.bar(
            data_frame=group_rc_df,
            x="entity",
            y="RC",
            title="Levelごとの所要資本要約",
            color=group_rc_df["color"],
            color_discrete_map="identity",
            text="RC",
        )
        group_rc_chart.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
        no_mlc_df = group_rc_df[group_rc_df["entity"] != "MLC"]
        group_esr_chart = px.bar(
            data_frame=no_mlc_df,
            x="entity",
            y="ESR",
            title="LevelごとのESR要約",
            color=no_mlc_df["color"],
            color_discrete_map="identity",
            text="ESR",
        )
        group_esr_chart.update_traces(
            texttemplate="%{text:.1%}",
            textposition="outside",
            cliponaxis=False,
        )
        group_esr_chart.update_yaxes(tickformat=".0%")
        group_capreq_chart = px.bar(
            data_frame=no_mlc_df,
            x="entity",
            y="RC",
            title="Levelごとの所要資本要約",
            color=no_mlc_df["color"],
            color_discrete_map="identity",
            text="RC",
        )
        group_capreq_chart.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
        group_ownfund_chart = px.bar(
            data_frame=no_mlc_df,
            x="entity",
            y="AC",
            title="Levelごとの適格資本要約",
            color=no_mlc_df["color"],
            color_discrete_map="identity",
            text="AC",
        )
        group_ownfund_chart.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    return group_rc_chart, group_esr_chart, group_capreq_chart, group_ownfund_chart
