import plotly.express as px

import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.nonlife_standalone.db_helper as db_helper


def get_chart(wvr_path, title):
    """
    Generic bar chart using supplied model field name
    """
    handler = db_helper.LossRatio()
    chart_data_df = handler.get_wvr_data(wvr_path, "NL_LRC_Fit")

    try:
        chart = init_chart(title, chart_data_df, "Product_Name")
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, chart_data_df, "Product_Name")
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")

    table_data = chart_data_df.to_dict("records")
    columns = dash_utils.set_column_names(chart_data_df.columns, precision=4)
    conditional_style = dash_utils.set_conditional_style(columns)

    return chart, table_data, columns, conditional_style


def init_chart(title, chart_data_df, model_field):
    """
    Create dash bar object
    """
    return px.bar(
        data_frame=chart_data_df,
        x="Group_Identifier",
        y=[model_field],
        title=f"<b>{title}</b>",
        color_discrete_sequence=dash_utils.get_color_plate("bar"),
        template="cloud_manager",
        labels={"value": "Loss Ratio"},
    )
