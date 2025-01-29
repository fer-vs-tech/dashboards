"""
@author: graham.howarth
"""
import dash
import database as db
import plotly.graph_objs as go
from dash import dcc, html

external_stylesheets = ["static/css/dash.css"]

query_liability = (
    "select "
    + '"Income_Proj_All" as "Future Cash Inflows",'
    + '-"Outgo_Proj_All" as "Future Cash Outflows",'
    + '"Disc_Time_Value_Orig_DR" as "TVOG: original disc",'
    + '"Risk_Adjustment" as "Risk Adjustment",'
    + '-"Contractual_Service_Margin" as "Contractual Service Margin",'
    +
    #'"PV_Income_Orig_DR_Proj",' +
    #'"PV_Outgo_Orig_DR_Proj",' +
    #'"Fulfilment_Cash_Flows",' +
    '0 as "Loss Component",'
    + '0 as "Incurred Claims",'
    + '-"Insurance_Contract_Liability" as "Insurance_Contract_Liability" '
    + 'from "IFRS_17_(PVCF)"."GD_Portfolio" as GD '
    + 'inner join "IFRS_17_(PVCF)"."GK_Portfolio" as GK on '
    + 'GD."ExecutionID" = GK."ExecutionID" and '
    + 'GD."GroupID" = GK."GroupID" '
    + "where GK.\"Product_Name_Value\" = 'Ex15B' and \"StepDate\" = '2019-12-31'"
)


df_liability = db.doQueryToDf(query_liability, "postgresql_ifrs17")
print(df_liability)
df_liability = df_liability.unstack()
df_liability = df_liability.reset_index()
df_liability = df_liability.drop(columns=["level_1"])
print(df_liability)
print(df_liability["level_0"])

# dropdown options
features = df_liability.columns[0:-1]
opts = [{"label": i, "value": i} for i in features]

layout = go.Layout(title="Insurance Contract Liability")
# layout=go.Layout(barmode='stack')
# trace_1 = go.Scatter(x = df['StepDate'], y = df['CF_Benefit_Annuity'],
#                    name = 'Annuity Benefit',
#                    line = dict(width = 2,
#                                color = 'rgb(229, 151, 50)'))
print(df_liability.loc[[0]])
fig = go.Waterfall(
    x=df_liability["level_0"],
    measure=[
        "absolute",
        "relative",
        "relative",
        "relative",
        "relative",
        "relative",
        "absolute",
        "relative",
    ],
    y=df_liability[0],
    base=0,
    decreasing={"marker": {"color": "Maroon", "line": {"color": "red", "width": 2}}},
    increasing={"marker": {"color": "Teal"}},
    totals={
        "marker": {"color": "deep sky blue", "line": {"color": "blue", "width": 3}}
    },
)

# trace_1 = None #go.Bar(x=df['StepDate'], y=df['CF_Benefit_Annuity'], name='Bar None')

fig = go.Figure(data=fig, layout=layout)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="R3S Cloud Manager", style={"color": "darkblue"}),
        html.H1(children="IFRS 17 Liabilities", style={"color": "darkblue"}),
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
                html.Div([], id="tableDiv", className="one-half column"),
                html.Div([], id="deathAnnuity", className="one-half column"),
            ],
            className="row",
        ),
    ]
)  # , style={'display': 'inline-block', 'width': '48%'})


# Step 5. Add callback functions
# @app.callback(Output('plot', 'figure'),
##             [Input('opt', 'value')])
# def update_figure(input1):
# selected_plots.append(go.Scatter(x=df_bond['StepDate'], y=df_bond[checked], name=str(checked + ", Bonds")))

# selected_plots.append(go.Scatter(x = df_bond['StepDate'], y = df_bond[checked],
#                name = checked,
#                line = dict(width = 2)))

#   fig = go.Figure(data = None, layout = layout)
#   return fig

# Command line entry point
if __name__ == "__main__":
    from waitress import serve

    # serve(server, host="0.0.0.0", port=5050)
    serve(app.server, listen="*:5051")
