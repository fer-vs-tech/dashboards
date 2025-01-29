MENU_MODELS = {"LIC Model": "nl_lic_model", "LRC Fit Model": "nl_lrc_fit", "LRC Eval Model": "nl_lrc_eval"}

# NL_RUN_OFF_SECTION = [
#     {'label': 'Incremental Values', 'value': 'Incremental Values'},
#     {'label': 'Cumulative Values', 'value': 'Cumulative Values'},
# ]

NL_RUN_OFF = [
    {'label': 'Incremental Pre-Inflation Adjustment', 'value': 'Incremental Pre-Inflation Adjustment', 'disabled': True},
    {'label': 'Paid Claims', 'value': 'Tri_Paid_Claims_By_Year_Pre_Infl'},
    {'label': 'Case Reserves', 'value': 'Tri_Case_Reserves_By_Year_Pre_Infl'},
    {'label': 'Incurred Claims', 'value': 'Tri_Claim_Costs_By_Year_Pre_Infl'},
    {'label': 'Incremental Values', 'value': 'Incremental', 'disabled': True},
    {'label': 'Paid Claims', 'value': 'Tri_Paid_Claims_By_Year'},
    {'label': 'Case Reserves', 'value': 'Tri_Case_Reserves_By_Year'},
    {'label': 'Incurred Claims', 'value': 'Tri_Claim_Costs_By_Year'},
    {'label': 'Cumulative Values', 'value': 'Cumulative', 'disabled': True},
    {'label': 'Paid Claims', 'value': 'Tri_Paid_Claims'},
    {'label': 'Case Reserves', 'value': 'Tri_Case_Reserves'},
    {'label': 'Incurred Claims', 'value': 'Tri_Claim_Costs'}
]
NL_DATA_ANALYSIS = [{"label": "Outlier Analysis", "value":"Outlier Analysis"}, {"label": "Trend Analysis", "value": "Trend Analysis"}]
NL_AGE_2_AGE = [
    {'label': "Pre Data Analysis", 'value': "pre-data-analysis"},
    {'label': "Post Data Analysis", 'value': "post-data-analysis"},
]
NL_DEV_FACTORS = [{"label": "Loss Dev Factors", "value": "Loss Dev Factors"}, {"label": "Ultimate Dev Factors", "value": "Ultimate Dev Factors"}]
NL_PROJ_RESULTS = ["Cumulative Incurred Claims Projected", "Incremental Incurred Claims Projected"]
NL_LIC_SUMMARY = ["Claim Costs Results"]


# NL_LIC_OPTIONS = {
#     "Run-Off Triangles" : NL_RUN_OFF,
#     "Data Analysis" : NL_DATA_ANALYSIS,
#     "Age-To-Age Factors": NL_AGE_2_AGE,
#     "Dev Factor": NL_DEV_FACTORS,
#     "Proj. Results": NL_PROJ_RESULTS,
#     "LIC Summary": NL_LIC_SUMMARY
# }

NL_RUN_OFF_SECTION = {
    'Incremental Values': NL_RUN_OFF,
    'Cumulative Values': NL_RUN_OFF,
}

NL_LIC_SECTIONS = {
    "Run-Off Triangles" : NL_RUN_OFF_SECTION,
    "Data Analysis" : NL_DATA_ANALYSIS,
    "Age-To-Age Factors": NL_AGE_2_AGE,
    "Dev Factor": NL_DEV_FACTORS,
    "Proj. Results": NL_PROJ_RESULTS,
    "LIC Summary": NL_LIC_SUMMARY
}

NL_LRC_FIT_SECTIONS = ["Option 1"]
NL_LRC_EVAL_SECTIONS = ["Option_1"]