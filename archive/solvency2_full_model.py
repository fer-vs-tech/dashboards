"""
@author: graham.howarth
"""
import pandas as pd

import dash

from dash.dependencies import Output, Input
from dash import html, dcc, dash_table

import plotly.graph_objs as go

import database as db

external_stylesheets = ["static/css/dash.css"]

query_bscr = 'SELECT "SCR_Def", "SCR_Health", "SCR_Int", "SCR_Life", "SCR_Mkt", "SCR_NonLife" FROM "A_BSCR"'

query_bond = (
    'SELECT * FROM "A_Bond" where "Realistic_RN_Scenario" = 1 order by "StepDate" asc'
)
query_cash = (
    'SELECT * FROM "A_Cash" where "Realistic_RN_Scenario" = 1 order by "StepDate" asc'
)
query_company = 'SELECT * FROM "A_Company" where "Realistic_RN_Scenario" = 1 order by "StepDate" asc'
query_equity = (
    'SELECT * FROM "A_Equity" where "Realistic_RN_Scenario" = 1 order by "StepDate" asc'
)
query_property = 'SELECT * FROM "A_Property" where "Realistic_RN_Scenario" = 1 order by "StepDate" asc'

df_bscr = db.doQueryToDf(query_bscr, "postgresql_sol2")
print(df_bscr)
df_bscr = df_bscr.unstack()
df_bscr = df_bscr.reset_index()
df_bscr = df_bscr.drop(columns=["level_1"])
print(df_bscr)
print(df_bscr["level_0"])


df_bond = db.doQueryToDf(query_bond, "postgresql_sol2")
df_cash = db.doQueryToDf(query_cash, "postgresql_sol2")
df_company = db.doQueryToDf(query_company, "postgresql_sol2")
df_equity = db.doQueryToDf(query_equity, "postgresql_sol2")
df_property = db.doQueryToDf(query_property, "postgresql_sol2")

# dropdown options
features = df_bond.columns[1:-1]
opts = [{"label": i, "value": i} for i in features]

layout = go.Layout(title="Time Series Plot", hovermode="closest")
# layout=go.Layout(barmode='stack')
# trace_1 = go.Scatter(x = df['StepDate'], y = df['CF_Benefit_Annuity'],
#                    name = 'Annuity Benefit',
#                    line = dict(width = 2,
#                                color = 'rgb(229, 151, 50)'))

trace_1 = None  # go.Bar(x=df['StepDate'], y=df['CF_Benefit_Annuity'], name='Bar None')

fig = go.Figure(data=trace_1, layout=layout)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="R3S Cloud Manager", style={"color": "darkblue"}),
        html.H1(children="Solvency II Projections", style={"color": "darkblue"}),
        html.Br(),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="bscr",
                            figure={
                                "data": [
                                    {
                                        "labels": df_bscr["level_0"],
                                        "values": df_bscr[0],
                                        "type": "pie",
                                        "name": "BSCR",
                                    }
                                ],
                                "layout": {"title": "BSCR"},
                            },
                        ),
                    ],
                    className="one-half column",
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="assets",
                            figure={
                                "data": [
                                    {
                                        "labels": [
                                            "Bonds",
                                            "Cash",
                                            "Company",
                                            "Equity",
                                            "Property",
                                        ],
                                        "values": [
                                            df_bond["Assets_Total"][0],
                                            df_cash["Assets_Total"][0],
                                            df_company["Assets_Total"][0],
                                            df_equity["Assets_Total"][0],
                                            df_property["Assets_Total"][0],
                                        ],
                                        "type": "pie",
                                        "name": "Assets Distribution",
                                    }
                                ],
                                "layout": {"title": "Assets Distribution"},
                            },
                        )
                    ],
                    className="one-half column",
                ),
            ],
            className="row",
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
        html.Div(
            [
                html.Div([], id="tableDiv", className="one-half column"),
                html.Div([], id="deathAnnuity", className="one-half column"),
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
        selected_plots.append(
            go.Scatter(
                x=df_bond["StepDate"], y=df_bond[checked], name=str(checked + ", Bonds")
            )
        )
        selected_plots.append(
            go.Scatter(
                x=df_cash["StepDate"],
                y=df_cash[checked],
                name=str(checked + ", Cash"),
                line=dict(width=2),
            )
        )
        selected_plots.append(
            go.Scatter(
                x=df_company["StepDate"],
                y=df_company[checked],
                name=str(checked + ", Company"),
                line=dict(width=2),
            )
        )
        selected_plots.append(
            go.Scatter(
                x=df_equity["StepDate"],
                y=df_equity[checked],
                name=str(checked + ", Equity"),
                line=dict(width=2),
            )
        )
        selected_plots.append(
            go.Scatter(
                x=df_property["StepDate"],
                y=df_property[checked],
                name=str(checked + ", Property"),
                line=dict(width=2),
            )
        )
        # selected_plots.append(go.Scatter(x = df_bond['StepDate'], y = df_bond[checked],
        #                name = checked,
        #                line = dict(width = 2)))

    fig = go.Figure(data=selected_plots, layout=layout)
    return fig


# Command line entry point
if __name__ == "__main__":
    from waitress import serve

    # serve(server, host="0.0.0.0", port=5050)
    serve(app.server, listen="*:5051")
