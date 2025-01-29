import pandas as pd
import plotly.express as px
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.nonlife_standalone.db_helper as db_helper


def get_chart(wvr_path, title):
    """
    Generic line chart using supplied model field name
    """
    handler = db_helper.ClaimCostsPaidStatus()
    chart_data_df = handler.get_wvr_data(wvr_path, "NL_LIC_Model")
    #print(chart_data_df)

    try:
        chart = init_chart(title, chart_data_df, "Claim_Costs_Summary")
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, chart_data_df, "Claim_Costs_Summary")
    for bar in chart.data:
        bar.width = 0.5
    
    # Add sum of rows
    chart_data_df.loc[:,"Total"]= chart_data_df.drop("Origin_Period_Position", 1).sum(numeric_only=True, axis=1)
    chart_data_df.loc["Total"]= chart_data_df.set_index("Origin_Period_Position").sum(numeric_only=True, axis=0)
    chart_data_df.iloc[-1, chart_data_df.columns.get_loc('Origin_Period_Position')] = "Total"
    
    table_data = chart_data_df.to_dict("records")
    columns = dash_utils.set_column_names(chart_data_df.columns, precision=0)
    conditional_style = dash_utils.set_conditional_style(columns)
    
    return chart, table_data, columns, conditional_style


def init_chart(title, chart_data_df, model_field):
    """
    Create dash chart object
    """
    return px.bar(
        data_frame=chart_data_df,
        x="Origin_Period_Position",
        y=["Claim_Paid_By_Origin", model_field],
        title=f"<b>{title}</b>",
        width=1100,
        # height=600,
        text_auto="0.2s",
        barmode="stack",
        color_discrete_sequence=dash_utils.get_color_plate("bar"),
        template="cloud_manager",
        # text=["Claim_Paid_By_Origin", model_field],
        labels={"value": "Caim Costs Summary", "variable": "Categories"}, 
    )