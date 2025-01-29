import sys

sys.path.append("..")

import dash
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
from sqlalchemy.orm import sessionmaker

import cm_dashboards.alchemy_db as db
import cm_dashboards.utilities as utilities
from cm_dashboards.server import server

DB_ENGINE = None
DB_METADATA = None
Session = None

external_stylesheets = ["static/css/dash.css"]

app = dash.Dash(
    name="nonlife_sample",
    server=server,
    url_base_pathname="/dash/nonlife_sample/",
    external_stylesheets=external_stylesheets,
    compress=server.config["COMPRESS_CONTENT"],
)

# HTML layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                dcc.Input(id="jobrun", value="", type="hidden"),
            ]
        ),
        dcc.Graph(config={"displaylogo": False}, id="chi-squared"),
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
    global DB_ENGINE
    global DB_METADATA
    global Session
    jobrun = 0
    if input_url:
        params = utilities.extract_url_params(input_url)
        if "jobrun" in params:
            jobrun = params["jobrun"][0]
            db_url = db.get_db_connection_url(jobrun)
            DB_ENGINE = db.get_db_engine(db_url)
            DB_METADATA = db.get_db_metadata(DB_ENGINE)
            Session = sessionmaker()
            Session.configure(bind=DB_ENGINE)
    return jobrun


@app.callback(
    Output("chi-squared", "figure"),
    [Input(component_id="jobrun", component_property="value")],
)
def update_figure(input_jobrun):
    """
    Update the chart with the database query results from this customer
    """
    # Get generated view definition
    distributions = DB_METADATA.tables["GD_Distributions"]
    runs = DB_METADATA.tables["T_Runs"]
    # Build query string
    db_session = Session()

    # Figure out which execution IDs are applicable to our job run
    runs_query = db_session.query(runs).filter(runs.c.Job_Run == input_jobrun)
    execution_ids = pd.read_sql(runs_query.statement, con=runs_query.session.bind)
    execution_ids_list = execution_ids["ExecutionID"].tolist()

    # Build query on data table
    dist_query = (
        db_session.query(distributions)
        .filter(distributions.c.ExecutionID.in_(execution_ids_list))
        .filter(distributions.c.Product_Name_Value == "Grp1")
        .filter(distributions.c.Input_Variable == "Loss_Ratio")
        .filter(distributions.c.Method_Value == "MME")
    )
    # Use generated query to populate pandas dataframe
    df = pd.read_sql(dist_query.statement, con=dist_query.session.bind)
    db_session.close()

    chi_squared = px.bar(df, x="Dist_Value", y="ChiSq_Test_Stat", title="Chi-Squared Test MME")
    return chi_squared
