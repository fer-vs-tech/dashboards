import pandas as pd
import plotly.express as px

import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.wvr_data.wvr_functions as wvr_functions


def get_data_from_wvr(wvr_path, model, x, y, model_field, table, grouping_id):
    """
    Extract data from .wvr file
    """
    connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
    con = wvr_functions.get_connection(connect_string)
    results = pd.read_sql(
        "Select {0}, {1}, {2} from [{3}] where Grouping_ID = '{4}'".format(
            y, x, model_field, table, grouping_id
        ),
        con,
    )
    con.close()
    # print(results)
    table_data = dash_utils.pivot_data(results, x, y, model_field)

    return results, table_data


def get_chart(wvr_path, title, model_field):
    """
    Generic line chart using supplied model field name
    """
    chart_data_df, table_data_df = get_data_from_wvr(
        wvr_path,
        "NL_LIC_Model",
        x="Dev_Period_Position",
        y="Origin_Period_Position",
        model_field=model_field,
        table="I_Data_Chain_Ladder",
        grouping_id="Grp1_BCL",
    )

    try:
        chart = init_chart(title, chart_data_df, model_field)
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, chart_data_df, model_field)
    chart.update_xaxes(type="category")
    chart.update_yaxes(autotypenumbers="strict")
    chart.update_traces(patch={"line": {"dash": "dot"}})

    table_data = table_data_df.to_dict("records")
    columns = dash_utils.set_column_names(table_data_df.columns)
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
