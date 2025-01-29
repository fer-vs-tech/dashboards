"""
@author: graham.howarth
"""

import dash
import database as db
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

external_stylesheets = ["static/css/dash.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="R3S Cloud Manager", style={"color": "darkblue"}),
        html.H1(children="Inflation Adjustment", style={"color": "darkblue"}),
        html.Div(["Filter: ", dcc.Input(id="my-input", value="2018", type="text")]),
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
        'SELECT GK."Grp_Value", GD.* FROM public."GD_Inflation_Adj" as GD '
        + 'inner join "GK_Inflation_Adj" as GK on GD."ExecutionID" = GK."ExecutionID" and GD."GroupID" = GK."GroupID"'
        + "where GK.\"Grp_Value\" like 'AY_%'"
    )
    df = db.doQueryToDf(query, "postgresql_sol2")
    mycolumns = [{"name": i, "id": i} for i in df.columns]
    return html.Div(
        [
            dcc.Graph(
                id="example",
                figure={
                    "data": [
                        {
                            "names": df["Grp_Value"],
                            "values": df["BS_Claim_Costs_OS"],
                            "type": "pie",
                            "name": "Claim Costs",
                        }
                    ],
                    "layout": {"title": "Inflation Adjustment"},
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
    serve(app.server, listen="*:5051")
