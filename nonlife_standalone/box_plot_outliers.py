import plotly.express as px

import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.nonlife_standalone.db_helper as db_helper


def get_chart(wvr_path, title):
    """
    Generic box chart using supplied model field name
    """
    handler = db_helper.BoxPlotOutliers()
    chart_data_df = handler.get_wvr_data(wvr_path, "NL_LIC_Model")
    # print(chart_data_df)

    try:
        chart = init_chart(title, chart_data_df, "Age_To_Age_Factors_Pre_Outliers")
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, chart_data_df, "Age_To_Age_Factors_Pre_Outliers")
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")

    table_data = chart_data_df.to_dict("records")
    columns = dash_utils.set_column_names(chart_data_df.columns, precision=3)
    conditional_style = dash_utils.set_conditional_style(columns)

    return chart, table_data, columns, conditional_style


def init_chart(title, chart_data_df, model_field):
    """
    Create dash box object
    """
    return px.box(
        data_frame=chart_data_df,
        x="Dev_Period_Position",
        y=[
            "Age_To_Age_Factors_Outliers_Top",
            "Age_To_Age_Factors_Outliers_Bottom",
            "Age_To_Age_Factors_Outliers_Percentile_25",
            "Age_To_Age_Factors_Outliers_Percentile_50",
            "Age_To_Age_Factors_Outliers_Percentile_75",
        ],
        color="Dev_Period_Position",
        title=f"<b>{title}</b>",
        notched=True,
        # points="all",
        hover_data=[model_field],
        color_discrete_sequence=dash_utils.get_color_plate("line"),
        template="cloud_manager",
        labels={"value": "Age_To_Age_Factors_Mean_Pre_Outliers"},
    )
