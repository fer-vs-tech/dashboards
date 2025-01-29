import pandas as pd

import cm_dashboards.wvr_data.wvr_functions as wvr_functions

SQL_DD = "Select distinct [{field}] from [G_Portfolio]"


def get_dropdown_list_data(wvr_path, model, field_name):
    connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
    con = wvr_functions.get_connection(connect_string)
    sql_query = SQL_DD.format(field=field_name)
    results_df = pd.read_sql(sql_query, con)
    con.close()
    results_list = results_df[results_df.columns[0]].to_list()
    return results_list
