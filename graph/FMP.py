import math
import textwrap

import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

import cm_dashboards.alchemy_db as db
import cm_dashboards.graph.FMP_sqls as query
from cm_dashboards.server import server

external_stylesheets = [
    "../static/css/fontawesome-all.min.css",
    "../static/css/main.css",
]

JOBRUN = ""
DB_URL = ""

markdown_text = """
## Notes: 
###### Dhipaya Life Assurance (“DLA”) has performed 1Q IFRS17 closing process with New business contracts of Credit Life issued during 1Q.
###### Closing process is calculated based on actual NB data as of Dec 31.
---
## Explanation on movement steps
1. ***NB WA Diff*** : For open cohort’s BEL diff arising from initial EIR and weighted averaged EIR  
2. ***Exp Prem***: Expected Premium  
3. ***Exp Claim (Ins)*** : Expected Claim (Insurance Component)  
4. ***Exp AC (prem)*** : Expected Acquisition Cost (Premium-related cost) such as Direct Commission  
5. ***Exp AC(non-prem)*** : Expected Acquisition Cost (Non-Premium related cost)  
6. ***Exp maint cost*** : Expected maintenance cost  
7. ***Exp PL CF*** : Expected Policy Loan Cash flow  
8. ***Unwinding*** : Interest expense accreted  
9. ***Vol adj***: Actual NB volume in March IF data  
10. ***Act assumpt*** : Actuarial Assumption update  
11. ***Eco assumpt*** : Discretionary change in ISP crediting rate’s margin (management decision)  
12. ***Disc rate*** : Economic Assumption update
"""

bar_df = None
pie_df = None
col_list = []
prem_ratio_as_percentage = []
pie_percent = []


app = dash.Dash(
    name="graph",
    server=server,
    url_base_pathname="/dash/graph/",
    # external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    update_title="Loading...",
    compress=server.config["COMPRESS_CONTENT"],
)


def serve_layout():
    GOC = []
    df_GOC = {}
    df_closing_dates = {}
    if len(DB_URL) != 0:
        df_GOC = db.query_to_dataframe(db.get_db_connection(DB_URL), query.gocs)
        df_closing_dates = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.closing_dates
        )

    if "GOC" in df_GOC:
        for group in df_GOC["GOC"]:
            GOC.append({"label": str(group), "value": group})

    def chkValidDates(df_dates, gocYear):
        vdates = []
        valid_dates = [date for date in df_dates if date.year >= gocYear]
        # print(valid_dates)
        for vdate in valid_dates:
            vdates.append({"label": str(vdate), "value": vdate})
        return vdates

    def findNumberFromGoc(str_goc):
        for ea in str_goc.split("_"):
            if ea.isnumeric() == True:
                # print(ea, "is a NUMBER!!!")
                return int(ea)

    # vdates = chkValidDates(df_closing_dates["closingDates"], findNumberFromGoc(init_GOC))
    vdates = []
    if "closingDates" in df_closing_dates:
        for vdate in df_closing_dates["closingDates"]:
            vdates.append({"label": str(vdate), "value": vdate})

    ##################### Goc Portion Initialization #####################
    global bar_df
    global pie_df

    bar_df = pd.read_csv("./data/bar.csv")
    pie_df = pd.read_csv("./data/pie.csv")

    bar_df = bar_df.set_index("type")
    pie_df = pie_df.set_index("type")

    global col_list
    col_list = bar_df.columns.tolist()
    bar_df_without_total = bar_df.drop(labels="Total NB GoC", axis=1)
    global prem_ratio_as_percentage
    prem_ratio_as_percentage = [
        str(p) + "%" for p in bar_df_without_total.iloc[7].astype(float).round(4) * 100
    ]
    global pie_percent
    pie_percent = (pie_df.iloc[0].astype(float) * 100).round(0).astype(int)

    GOC_value = ""
    if len(GOC) > 0:
        GOC_value = GOC[0]["label"]

    vdates_value = ""
    if len(vdates) > 0:
        vdates_value = vdates[0]["label"]

    return html.Div(
        [
            # represents the URL bar, doesn't render anything
            dcc.Location(id="url", refresh=False),
            html.Div(
                [
                    dcc.Input(id="jobrun", value="", type="hidden"),
                ]
            ),  # type="hidden"
            dcc.Tabs(
                id="tabs",
                value="movement",
                children=[
                    # 1st tab - Movement
                    dcc.Tab(
                        label="Movement",
                        value="movement",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=[
                            html.Div(
                                [
                                    html.Div(
                                        [  # 1st row. GName label, GName Dropbox + cDate label, cDate DropBox + button
                                            html.Div(
                                                [  # 1st column
                                                    html.Label(
                                                        "Choose a Group Name :",
                                                        style={"display": "block"},
                                                    ),
                                                    dcc.Dropdown(
                                                        id="goc-picker",
                                                        options=GOC,
                                                        value=GOC_value,
                                                    ),
                                                ],
                                                style={
                                                    "padding-bottom": "30px",
                                                },
                                                className="col-6",
                                            ),
                                            html.Div(
                                                [  # 2nd column
                                                    html.Label(
                                                        "Closing Date :",
                                                        style={"display": "block"},
                                                    ),
                                                    dcc.Dropdown(
                                                        id="closingDate-picker",
                                                        options=vdates,
                                                        value=vdates_value,
                                                        style={
                                                            "display": "block",
                                                            "margin-top": "10px",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "padding-bottom": "30px",
                                                    "display": "inline-block",
                                                },
                                                className="col-5",
                                            ),
                                            html.Div(
                                                [
                                                    html.Button(
                                                        id="submit-btn",
                                                        n_clicks=0,
                                                        children="Submit",
                                                        # style={
                                                        # },
                                                        className="button",
                                                    )
                                                ],
                                                style={
                                                    "padding-top": "30px",
                                                },
                                                className="col-1",
                                            ),
                                        ],
                                        className="row",
                                        style={"margin-top": "2rem"},
                                    ),
                                    html.Div(
                                        [  # row2
                                            html.Div(
                                                [  # Bel Col
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                config={
                                                                    "displaylogo": False
                                                                },
                                                                id="BEL",
                                                            )
                                                        ],
                                                        style={},
                                                    ),
                                                ],
                                                className="col-6",
                                            ),
                                            html.Div(
                                                [  # RA Col
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                config={
                                                                    "displaylogo": False
                                                                },
                                                                id="RA",
                                                            )
                                                        ],
                                                        style={},
                                                    ),
                                                ],
                                                className="col-6",
                                            ),
                                        ],
                                        style={},
                                        className="row",
                                    ),
                                    html.Div(
                                        [  # row3
                                            html.Div(
                                                [dcc.Markdown(children=markdown_text)],
                                                className="col-6 label",
                                            ),
                                            html.Div(
                                                [  # CSM column
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                config={
                                                                    "displaylogo": False
                                                                },
                                                                id="CSM",
                                                            )
                                                        ],
                                                        style={},
                                                    )
                                                ],
                                                style={},
                                                className="col-6",
                                            ),
                                        ],
                                        className="row",
                                    ),
                                ]
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Goc Portion",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        value="portion",
                        children=[
                            html.Div(
                                [
                                    html.Div(
                                        [  # 1st row. cDate label, cDate DropBox
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Closing Date :",
                                                        style={"display": "block"},
                                                    ),
                                                    dcc.Dropdown(
                                                        id="goc-portion-closing-date-picker",
                                                        options=vdates,
                                                        value=vdates_value,
                                                        style={
                                                            "display": "block",
                                                            "margin-top": "10px",
                                                        },
                                                    ),
                                                ],
                                                style={
                                                    "padding-bottom": "30px",
                                                    "display": "inline-block",
                                                },
                                                className="col-12",
                                            )
                                        ],
                                        className="row",
                                        style={"margin-top": "2rem"},
                                    ),
                                    html.Div(
                                        [  # row2
                                            html.Div(
                                                [  # Bel Contribution Col
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                config={
                                                                    "displaylogo": False
                                                                },
                                                                id="BEL-NB-Goc",
                                                            )
                                                        ],
                                                    ),
                                                ],
                                                className="col-4",
                                            ),
                                            html.Div(
                                                [  # RA Contribution Col
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                config={
                                                                    "displaylogo": False
                                                                },
                                                                id="RA-NB-Goc",
                                                            )
                                                        ],
                                                    ),
                                                ],
                                                className="col-4",
                                            ),
                                            html.Div(
                                                [  # CSM Contribution Col
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                config={
                                                                    "displaylogo": False
                                                                },
                                                                id="CSM-NB-Goc",
                                                            )
                                                        ],
                                                    ),
                                                ],
                                                className="col-4",
                                            ),
                                        ],
                                        style={},
                                        className="row",
                                    ),
                                    html.Div(
                                        [  # row3
                                            html.Div(
                                                [  # CSM / PV Prem ratio
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                id="CSM-over-PV-bar"
                                                            )
                                                        ],
                                                    ),
                                                ],
                                                className="col-6",
                                            ),
                                            html.Div(
                                                [  # CSM / PV Prem ratio
                                                    html.Div(
                                                        [
                                                            dcc.Graph(
                                                                id="CSM-over-PV-pie"
                                                            )
                                                        ],
                                                    ),
                                                ],
                                                className="col-6",
                                            ),
                                        ],
                                        style={},
                                        className="row",
                                    ),
                                ]
                            )
                        ],
                    ),
                ],
            ),
        ],
        className="container",
        style={"margin-top": "2%"},
    )


app.layout = serve_layout()


@app.callback(
    Output("jobrun", "value"),
    [Input("url", "search")],
)
def update_jobrun(input_jobrun):
    """
    Update the jobrun
    """

    global JOBRUN
    global DB_URL
    if input_jobrun:
        # TODO: Improve this
        JOBRUN = input_jobrun.split("?jobrun=")[1]
        print("Got JOBRUN: {0}".format(JOBRUN))
        DB_URL = db.get_db_connection_url(JOBRUN)
        print("Got DB_URL: {0}".format(DB_URL))
        # print("JOBRUN: ", JOBRUN)
    return JOBRUN


@app.callback(
    Output("CSM-over-PV-pie", "figure"),
    [Input("goc-portion-closing-date-picker", "value")],
)
def drawBELTotalNBGoc(gocSelected):
    return {
        "data": [
            go.Pie(
                labels=pie_df.columns,
                values=pie_percent,
                hoverinfo="label+percent",
            ),
        ],
        "layout": {
            "title": "CSM / PV Prem ratio",
            "hovermode": "closest",
            "xaxis": {"automargin": True},
        },
    }


@app.callback(
    Output("CSM-over-PV-bar", "figure"),
    [Input("goc-portion-closing-date-picker", "value")],
)
def drawBELTotalNBGoc(gocSelected):
    return {
        "data": [
            go.Bar(
                x=col_list[: len(col_list) - 1],
                y=bar_df.iloc[7],
                marker_color="royalblue",
                text=prem_ratio_as_percentage,
                textposition="auto",
            ),
        ],
        "layout": {
            "title": "CSM / PV Prem ratio (at SM date : 3/31)",
            "hovermode": "closest",
            "xaxis": {"automargin": True},
        },
    }


@app.callback(
    Output("BEL-NB-Goc", "figure"), [Input("goc-portion-closing-date-picker", "value")]
)
def drawBELTotalNBGoc(gocSelected):
    return {
        "data": [
            go.Bar(
                x=bar_df.index[:2],
                y=[
                    bar_df.loc["Beg BEL"]["Total NB GoC"],
                    bar_df.loc["End BEL"]["Total NB GoC"],
                ],
                marker_color="blueviolet",
            ),
        ],
        "layout": {
            "title": "BEL Contribution by NB GoC  (From IR to SM)",
            "hovermode": "closest",
            "xaxis": {"automargin": True},
        },
    }


@app.callback(
    Output("RA-NB-Goc", "figure"), [Input("goc-portion-closing-date-picker", "value")]
)
def drawBELTotalNBGoc(gocSelected):
    return {
        "data": [
            go.Bar(
                x=bar_df.index[2:4],
                y=[
                    bar_df.loc["Beg RA"]["Total NB GoC"],
                    bar_df.loc["End RA"]["Total NB GoC"],
                ],
                marker_color="burlywood",
            ),
        ],
        "layout": {
            "title": "RA Contribution by NB GoC  (From IR to SM)",
            "hovermode": "closest",
            # 'height' : 600,
            "xaxis": {"automargin": True},
        },
    }


@app.callback(
    Output("CSM-NB-Goc", "figure"), [Input("goc-portion-closing-date-picker", "value")]
)
def drawBELTotalNBGoc(gocSelected):
    return {
        "data": [
            go.Bar(
                x=bar_df.index[4:6],
                y=[
                    bar_df.loc["Beg CSM"]["Total NB GoC"],
                    bar_df.loc["End CSM"]["Total NB GoC"],
                ],
                marker_color="slategrey",
            ),
        ],
        "layout": {
            "title": "CSM Contribution by NB GoC  (From IR to SM)",
            "hovermode": "closest",
            # 'height' : 600,
            "xaxis": {"automargin": True},
        },
    }


# # Once a group name is chosen, closing dates equal to or greater than its year ONLY will be filled in as options
# @app.callback(Output("closingDate-picker", "options"), [Input("goc-picker", "value")])
# def fill_in_closingDates(gocSelected):
#     return vdates


def build_bel_RA_df(goc, date, which_graph):
    if which_graph == "bel":
        df_bal = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.BEL_beg_bal(JOBRUN, goc, date)
        )
        df_WAP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.BEL_WAP(JOBRUN, goc, date)
        )
        df_RDP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.BEL_RDP(JOBRUN, goc, date)
        )
        df_QDP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.BEL_QDP(JOBRUN, goc, date)
        )
        df_PAP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.BEL_PAP(JOBRUN, goc, date)
        )
        df_EBP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.BEL_EBP(JOBRUN, goc, date)
        )
        df_LossComp = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.BEL_LossComp(JOBRUN, goc, date)
        )
    else:  # RA
        df_bal = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.RA_beg_bal(JOBRUN, goc, date)
        )
        df_WAP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.RA_WAP(JOBRUN, goc, date)
        )
        df_RDP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.RA_RDP(JOBRUN, goc, date)
        )
        df_QDP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.RA_QDP(JOBRUN, goc, date)
        )
        df_PAP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.RA_PAP(JOBRUN, goc, date)
        )
        df_EBP = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.RA_EBP(JOBRUN, goc, date)
        )
        df_LossComp = db.query_to_dataframe(
            db.get_db_connection(DB_URL), query.RA_LossComp(JOBRUN, goc, date)
        )

    initial_vol = df_QDP["Vol adj"]
    initial_assumpt = df_PAP["Act assumpt"]
    Exp_Initial = df_WAP["cal"]
    del df_WAP["cal"]

    vol_adj = initial_vol - Exp_Initial - df_RDP["Act rate"]
    act_assumpt = initial_assumpt - initial_vol
    eco_assumpt = df_EBP["Eco assumpt"] - initial_assumpt

    df_merged = pd.concat([df_bal, df_WAP, df_RDP], axis=1)
    df_merged.insert(len(df_merged.columns), "Vol adj", vol_adj, True)
    df_merged.insert(len(df_merged.columns), "Act assumpt", act_assumpt, True)
    df_merged.insert(len(df_merged.columns), "Eco assumpt", eco_assumpt, True)
    df_merged = pd.concat([df_merged, df_LossComp], axis=1)
    # print(df_merged)
    del df_bal, df_WAP, df_RDP, df_QDP, df_PAP, df_EBP, df_LossComp

    return df_merged


def build_CSM_df(goc, date):
    df_CSM_bal = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.CSM_beg_bal(JOBRUN, goc, date)
    )
    df_CSM_WAP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.CSM_WAP(JOBRUN, goc, date)
    )
    df_CSM_Amor = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.CSM_AMOR(JOBRUN, goc, date)
    )

    df_merged = pd.concat([df_CSM_bal, df_CSM_WAP], axis=1)

    # For Vol adj
    df_BEL_QDP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.BEL_QDP(JOBRUN, goc, date)
    )  # Initial_BEL_Other_QDP_Proc
    df_BEL_Exp_Init_WAP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.BEL_Exp_Init_WAP(JOBRUN, goc, date)
    )  # Exp_Initial_BEL_Other_RSP_WAP_Proc
    df_BEL_RDP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.BEL_RDP(JOBRUN, goc, date)
    )  # Exp_BEL_Other_component_Diff_Actual_Rate_RDP_Proc
    df_RA_QDP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.RA_QDP(JOBRUN, goc, date)
    )  # Initial_RA_Other_QDP_Proc
    df_RA_Exp_Init_WAP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.RA_Exp_Init_WAP(JOBRUN, goc, date)
    )  # Exp_Initial_RA_Other_RSP_WAP_Proc
    df_RA_RDP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.RA_RDP(JOBRUN, goc, date)
    )  # Exp_RA_Other_component_Diff_Actual_Rate_RDP_Proc

    vol_adj_str = "Vol adj"
    act_rate_str = "Act rate"
    act_assumpt_str = "Act assumpt"
    eco_assumpt_str = "Eco assumpt"

    vol = (
        df_BEL_Exp_Init_WAP["cal"]
        + df_BEL_RDP[act_rate_str]
        - df_RA_QDP[vol_adj_str]
        + df_RA_Exp_Init_WAP["cal"]
        + df_RA_RDP[act_rate_str]
        - df_BEL_QDP[vol_adj_str]
    )

    # For Act assumpt
    df_bel_PAP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.BEL_PAP(JOBRUN, goc, date)
    )  # Initial_BEL_Other_PAP_Proc
    df_ra_PAP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.RA_PAP(JOBRUN, goc, date)
    )  # Initial_RA_Other_PAP_Proc

    # For Eco assumpt
    df_bel_EBP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.BEL_EBP(JOBRUN, goc, date)
    )  # Initial_BEL_Other_EBP_Proc
    df_bel_PAP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.BEL_PAP(JOBRUN, goc, date)
    )  # Initial_BEL_Other_PAP_Proc
    df_ra_EBP = db.query_to_dataframe(
        db.get_db_connection(DB_URL), query.RA_EBP(JOBRUN, goc, date)
    )  # Initial_RA_Other_EBP_Proc

    act_assumpt = (
        df_BEL_QDP[vol_adj_str]
        + df_RA_QDP[vol_adj_str]
        - df_ra_PAP[act_assumpt_str]
        - df_bel_PAP[act_assumpt_str]
    )
    eco_assumpt = (
        df_bel_PAP[act_assumpt_str]
        + df_ra_PAP[act_assumpt_str]
        - df_bel_EBP[eco_assumpt_str]
        - df_ra_EBP[eco_assumpt_str]
    )

    df_merged.insert(len(df_merged.columns), vol_adj_str, vol, True)
    df_merged.insert(len(df_merged.columns), act_assumpt_str, act_assumpt, True)
    df_merged.insert(len(df_merged.columns), eco_assumpt_str, eco_assumpt, True)

    df_merged = pd.concat([df_merged, df_CSM_Amor], axis=1)

    return df_merged


### remove data with value = 0  ###
def remove_data_with_zero(df):
    col_idx_list_with_zero = []
    [
        col_idx_list_with_zero.append(i)
        for v, i in zip(df.iloc[0], range(0, len(df.columns)))
        if v == 0 or math.isnan(v)
    ]
    df.drop(df.columns[col_idx_list_with_zero], axis=1, inplace=True)
    return df


### calculate end Balance and add it as the last column to df
def add_endbal_to_df(df):
    end_bal = round(sum(df.iloc[0].astype(float)), 2)
    df.insert(len(df.columns), "End Balance", end_bal, True)
    return df


### wrapping x-axis values for better look
def wrap_xaxis_properties(df):
    split_cols = []
    for c in df.columns:
        split_col = textwrap.wrap(c, width=20)
        split_col = "<br>".join(split_col)
        split_cols.append(split_col)
    return split_cols


def text_properties(df_float):
    text_list = df_float.tolist()  # remove the last column
    text_list = ["{:,.0f}".format(t) for t in text_list]
    text_list = ["+" + str(t) if not (t.startswith("-")) else t for t in text_list]

    last_value = text_list.pop()
    text_list.append("Total: " + last_value)
    return text_list


def measure_properties(df_float):
    measure = []
    [
        (
            measure.append("absolute")
            if m == 0
            else (
                measure.append("total")
                if m == df_float.index.size - 1
                else measure.append("relative")
            )
        )
        for m in range(0, df_float.index.size)
    ]
    return measure


@app.callback(
    Output("BEL", "figure"),
    Input("submit-btn", "n_clicks"),
    State("goc-picker", "value"),
    State("closingDate-picker", "value"),
)
def draw_Bel(n_clicks, gocSelected, dateSelected):
    if len(gocSelected) == 0 or len(dateSelected) == 0:
        return {}
    df = build_bel_RA_df(gocSelected, dateSelected, "bel")
    # print("df: ", df)
    df = remove_data_with_zero(df)
    df = add_endbal_to_df(df)
    df_float = df.iloc[0].astype(float).round(2)
    text_list = text_properties(df_float)
    measure = measure_properties(df_float)
    return {
        "data": [
            go.Waterfall(
                x=split_cols if "split_cols" in locals() else df.columns,
                y=df_float,
                text=text_list,
                textposition="outside",
                decreasing={
                    "marker": {
                        "color": "deepskyblue",
                    },
                },
                increasing={"marker": {"color": "orange"}},
                totals={"marker": {"color": "#50c878"}},
                measure=measure,
                connector={
                    "mode": "between",
                    "line": {
                        "color": "rgb(63, 63, 63)",
                        "dash": "dot",
                    },
                },
            )
        ],
        "layout": {
            "title": "BEL Movement",
            "hovermode": "closest",
            "height": 600,
            "xaxis": {"automargin": True},
        },
    }


@app.callback(
    Output("RA", "figure"),
    Input("submit-btn", "n_clicks"),
    State("goc-picker", "value"),
    State("closingDate-picker", "value"),
)
def draw_RA(n_clicks, gocSelected, dateSelected):
    if len(gocSelected) == 0 or len(dateSelected) == 0:
        return {}
    df = build_bel_RA_df(gocSelected, dateSelected, "RA")
    df = remove_data_with_zero(df)
    df = add_endbal_to_df(df)
    df_float = df.iloc[0].astype(float).round(2)
    text_list = text_properties(df_float)
    measure = measure_properties(df_float)

    return {
        "data": [
            go.Waterfall(
                x=split_cols if "split_cols" in locals() else df.columns,
                y=df_float,
                text=text_list,
                textposition="outside",
                decreasing={"marker": {"color": "deepskyblue"}},
                increasing={"marker": {"color": "orange"}},
                totals={"marker": {"color": "#50c878"}},
                measure=measure,
                connector={
                    "mode": "between",
                    "line": {
                        "color": "rgb(63, 63, 63)",
                        "dash": "dot",
                    },
                },
            )
        ],
        "layout": {
            "title": "RA Movement",
            "hovermode": "closest",
            "height": 600,
            "xaxis": {"automargin": True},
        },
    }


@app.callback(
    Output("CSM", "figure"),
    Input("submit-btn", "n_clicks"),
    State("goc-picker", "value"),
    State("closingDate-picker", "value"),
)
def draw_RA(n_clicks, gocSelected, dateSelected):
    if len(gocSelected) == 0 or len(dateSelected) == 0:
        return {}
    df = build_CSM_df(gocSelected, dateSelected)
    df = remove_data_with_zero(df)
    df = add_endbal_to_df(df)
    df_float = df.iloc[0].astype(float).round(2)
    text_list = text_properties(df_float)
    measure = measure_properties(df_float)

    return {
        "data": [
            go.Waterfall(
                x=split_cols if "split_cols" in locals() else df.columns,
                y=df_float,
                text=text_list,
                textposition="outside",
                decreasing={"marker": {"color": "deepskyblue"}},
                increasing={"marker": {"color": "orange"}},
                totals={"marker": {"color": "#50c878"}},
                measure=measure,
                connector={
                    "mode": "between",
                    "line": {
                        "color": "rgb(63, 63, 63)",
                        "dash": "dot",
                    },
                },
                cliponaxis=False,
            )
        ],
        "layout": {
            "title": "CSM Movement",
            "hovermode": "closest",
            "height": 600,
            "xaxis": {"automargin": True},
            "yaxis": {"automargin": True},
        },
    }
