import dash
from dash import dcc, html

external_stylesheets = ["static/css/dash.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Column 1"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.H3("Column 2"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g2",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.H3("Column 3"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g3",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one-third column",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Column 1"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g4",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="three columns",
                ),
                html.Div(
                    [
                        html.H3("Column 2"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g5",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="three columns",
                ),
                html.Div(
                    [
                        html.H3("Column 3"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g6",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="three columns",
                ),
                html.Div(
                    [
                        html.H3("Column 4"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g7",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="three columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Column 1"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g8",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="two columns",
                ),
                html.Div(
                    [
                        html.H3("Column 2"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g9",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="two columns",
                ),
                html.Div(
                    [
                        html.H3("Column 3"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g10",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="two columns",
                ),
                html.Div(
                    [
                        html.H3("Column 4"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g11",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="two columns",
                ),
                html.Div(
                    [
                        html.H3("Column 5"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g12",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="two columns",
                ),
                html.Div(
                    [
                        html.H3("Column 6"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g13",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="two columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Column 1"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g14",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 2"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g15",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 3"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g16",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 4"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g17",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 5"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g18",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 6"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g19",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 7"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g20",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 8"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g21",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 9"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g22",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 10"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g23",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 11"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g24",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
                html.Div(
                    [
                        html.H3("Column 12"),
                        dcc.Graph(
                            config={"displaylogo": False},
                            id="g25",
                            figure={"data": [{"y": [1, 2, 3]}]},
                        ),
                    ],
                    className="one columns",
                ),
            ],
            className="row",
        ),
    ]
)


# Command line entry point
if __name__ == "__main__":
    from waitress import serve

    # serve(server, host="0.0.0.0", port=5050)
    serve(app.server, listen="*:5050")
