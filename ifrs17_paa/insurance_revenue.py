import pandas as pd

import cm_dashboards.ifrs17_paa.dash_utils as dash_utils
import cm_dashboards.wvr_data.wvr_functions as wvr_functions


def insurance_revenue_table(raw_df):
    # Set the Category of the index so we can reference it when looking up fields
    df = raw_df.set_index("Category")
    insurance_revenue_df = pd.DataFrame(
        [
            {
                "Category": "Insurance service expenses incurred",
                "Value": df.at[
                    "Insurance_Contract_Revenue", "Insurance Contract Liability"
                ],
            },
            {
                "Category": "Contractual service margin recognised in profit or loss",
                "Value": 0,
            },
            {
                "Category": "Change in the risk adjustment for non-financial risk caused by the release from risk",
                "Value": -dash_utils.string_to_int(
                    df.at["Insurance_Contract_Revenue", "RA"]
                ),
            },
            {
                "Category": "Allocation of recovery of insurance acquisition cash flows",
                "Value": -df.at["Amortized_DAC", "Insurance Contract Liability"],
            },
        ]
    )
    insurance_revenue_df.loc["Insurance Revenue"] = insurance_revenue_df.replace(
        "", 0
    ).sum(numeric_only=True, axis=0)
    insurance_revenue_df.at["Insurance Revenue", "Category"] = "Insurance Revenue"

    insurance_revenue_df.loc["Contractual service Margin"] = [
        "Contractual service Margin",
        0,
    ]

    return insurance_revenue_df


SQL_CF_EXPENSE = (
    "Select CF_Expense_Directly_Attributable_PL "
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
    sql_query = SQL_CF_EXPENSE.format(
        table=table,
        onerous_type=onerous_type,
        inception_year=inception_year,
        model=model_value,
        product=product,
        step_date=step_date,
    )
    cf_expense = pd.read_sql(
        sql_query,
        con,
    )
    con.close()
    return cf_expense["CF_Expense_Directly_Attributable_PL"].values[0]
