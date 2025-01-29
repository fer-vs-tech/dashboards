"""
@author: graham.howarth
"""

import alchemy_db as db
import dash
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
from flask import Flask

server = Flask(__name__)
# Disable any caching of downloaded files
server.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
server.config["UPLOAD_FOLDER"] = "."

app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/")

app.layout = html.Div(
    children=[
        html.H1(children="R3S Cloud Manager", style={"color": "darkblue"}),
        html.H1(
            children="Sum Assured and Value Net Premium", style={"color": "darkblue"}
        ),
        html.Div(
            ["Date filter: ", dcc.Input(id="my-input", value="2018", type="text")]
        ),
        html.Br(),
        html.Div(id="tableDiv", className="tableDiv"),
    ],
    style={"display": "inline-block", "width": "48%"},
)


@app.callback(
    Output("tableDiv", "children"),
    [Input(component_id="my-input", component_property="value")],
)
def update_table(input_value):
    query = (
        'select "COMMENCEMENT_DATE", sum("SUM_ASSURED") as SUM_ASSURED, sum("VAL_NET_PREM") as VAL_NET_PREM from "I_NEW_PAR" '
        + 'where "ExecutionID" = 9 and TO_CHAR("COMMENCEMENT_DATE", \'YYYY-MM-DD\') like\''
        + input_value
        + '%\' group by "COMMENCEMENT_DATE" order by "COMMENCEMENT_DATE"'
    )
    df = db.query_to_dataframe(db.get_db_connection(entry="postgres_vietnam"), query)
    print(df)
    mycolumns = [{"name": i, "id": i} for i in df.columns]
    return html.Div(
        [
            dcc.Graph(
                id="example",
                figure={
                    "data": [
                        {
                            "x": df["COMMENCEMENT_DATE"],
                            "y": df["sum_assured"],
                            "type": "line",
                            "name": "Sum Assured",
                        },
                        {
                            "x": df["COMMENCEMENT_DATE"],
                            "y": df["val_net_prem"],
                            "type": "bar",
                            "name": "Net Premium",
                        },
                    ],
                    "layout": {"title": "Sum Assured and Value Net Premium"},
                },
            ),
            dash_table.DataTable(
                id="table", columns=mycolumns, data=df.to_dict("records")
            ),
        ]
    )


# Command line entry point
if __name__ == "__main__":
    from waitress import serve

    # serve(server, host="0.0.0.0", port=5050)
    serve(server, listen="*:5050")
