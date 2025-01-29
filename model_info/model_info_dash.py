"""
@author: graham.howarth
"""

import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
from sqlalchemy import exc

import cm_dashboards.alchemy_db as db
from cm_dashboards.model_info import model_tree
from cm_dashboards.server import server

external_stylesheets = ["../static/css/dash.css"]

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

SCHEMA = ""
EXECUTION_ID = 0
JOBRUN = ""
DB_URL = ""

app = dash.Dash(
    name="model_info",
    server=server,
    url_base_pathname="/dash/model_info/",
    external_stylesheets=external_stylesheets,
    compress=server.config["COMPRESS_CONTENT"],
)

layout = go.Layout(
    title="Component Count",
    hovermode="closest",
    height=600,
    yaxis=dict(
        title="Table Entries",
    ),
    xaxis=dict(
        title="Tables",
    ),
)

trace_1 = None  # go.Bar(x=df['StepDate'], y=df['CF_Benefit_Annuity'], name='Bar None')

fig = go.Figure(data=trace_1, layout=layout)

app.layout = html.Div(
    children=[
        html.H1(children="R3S Cloud Manager", style={"color": "darkblue"}),
        html.H1(children="Model Output Summary", style={"color": "darkblue"}),
        # represents the URL bar, doesn't render anything
        dcc.Location(id="url", refresh=False),
        html.Div([dcc.Input(id="jobrun", value="", type="hidden")]),
        html.Br(),
        html.Div(
            className="row",
            children=[
                html.Div(
                    id="tableDiv2",
                    className="one-third column",
                    children=[
                        dash_table.DataTable(
                            id="executionTable",
                            row_selectable="single",
                            style_data_conditional=style_data_conditional,
                        )
                    ],
                ),
                html.Div(
                    className="one-half column",
                    children=[
                        dcc.Graph(
                            id="my-graph",
                            figure=model_tree.network_graph(SCHEMA, EXECUTION_ID, DB_URL),
                        ),
                    ],
                ),
                html.Div(
                    className="one-half column",
                    children=[
                        dcc.Graph(config={"displaylogo": False}, id="plot", figure=fig),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[],
        ),
    ],
    # style={"display": "inline-block", "width": "48%"},
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
    global DB_URL
    global SCHEMA
    if input_jobrun:
        # TODO: Improve this
        JOBRUN = input_jobrun.split("?jobrun=")[1]
        print("Got JOBRUN: {0}".format(JOBRUN))
        DB_URL = db.get_db_connection_url(JOBRUN)
        print("Got DB_URL: {0}".format(DB_URL))
        query = "select TABLE_SCHEMA from information_schema.tables where TABLE_NAME = 'T_Runs'"
        try:
            schema_list = db.query_to_list(db.get_db_connection(DB_URL), query)
        except exc.SQLAlchemyError as e:
            print(e)
            pass
        print(schema_list)
        SCHEMA = schema_list[0].values()[0]
    return JOBRUN


@app.callback(
    [
        Output("executionTable", "columns"),
        Output("executionTable", "data"),
        Output("executionTable", "style_cell_conditional"),
    ],
    [Input(component_id="jobrun", component_property="value")],
)
def update_jobruns_table(input_jobrun):
    """
    Update the table listing jobruns
    """
    mycolumns = [{"name": "ExecutionID", "id": "ExecutionID"}]
    data = [{}]
    df = pd.DataFrame()
    print("Jobrun: " + input_jobrun)
    query = (
        'select r.*, cp."Name" as "model" from "T_Runs" r '
        'inner join "T_Components" cp on r."ExecutionID" = cp."ExecutionID" '
        "where cp.\"Type\" = 'model'"
    )
    jobrun_query = '{0} and "Job_Run"={1}'.format(query, input_jobrun)
    try:
        df = db.query_to_dataframe(db.get_db_connection(DB_URL), jobrun_query)
    except exc.SQLAlchemyError as e:
        # Jobrun column may not be present in the DB
        print(e)
        pass
    data = df.to_dict("records")
    mycolumns = [{"name": i, "id": i} for i in df.columns]
    style_cell_conditional = set_column_styles(df.columns, ["ExecutionID", "ExecutionTime", "Job_Run"])

    return mycolumns, data, style_cell_conditional


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
                "textAlign": "left",
            }
        ]
        + [{"if": {"column_id": c}, "display": "None", "hidden": "True"} for c in hidden_cols]
    )
    return style_cell_conditional


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [
        dash.dependencies.Input("executionTable", "data"),
        dash.dependencies.Input("executionTable", "selected_rows"),
    ],
)
def update_model_network_chart(input_data, input_row):
    """
    Generate Network Chart based on selected Execution ID
    """
    global EXECUTION_ID
    print("Got value: " + str(input_data))
    if input_data:
        if input_row:
            EXECUTION_ID = str(input_data[input_row[0]]["ExecutionID"])
    print("schema: " + SCHEMA)
    return model_tree.network_graph(SCHEMA, EXECUTION_ID, DB_URL)


@app.callback(
    dash.dependencies.Output("plot", "figure"),
    [dash.dependencies.Input("my-graph", "clickData")],
)
def display_click_data(clickData):
    """
    A click on a chart node will get a Component
    """
    component_name = ""
    component_id = 0
    return_chart = fig
    if clickData:
        find_relevant_tables_query = "select table_name from information_schema.tables where table_schema = '{0}'".format(SCHEMA)
        count_table_entries_query = 'select count(*) as entries_count from "{schema}"."{table}" where "ExecutionID" = {execution_id}'
        df = db.query_to_dataframe(db.get_db_connection(DB_URL), find_relevant_tables_query)
        component_tables = df.to_dict("list")
        print(df)
        count_list = []
        print(component_tables)
        for table_name in component_tables["table_name"]:
            print(table_name)
            populated_query = count_table_entries_query.format(
                schema=SCHEMA,
                table=table_name,
                execution_id=EXECUTION_ID,
            )
            count_list.append(
                [
                    table_name,
                    db.query_to_list(db.get_db_connection(DB_URL), populated_query)[0][0],
                ]
            )
        count_df = pd.DataFrame(count_list, columns=["table", "count"])
        print(count_df)
        trace_1 = go.Bar(
            x=count_df["table"],
            y=count_df["count"],
            name="Component Entries",
        )

        fig1 = go.Figure(data=trace_1, layout=layout)
        return_chart = fig1

    return return_chart


# Command line entry point
# if __name__ == "__main__":
#    from waitress import serve

# serve(server, host="0.0.0.0", port=5050)
#    serve(app.server, listen="*:5051")
