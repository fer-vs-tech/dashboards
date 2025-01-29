import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

# Step 1. Launch the application
external_stylesheets = ["static/css/dash.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Step 2. Import the dataset
filepath = (
    "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv"
)
st = pd.read_csv(filepath)

# dropdown options
features = st.columns[1:-1]
opts = [{"label": i, "value": i} for i in features]

# range slider options
st["Date"] = pd.to_datetime(st.Date)
dates = [
    "2015-02-17",
    "2015-05-17",
    "2015-08-17",
    "2015-11-17",
    "2016-02-17",
    "2016-05-17",
    "2016-08-17",
    "2016-11-17",
    "2017-02-17",
]


# Step 3. Create a plotly figure
plots = []
trace_1 = go.Scatter(
    x=st.Date,
    y=st["AAPL.High"],
    name="AAPL HIGH",
    line=dict(width=2, color="rgb(229, 151, 50)"),
)
plots.append(trace_1)
layout = go.Layout(title="Time Series Plot", hovermode="closest")
fig = go.Figure(data=trace_1, layout=layout)


# Step 4. Create a Dash layout
app.layout = html.Div(
    [
        # a header and a paragraph
        html.Div(
            [html.H1("Stock Dashboard"), html.P("Apple Inc")],
            style={"padding": "50px", "backgroundColor": "#3aaab2"},
        ),
        # adding a plot
        dcc.Graph(config={"displaylogo": False}, id="plot", figure=fig),
        # dropdown
        html.P(
            [
                html.Label("Choose a feature"),
                dcc.Checklist(id="opt", options=opts, value=opts[0]),
            ]
        ),
        # range slider
        html.P(
            [
                html.Label("Time Period"),
                dcc.RangeSlider(
                    id="slider",
                    marks={i: dates[i] for i in range(0, 9)},
                    min=0,
                    max=8,
                    value=[1, 7],
                ),
            ],
            style={
                "width": "80%",
                "fontSize": "20px",
                "padding-left": "100px",
                "display": "inline-block",
            },
        ),
    ]
)


# Step 5. Add callback functions
@app.callback(
    Output("plot", "figure"), [Input("opt", "value"), Input("slider", "value")]
)
def update_figure(input1, input2):
    # filtering the data
    st2 = st[(st.Date > dates[input2[0]]) & (st.Date < dates[input2[1]])]
    selected_plots = []
    print(input1)
    for checked in input1:
        selected_plots.append(
            go.Scatter(
                x=st2.Date,
                y=st2[checked],
                name=checked,
                line=dict(width=2, color="rgb(106, 181, 135)"),
            )
        )

    fig = go.Figure(data=selected_plots, layout=layout)
    return fig


# Step 6. Add the server clause
if __name__ == "__main__":
    from waitress import serve

    serve(app.server, listen="*:5050")
