import plotly.express as px

import cm_dashboards.demo_nl.utils.dash_utils as dash_utils
import cm_dashboards.demo_nl.utils.db_helper as db_helper


def get_chart(wvr_path, title):
    """
    Generic line chart using supplied model field name
    """
    wvr = wvr_path["nl_lic_model"]
    handler = db_helper.UltimateDevelopmentFactorsCumulative()
    chart_data_df = handler.get_wvr_data(wvr, "NL_LIC_Model")
    # print(chart_data_df)

    try:
        chart = init_chart(title, chart_data_df, "Ult_Dev_Factors")
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, chart_data_df, "Ult_Dev_Factors")
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")

    table_data_df = dash_utils.pivot_data(
        chart_data_df,
        "Dev_Period_Position",
        "Origin_Period_Position",
        "Ult_Dev_Factors",
    )
    # print(table_data_df)
    table_data = table_data_df.to_dict("records")
    columns = dash_utils.set_column_names(table_data_df.columns, precision=4)
    conditional_style = dash_utils.set_conditional_style(columns)

    return chart, table_data, columns, conditional_style


def init_chart(title, chart_data_df, model_field):
    """
    Create dash chart object
    """
    return px.line(
        chart_data_df,
        x="Dev_Period_Position",
        y=model_field,
        color="Origin_Period_Position",
        title=f"<b>{title}</b>",
        markers=True,
        color_discrete_sequence=dash_utils.get_color_plate("line"),
        template="cloud_manager",
        labels={"Val": "Origin_Period_Position"},
    )
