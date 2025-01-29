import plotly.express as px

import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.nonlife_standalone.db_helper as db_helper


def get_chart(wvr_path, title):
    """
    Generic line chart using supplied model field name
    """
    handler = db_helper.CumulativeIncuredClaimsProjectedPostFutureInflationAdj()
    chart_data_df = handler.get_wvr_data(wvr_path, "NL_LIC_Model")
    # print(chart_data_df)

    try:
        chart = init_chart(title, chart_data_df, "Tri_Claim_Costs_Proj")
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, chart_data_df, "Tri_Claim_Costs_Proj")
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")
    chart.update_traces(patch={"line": {"dash": "dot", "width": 2}})

    table_data_df = dash_utils.pivot_data(
        chart_data_df,
        "Dev_Period_Position",
        "Origin_Period_Position",
        "Tri_Claim_Costs_Proj",
    )
    # print(table_data_df)
    table_data = table_data_df.to_dict("records")
    columns = dash_utils.set_column_names(table_data_df.columns, precision=0)
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
        # line_dash=model_field,
        color_discrete_sequence=dash_utils.get_color_plate("line"),
        template="cloud_manager",
        labels={"value": "Origin_Period_Position"},
    )
