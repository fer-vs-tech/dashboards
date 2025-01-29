import json

import dash
import model_tree
from dash import dcc, html

# import the css template, and pass the css template into dash
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Transaction Network"

YEAR = [2010, 2019]
ACCOUNT = 0

# styles: for right side hover/click component
styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}

app.layout = html.Div(
    [
        html.Div(
            [html.H1("Transaction Network Graph")],
            className="row",
            style={"textAlign": "center"},
        ),
        html.Div(
            ["Execution filter: ", dcc.Input(id="execution-id", value="1", type="text")]
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="eight columns",
                    children=[
                        dcc.Graph(
                            id="my-graph",
                            figure=model_tree.network_graph("public", 1),
                        )
                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [
        dash.dependencies.Input("execution-id", "value"),
    ],
)
def update_output(value):
    return model_tree.network_graph("public", value)


@app.callback(
    dash.dependencies.Output("hover-data", "children"),
    [dash.dependencies.Input("my-graph", "hoverData")],
)
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    dash.dependencies.Output("click-data", "children"),
    [dash.dependencies.Input("my-graph", "clickData")],
)
def display_click_data(clickData):
    print(json.dumps(clickData, indent=2))
    return json.dumps(clickData, indent=2)


# Command line entry point
if __name__ == "__main__":
    from waitress import serve

    # serve(server, host="0.0.0.0", port=5050)
    serve(app.server, listen="*:5051")
