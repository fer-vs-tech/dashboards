import plotly.express as px

import cm_dashboards.helpers as helpers
import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.nonlife_standalone.db_helper as db_helper


def get_chart(wvr_path, title):
    """
    Generic bar chart using supplied model field name
    """
    handler = db_helper.ClaimsDataLossRatio()
    chart_data_df = handler.get_wvr_data(wvr_path, "NL_LRC_Fit")
    data_source_data_df = helpers.parse_string_series_as_dataframe(
        chart_data_df["Source_Data_St"][0]
    )
    print(data_source_data_df.columns)
    try:
        chart = init_chart(title, data_source_data_df, "Year")
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, data_source_data_df, "Year")
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")

    table_data = data_source_data_df.to_dict("records")
    print(table_data)
    columns = dash_utils.set_column_names(
        data_source_data_df.columns, precision=4, show_negative_numbers=True
    )
    conditional_style = dash_utils.set_conditional_style(columns)

    return chart, table_data, columns, conditional_style


def init_chart(title, chart_data_df, model_field):
    """
    Create dash bar object
    """
    return px.bar(
        data_frame=chart_data_df,
        x="Year",
        y=["Value"],
        title=f"<b>{title}</b>",
        hover_data=[model_field],
        color_discrete_sequence=dash_utils.get_color_plate("bar"),
        template="cloud_manager",
        labels={"value": "Claims Data and Loss Ratio"},
    )
