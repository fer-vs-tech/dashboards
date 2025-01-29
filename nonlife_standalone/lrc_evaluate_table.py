import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.nonlife_standalone.db_helper as db_helper


def get_table(wvr_path):
    """
    Generic line chart using supplied model field name
    """
    handler = db_helper.LRCEvaluate()
    table_data_df = handler.get_wvr_data(wvr_path, "NL_LRC_Eval")

    # Table 1
    table_df1 = table_data_df[
        [
            "Product_Name",
            "Input_Variable",
            "Method Value",
            "Dist Value",
            "Fitted_Param_1",
            "Fitted_Param_2",
            "Input_Mean",
            "Risk_Adjustment",
            "Risk_Adjustment_Ratio",
        ]
    ]
    table_data1 = table_df1.to_dict("records")
    columns1 = dash_utils.set_column_names(table_df1.columns, precision=2)
    conditional_style1 = dash_utils.set_conditional_style(columns1)

    # Table 2
    table_df2 = table_data_df[
        [
            "Product_Name",
            "Input_Variable",
            "Method Value",
            "Dist Value",
            "Fitted_Param_1",
            "Fitted_Param_2",
            "AD_Test_Stat",
            "ADmod_AU_Test_Stat",
            "ChiSq_Test_Stat",
            "KS_Dn_Test_Stat",
        ]
    ]
    table_data2 = table_df2.to_dict("records")
    columns2 = dash_utils.set_column_names(table_df2.columns, precision=2)
    conditional_style2 = dash_utils.set_conditional_style(columns2)
    return (
        table_data1,
        columns1,
        conditional_style1,
        table_data2,
        columns2,
        conditional_style2,
    )
