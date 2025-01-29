import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.nonlife_standalone.db_helper as db_helper


def get_table(wvr_path, title):
    """
    Generic bar chart using supplied model field name
    """
    handler = db_helper.Parameterization()
    chart_data_df = handler.get_wvr_data(wvr_path, "NL_LRC_Fit")

    # Data cleaning - rename columns to match the model
    mme_data = chart_data_df[chart_data_df["Fitting_Method"] == 1]
    mle_data = chart_data_df[chart_data_df["Fitting_Method"] == 2]
    mle_data.rename(
        columns={
            "Dist Value": "Dist Value_MLE",
            "Distribution_LR": "Distribution_LR_MLE",
            "Fitting_Method": "Fitting_Method_MLE",
            "Fitted_Param_1": "Fitted_Param_1_MLE",
            "Fitted_Param_2": "Fitted_Param_2_MLE",
        },
        inplace=True,
    )

    # Get the only the columns we need
    mme_param_1 = mme_data["Fitted_Param_1"].to_list()
    mme_param_2 = mme_data["Fitted_Param_2"].to_list()
    mle_param_1 = mle_data["Fitted_Param_1_MLE"].to_list()
    mle_param_2 = mle_data["Fitted_Param_2_MLE"].to_list()

    # Create a dict with the parameters for each fitting method
    table_data_mme_1 = dash_utils.set_table_data(mme_param_1, "MME")
    table_data_mme_2 = dash_utils.set_table_data(mme_param_2, "MME")
    table_data_mle_1 = dash_utils.set_table_data(mle_param_1, "MLE")
    table_data_mle_2 = dash_utils.set_table_data(mle_param_2, "MLE")

    # Merge the two tables
    row_1 = {**table_data_mme_1, **table_data_mle_1}
    row_2 = {**table_data_mme_2, **table_data_mle_2}
    table_data = [row_1, row_2]

    # Create the table for each fitting method
    mme_columns = dash_utils.set_parameterization_column_names(
        mme_data, precision=4, show_negative_numbers=True, additional_header="MME"
    )
    mle_columns = dash_utils.set_parameterization_column_names(
        mle_data, precision=4, show_negative_numbers=True, additional_header="MLE"
    )
    # Merge columns
    columns = mme_columns + mle_columns
    return table_data, columns
