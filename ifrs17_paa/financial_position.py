import pandas as pd

import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.wvr_data.wvr_functions as wvr_functions

SQL_POSITION = "Select Cash_Balance_Opening, '' as Cash_This_Year, Cash_Balance, '' as Insurance_Contract_Liability "

SQL_ASSET = (
    "Select Cash_Balance_Opening{section} as Cash_Balance_Opening, Cash_This_Year{section} as Cash_This_Year, "
    "'' as Cash_Balance, Insurance_Contract_Liability{section} as Insurance_Contract_Liability "
)

SQL_WHERE_CLAUSE = (
    "from [{table}] where [Grp_Onerous_Type Value] = {onerous_type} and [Inception_Year Value] = {inception_year} "
    "and [Model Value] = '{model}' and [Product_Name Value] = '{product}' and [Step Date] = '{step_date}'"
)


def get_data_from_wvr(
    wvr_path,
    model,
    table,
    onerous_type,
    inception_year,
    model_value,
    product,
    step_date,
):
    connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
    con = wvr_functions.get_connection(connect_string)
    formatted_where = SQL_WHERE_CLAUSE.format(
        table=table,
        onerous_type=onerous_type,
        inception_year=inception_year,
        model=model_value,
        product=product,
        step_date=step_date,
    )
    sql_query = SQL_POSITION + formatted_where
    position = pd.read_sql(
        sql_query.format(table=table),
        con,
    )
    sql_query = SQL_ASSET + formatted_where
    asset = pd.read_sql(
        sql_query.format(section="_Asset", table=table),
        con,
    )

    results = position.append([asset, position])
    con.close()
    print(results)
    trans = results.transpose().reset_index()
    # Set column headers
    trans.columns = ["Category", "Position", "ASSET", "LIABILITIES"]
    print(trans)
    return trans


def get_claim_costs_results_chart(wvr_path):
    table_data_df = get_data_from_wvr(
        wvr_path, model="IFRS_17_PAA", table="G_Portfolio"
    )

    table_data = table_data_df.to_dict("records")
    columns = dash_utils.set_column_names(table_data_df.columns)
    return table_data, columns
