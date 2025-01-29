import pandas as pd

import cm_dashboards.ifrs17_paa.dash_utils as dash_utils


def reconcile_pl_table(raw_df):
    # Set the Category of the index so we can reference it when looking up fields
    df = raw_df.set_index("Category")
    reconcile_pl_df = pd.DataFrame(
        [
            {
                "Category": "Opening Balance",
                "LRC": df.at["Opening_Balance", "DiscCF"],
                "LossComp of LRC": df.at["Opening_Balance", "LossComp"],
                "LIC": df.at["Opening_Balance", "RA"]
                + df.at["Opening_Balance", "IncClaim"],
                "Insurance Contract Liability": df.at[
                    "Opening_Balance", "Insurance Contract Liability"
                ],
            },
            {
                "Category": "Cash Inflows",
                "LRC": df.at["CF_Premium_Total", "Insurance Contract Liability"],
                "LossComp of LRC": "",
                "LIC": "",
                "Insurance Contract Liability": df.at[
                    "CF_Premium_Total", "Insurance Contract Liability"
                ],
            },
            {
                "Category": "Insurance Contract Revenue",
                "LRC": -df.at["Insurance_Contract_Revenue", "DiscCF"]
                + df.at["Amortized_DAC", "DiscCF"],
                "LossComp of LRC": "",
                "LIC": 0,
                "Insurance Contract Liability": -df.at[
                    "Insurance_Contract_Revenue", "DiscCF"
                ]
                + df.at["Amortized_DAC", "DiscCF"],
            },
            {
                "Category": "Insurance service expenses - onerous",
                "LRC": "",
                "LossComp of LRC": "",
                "LIC": -df.at["Insurance_Service_Related_Result", "RA"]
                - df.at["Insurance_Service_Related_Result", "IncClaim"],
                "Insurance Contract Liability": -df.at[
                    "Insurance_Service_Related_Result", "RA"
                ]
                - df.at["Insurance_Service_Related_Result", "IncClaim"],
            },
            {
                "Category": "Insurance service expenses - inc exp",
                "LRC": "",
                "LossComp of LRC": df.at["Loss_On_Onerous_Group", "LossComp"],
                "LIC": "",
                "Insurance Contract Liability": df.at[
                    "Loss_On_Onerous_Group", "LossComp"
                ],
            },
            {
                "Category": "BBA: ins finance expenses / VFA: Change in Fair Value",
                "LRC": df.at["Insurance_Finance_Expenses", "DiscCF"],
                "LossComp of LRC": df.at["Insurance_Finance_Expenses", "LossComp"],
                "LIC": df.at["Insurance_Finance_Expenses", "RA"]
                - df.at["Insurance_Finance_Expenses", "IncClaim"],
                "Insurance Contract Liability": df.at[
                    "Insurance_Finance_Expenses", "Insurance Contract Liability"
                ],
            },
        ]
    )
    reconcile_pl_df.loc["Closing Balance"] = reconcile_pl_df.replace("", 0).sum(
        numeric_only=True, axis=0
    )
    reconcile_pl_df.at["Closing Balance", "Category"] = "Closing Balance"
    print(reconcile_pl_df)

    pl_table_data = reconcile_pl_df.to_dict("records")
    pl_columns = dash_utils.set_column_names(reconcile_pl_df.columns)
    return pl_table_data, pl_columns
