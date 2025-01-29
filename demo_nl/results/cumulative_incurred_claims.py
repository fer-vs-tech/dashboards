#cumulative_incurred_claims
import dash
import plotly.express as px

import cm_dashboards.demo_nl.utils.dash_utils as dash_utils
import cm_dashboards.demo_nl.utils.db_helper as db_helper
import cm_dashboards.demo_nl.utils.helpers as helpers


def get_chart(inputs, wvr_path, title):
    """
    Generic line chart using supplied model field name
    """
    wvr = wvr_path["nl_lic_model"]
    if wvr is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    handler = db_helper.CumulativeIncurred(inputs)
    chart_data_df = handler.get_wvr_data(wvr, "NL_LIC_Model")
    # print(chart_data_df)


    # NEW
    if inputs.component in (["Tri_Paid_Claims", "Tri_Case_Reserves", "Tri_Claim_Costs"]):
        force = [chart_data_df["Dev_Period_Position"].max(), chart_data_df["Origin_Period_Position"].max()]

    # FORMAT DATAFRAME TRIANGLE LIKE
    df_triangle = helpers.convert_df_to_triangle(chart_data_df, ['Origin_Period_Position'], ['Dev_Period_Position'], ['returnValue'], force)

    columni = []
    for i in range(1, len(df_triangle.columns) + 1):
        columni.append(f"Dev {i}")
    df_triangle.columns = columni
    df_triangle.insert(0, 'Origin', range(1, len(df_triangle) + 1))

    try:
        df = chart_data_df[chart_data_df.returnValue.notnull()]
        chart = init_chart(title, df, "returnValue")
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, df, "returnValue")
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")

    table_data = df_triangle.to_dict('records')
    columns = dash_utils.set_column_names(df_triangle.columns, precision=4)
    conditional_style = dash_utils.set_conditional_style(columns)





    # try:
    #     chart = init_chart(title, chart_data_df, "returnValue")
    # except:
    #     # A dash initialisation bug requires this double init
    #     chart = init_chart(title, chart_data_df, "returnValue")
    # chart.update_xaxes(type="category")
    # chart.update_yaxes(autotypenumbers="strict")

    # table_data_df = dash_utils.pivot_data(
    #     chart_data_df,
    #     "Dev_Period_Position",
    #     "Origin_Period_Position",
    #     "Ult_Dev_Factors",
    # )

    # # print(table_data_df)
    # table_data = table_data_df.to_dict("records")
    # columns = dash_utils.set_column_names(table_data_df.columns, precision=4)
    # conditional_style = dash_utils.set_conditional_style(columns)

    return chart, table_data, columns, conditional_style



def init_chart(title, chart_data_df, model_field):
    """
    Create dash chart object
    """
    chart = px.line(
        chart_data_df,
        x="Dev_Period_Position",
        y=model_field,
        color="Origin_Period_Position",
        title=f"<b>{title}</b>",
        markers=True,
        color_discrete_sequence=dash_utils.get_color_plate("line"),
        #template="cloud_manager",
        labels={"Val": "Origin_Period_Position"},
    )

    legend_names = rename_lagends()

    chart.for_each_trace(
        lambda trace: trace.update(name=legend_names.get(trace.name, trace.name)),
    )

    return chart

def rename_lagends(legends_dict=None):
    """
    Helper function to rename legends to match the ones in the template
    """

    default = {
        "Dev_Period_Position": "Dev Period",
        "Origin_Period_Position": "Origin Period",
        "returnValue": "Value"
    }

    # Get kwargs
    if legends_dict is None:
        return default

    return {**default, **legends_dict}