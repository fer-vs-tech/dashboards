import sys

sys.path.append("..")

import os
from timeit import default_timer as timer

import dash
import pyodbc
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign
from dash.dependencies import Input, Output
from sqlalchemy.orm import sessionmaker

import cm_dashboards.alchemy_db as db
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr
from cm_dashboards.server import server as server

DB_ENGINE = None
DB_METADATA = None
Session = None
JOBRUN_ROOT = None
JOBRUN_WVR_PATH = None

external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/dash.css"]


app = dash.Dash(
    name="model_data",
    server=server,
    url_base_pathname="/dash/model_data/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    compress=server.config["COMPRESS_CONTENT"],
)

# HTML layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Input(id="jobrun", value="", type="hidden"),
        "Jobrun Name",
        html.Br(),
        dcc.Input(id="jobname", value=""),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="one-third column",
                    children=[
                        "Models in Batch",
                        dcc.Dropdown(
                            id="modelsDropdown",
                            options=[],
                        ),
                        "Row limit",
                        html.Br(),
                        dcc.Input(id="rowlimit", value="1000"),
                    ],
                ),
                html.Div(
                    className="one-third column",
                    children=[
                        "Model Tables",
                        dcc.Dropdown(
                            id="tablesDropdown",
                            options=[],
                        ),
                        "Table Size",
                        html.Br(),
                        dcc.Input(id="rowcount", value=""),
                    ],
                ),
            ],
        ),
        html.Div(
            id="tableDiv",
            #      className="eleven columns",
            children=[
                "Table Data",
                dash_table.DataTable(
                    id="dataOutputTable",
                    export_format="xlsx",
                    export_columns="visible",
                    filter_action="native",
                    # currently some headers are being truncated
                    #    sort_action="native",
                    sort_mode="multi",
                    page_size=500,
                    style_table={
                        "overflowX": "auto",
                        "minWidth": "100%",
                        "height": "600px",
                        "overflowY": "auto",
                    },
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
    global JOBRUN_ROOT
    global DB_METADATA
    global Session
    if input_url:
        params = utilities.extract_url_params(input_url)
        jobrun = 0
        if "jobrun" in params:
            jobrun = params["jobrun"][0]
            # print("Got JOBRUN: {0}".format(jobrun))
            db_url = utilities.get_modelrunner_db_url()
            if not JOBRUN_ROOT:
                JOBRUN_ROOT = utilities.get_entry_from_config_file("folders", "jobruns")
            DB_ENGINE = db.get_db_engine(db_url)
            if not DB_METADATA:
                DB_METADATA = db.get_db_metadata_subset(DB_ENGINE, ["JobRuns"])
            if not Session:
                Session = sessionmaker()
                Session.configure(bind=DB_ENGINE)
    return jobrun


@app.callback(
    Output("jobname", "value"),
    [Input(component_id="jobrun", component_property="value")],
)
def get_jobrun_name(input_jobrun):
    """
    Get name of this jobrun given the jobrun ID
    """
    global JOBRUN_WVR_PATH
    # Jobruns table
    jobruns = DB_METADATA.tables["JobRuns"]
    # Build query string
    db_session = Session()
    # Get jobrun entry
    jobrun_name = db_session.query(jobruns.c.name).filter(jobruns.c.id == input_jobrun).scalar()
    db_session.close()

    jobrun_wvr = jobrun_name + ".wvr"
    JOBRUN_WVR_PATH = os.path.join(JOBRUN_ROOT, jobrun_wvr)
    # print(JOBRUN_WVR_PATH)
    # print(jobrun_name)
    return jobrun_name


@app.callback(
    Output("modelsDropdown", "options"),
    [Input(component_id="jobname", component_property="value")],
)
def update_models_dropdown(input_jobname):
    """
    Update the model dropdown with the models inside this jobrun wvr
    """
    global JOBRUN_ROOT
    model_list = wvr.model_names_in_jobrun(JOBRUN_ROOT, input_jobname)
    print(model_list)
    # Build dropdown list data format
    dropdown_data = list()
    for model in model_list:
        dropdown_data.append({"label": model, "value": model})
    return dropdown_data


@app.callback(
    Output("tablesDropdown", "options"),
    [
        Input(component_id="modelsDropdown", component_property="value"),
    ],
)
def get_table_list(model_name):
    """
    Get list of tables in given wvr for given model
    """
    global JOBRUN_WVR_PATH
    dropdown_data = list()
    table_list = list()
    if model_name and JOBRUN_WVR_PATH:
        model_url = wvr.get_wvr_connection_url(JOBRUN_WVR_PATH, model_name)
        print(model_url)
        con = pyodbc.connect(model_url)
        table_list = wvr.get_wvr_table_list(con)
        con.close()
        # print(table_list)
    for table in table_list:
        dropdown_data.append({"label": table, "value": table})
    return dropdown_data


@app.callback(
    [
        Output("dataOutputTable", "columns"),
        Output("dataOutputTable", "data"),
        #       Output("dataOutputTable", "style_cell_conditional"),
        #       Output("dataOutputTable", "hidden_columns"),
    ],
    [
        Input(component_id="modelsDropdown", component_property="value"),
        Input(component_id="tablesDropdown", component_property="value"),
        Input(component_id="rowlimit", component_property="value"),
    ],
)
def get_table_data(model_name, table_name, rowlimit):
    """
    Get data for the given table in wvr for given model
    """
    global JOBRUN_WVR_PATH

    column_names = list()
    table_data = list()
    if model_name and table_name and JOBRUN_WVR_PATH:
        model_url = wvr.get_wvr_connection_url(JOBRUN_WVR_PATH, model_name)
        print(model_url)
        if len(rowlimit) == 0:
            rowlimit = 1000
        rowlimit = int(rowlimit)
        if rowlimit < 1:
            rowlimit = 1000
        if rowlimit > 100000:
            rowlimit = 100000
        start = timer()
        con = pyodbc.connect(model_url)
        end = timer()
        print("Obtaining a connection to {0} took {1}s".format(model_url, end - start))
        table_data_df = wvr.get_wvr_table_data(table_name, con, rowlimit)
        con.close()
        # #print(table_data_df)
        table_data = table_data_df.to_dict("records")
        # print(table_data)
        column_names = set_column_names(table_data_df.columns)
    return column_names, table_data


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


@app.callback(
    Output("rowcount", "value"),
    [
        Input(component_id="modelsDropdown", component_property="value"),
        Input(component_id="tablesDropdown", component_property="value"),
    ],
)
def get_rowcount(model_name, table_name):
    rowcount = ""
    if model_name and table_name and JOBRUN_WVR_PATH:
        model_url = wvr.get_wvr_connection_url(JOBRUN_WVR_PATH, model_name)
        con = pyodbc.connect(model_url)
        rowcount = wvr.get_wvr_table_rowcount(table_name, con)
    return rowcount
