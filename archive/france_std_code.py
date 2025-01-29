"""
@author: graham.howarth
"""
import dash
import database as db
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

external_stylesheets = ["static/css/dash.css"]

query = 'SELECT * FROM "A_PS_Pension" where "ExecutionID" = 1 and "CF_Benefit_Annuity" > 0 order by "StepDate" asc'
df = db.doQueryToDf(query, "postgresql_france")

# dropdown options
features = df.columns[1:-1]
opts = [{"label": i, "value": i} for i in features]

# layout = go.Layout(title = 'Time Series Plot',
#                  hovermode = 'closest')
layout = go.Layout(barmode="stack")
# trace_1 = go.Scatter(x = df['StepDate'], y = df['CF_Benefit_Annuity'],
#                    name = 'Annuity Benefit',
#                    line = dict(width = 2,
#                                color = 'rgb(229, 151, 50)'))

trace_1 = go.Bar(x=df["StepDate"], y=df["CF_Benefit_Annuity"], name="Bar None")

fig = go.Figure(data=trace_1, layout=layout)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="R3S Cloud Manager", style={"color": "darkblue"}),
        html.H1(children="France Cash Flow Projection", style={"color": "darkblue"}),
        html.Div(
            ["Date filter: ", dcc.Input(id="my-input", value="2018", type="text")]
        ),
        html.Br(),
        # adding a plot
        dcc.Graph(config={"displaylogo": False}, id="plot", figure=fig),
        # dropdown
        html.P(
            [
                html.Label("Choose a feature"),
                dcc.Checklist(id="opt", options=opts, value=opts[0]),
            ]
        ),
        html.Div(
            [
                html.Div([], id="tableDiv", className="one-third column"),
                html.Div([], id="deathAnnuity", className="one-third column"),
            ],
            className="row",
        ),
    ]
)  # , style={'display': 'inline-block', 'width': '48%'})


# Step 5. Add callback functions
@app.callback(Output("plot", "figure"), [Input("opt", "value")])
def update_figure(input1):
    selected_plots = []
    print(input1)
    for checked in input1:
        # selected_plots.append(go.Bar(x=df['StepDate'], y=df[checked], name=checked))

        selected_plots.append(
            go.Scatter(
                x=df["StepDate"],
                y=df[checked],
                name=checked,
                line=dict(
                    width=2
                    # , color = 'rgb(106, 181, 135)'
                ),
            )
        )

    fig = go.Figure(data=selected_plots, layout=layout)
    return fig


# Command line entry point
if __name__ == "__main__":
    from waitress import serve

    # serve(server, host="0.0.0.0", port=5050)
    serve(app.server, listen="*:5050")
