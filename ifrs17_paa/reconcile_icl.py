import pandas as pd

import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.wvr_data.wvr_functions as wvr_functions

SQL_DISC_CF = (
    "Select Disc_CF_Opening as Opening_Balance, Non_Insurance_Related_Result{section} as Non_Insurance_Related_Result, CF_Premium_Total, CF_Expense_Directly_Attributable{section} as CF_Expense_Directly_Attributable, "
    "'' as Outgo_Total_Paid, '' as Experience_Adj_LIC_Paid, Insurance_Finance_Expenses{section} as Insurance_Finance_Expenses, "
    "Insurance_Service_Related_Result{section} as Insurance_Service_Related_Result, '' as Insurance_Service_Expenses, '' as Incurred_Claims_and_Expenses, "
    "'' as Reserve_IBNR, Insurance_Contract_Revenue, Amortized_DAC, '' as Loss_On_Onerous_Group, Disc_CF as Closing_Balance "
)

SQL_RA = (
    "Select Risk_Adjustment_Opening as Opening_Balance, Non_Insurance_Related_Result{section} as Non_Insurance_Related_Result, '' as CF_Premium_Total, '' as CF_Expense_Directly_Attributable, "
    "Outgo_Total_Paid{section} as Outgo_Total_Paid, '' as Experience_Adj_LIC_Paid, Insurance_Finance_Expenses{section} as Insurance_Finance_Expenses, "
    "Insurance_Service_Related_Result{section} as Insurance_Service_Related_Result, Insurance_Service_Expenses{section} as Insurance_Service_Expenses, '' as Incurred_Claims_and_Expenses, "
    "'' as Reserve_IBNR, '' as Insurance_Contract_Revenue, '' as Amortized_DAC, '' as Loss_On_Onerous_Group, Risk_Adjustment as Closing_Balance "
)

SQL_LOSS_COMP = (
    "Select Loss_Component_Opening as Opening_Balance, Non_Insurance_Related_Result{section} as Non_Insurance_Related_Result, '' as CF_Premium_Total, '' as CF_Expense_Directly_Attributable, "
    "'' as Outgo_Total_Paid, '' as Experience_Adj_LIC_Paid, Insurance_Finance_Expenses{section} as Insurance_Finance_Expenses, "
    "Insurance_Service_Related_Result{section} as Insurance_Service_Related_Result, '' as Insurance_Service_Expenses, '' as Incurred_Claims_and_Expenses, "
    "'' as Reserve_IBNR, '' as Insurance_Contract_Revenue, '' as Amortized_DAC, Loss_On_Onerous_Group{section} as Loss_On_Onerous_Group, Loss_Component as Closing_Balance "
)

SQL_INC_CLAIM = (
    "Select Liability_Incurred_Claims_Opening as Opening_Balance, Non_Insurance_Related_Result{section} as Non_Insurance_Related_Result, '' as CF_Premium_Total, '' as CF_Expense_Directly_Attributable, "
    "Outgo_Total_Paid - Experience_Adj_LIC_Paid as Outgo_Total_Paid, Experience_Adj_LIC_Paid, Insurance_Finance_Expenses{section} as Insurance_Finance_Expenses, "
    "Insurance_Service_Related_Result{section} as Insurance_Service_Related_Result, '' as Insurance_Service_Expenses, Incurred_Claims_and_Expenses, "
    "Reserve_IBNR, '' as Insurance_Contract_Revenue, '' as Amortized_DAC, '' as Loss_On_Onerous_Group, Liability_Incurred_Claims as Closing_Balance "
)

SQL_INS_CONTRACT_LIAB = (
    "Select Insurance_Contract_Liability_Opening as Opening_Balance, Non_Insurance_Related_Result{section} as Non_Insurance_Related_Result, CF_Premium_Total{section} as CF_Premium_Total, CF_Expense_Directly_Attributable{section} as CF_Expense_Directly_Attributable, "
    "Outgo_Total_Paid{section} as Outgo_Total_Paid, Experience_Adj_LIC_Paid{section} as Experience_Adj_LIC_Paid, Insurance_Finance_Expenses{section} as Insurance_Finance_Expenses, "
    "Insurance_Service_Related_Result{section} as Insurance_Service_Related_Result, Insurance_Service_Expenses{section} as Insurance_Service_Expenses, Incurred_Claims_and_Expenses{section} as Incurred_Claims_and_Expenses, "
    "Reserve_IBNR{section} as Reserve_IBNR, Insurance_Contract_Revenue{section} as Insurance_Contract_Revenue, Amortized_DAC{section} as Amortized_DAC, Loss_On_Onerous_Group{section} as Loss_On_Onerous_Group, Insurance_Contract_Liability as Closing_Balance "
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
    sql_query = SQL_DISC_CF + formatted_where
    disc_cf = pd.read_sql(
        sql_query.format(section="_DiscCF", table=table),
        con,
    )
    sql_query = SQL_RA + formatted_where
    ra = pd.read_sql(
        sql_query.format(section="_RA", table=table),
        con,
    )
    sql_query = SQL_LOSS_COMP + formatted_where
    losscomp = pd.read_sql(
        sql_query.format(section="_LossComp", table=table),
        con,
    )
    sql_query = SQL_INC_CLAIM + formatted_where
    incclaim = pd.read_sql(
        sql_query.format(section="_IncClaim", table=table),
        con,
    )
    sql_query = SQL_INS_CONTRACT_LIAB + formatted_where
    contract_liab = pd.read_sql(
        sql_query.format(section="", table=table),
        con,
    )

    results = disc_cf.append([ra, losscomp, incclaim, contract_liab])
    con.close()
    print(results)
    trans = results.transpose().reset_index()
    # Set column headers
    trans.columns = [
        "Category",
        "DiscCF",
        "RA",
        "LossComp",
        "IncClaim",
        "Insurance Contract Liability",
    ]
    print(trans)
    return trans


def get_claim_costs_results_chart(wvr_path):
    table_data_df = get_data_from_wvr(
        wvr_path, model="IFRS_17_PAA", table="G_Portfolio"
    )

    table_data = table_data_df.to_dict("records")
    columns = dash_utils.set_column_names(table_data_df.columns)
    return table_data, columns
