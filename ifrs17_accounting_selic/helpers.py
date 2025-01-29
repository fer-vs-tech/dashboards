import math

import pandas as pd

import cm_dashboards.ifrs17_accounting.dash_utils as dash_utils


def get_df(handler, wvr_path, model="journal"):
    """
    Get table data from wvr
    """
    models = {
        "mapping": "IFRS17_Accounting_Mapping",
        "journal": "IFRS17_Accounting_Journal",
    }

    table_data_df = handler.get_wvr_data(wvr_path, models[model])
    return table_data_df


def prepare_table_data(table_data_df, hidden_columns=[]):
    table_data = table_data_df.to_dict("records")
    columns = dash_utils.set_column_names(
        table_data_df.columns, precision=2, hidden_columns=hidden_columns
    )
    conditional_style = dash_utils.set_conditional_style(columns)
    return table_data, columns, conditional_style


def pivot_data(df):
    """
    Rotate data
    """
    result = df.transpose().reset_index()
    result.set_index("index", inplace=True)
    return result


def set_value(df, column_name, apply_formatter=True):
    """
    Set value to column
    """
    result = None
    try:
        result = df[column_name].iloc[0]
    except IndexError:
        result = 0
    if apply_formatter:
        return formatter(result)
    return result


def set_value_by_checking(IF_df, NB_df, category_id, column_name, apply_formatter=True):
    """
    Set value by checking
    """
    result = None
    try:
        if category_id == "IF":
            result = IF_df[column_name].iloc[0]
        elif category_id == "NB":
            result = NB_df[column_name].iloc[0]
        else:
            result = 0
    except IndexError:
        result = 0
    if apply_formatter:
        return formatter(result)
    return result


def set_link(df, url_path, journal_type, name):
    """
    Set download link
    """
    # Adjust URL path
    if url_path is None:
        url_path = "?"
    else:
        url_path = url_path + "&"

    # Set link according to name
    if name == "View":
        default_view_path = "journal_view"
        # Set view link according to journal type
        if journal_type in ["primary_general_paa", "reinsurance_general_paa"]:
            default_view_path = "journal_view_paa"
        link = f"[{name}]({default_view_path}/{url_path}journal_type={journal_type}&company_id={df.GoC_Name})"
    elif name == "Download":
        link = f"[{name}](download/{journal_type}/all/{df.GoC_Name}/)"
    else:
        link = f"{name}"
    return link


def prepere_checking(count_num):
    """
    Prepare checking
    """
    # Initialization
    temp_list = []
    keys = {
        "NB": [],
        "IF": [],
    }

    # Generate list of grouped numbers [1,2], [3,4], [5,6] ...
    for i in range(1, count_num, 2):
        temp_list.append([i, i + 1])

    # Store IF and NB numbers in separate lists
    for i, val in enumerate(temp_list):
        if i % 2 == 0:
            keys["IF"].append(val)
        else:
            keys["NB"].append(val)

    # Flat nested list
    keys["NB"] = [j for i in keys["NB"] for j in i]
    keys["IF"] = [j for i in keys["IF"] for j in i]

    return keys


def formatter(x):
    try:
        # if isinstance(x, int): return x
        x = math.ceil(x * 100) / 100
        # x = -0 if x == -0.0 else x
        return x
    except:
        return x


def create_header_data(header_df):
    """
    Create header dataframe from dict
    """
    header_dict = header_df.transpose().to_dict()
    details = {
        "Posting_Key": ["H"],
        "Record_Type": ["SA"],
        "COA": [2020],
        "Special_GL": [header_dict["Document_Date"]],
        "Amount": [header_dict["Posting_Date"]],
        "Base_Amount": ["THB"],
        "Tax_Code": [""],
        "BaseLine_Date": [header_dict["Document_Header_Text"]],
        "Payment_Term": ["0000"],
    }
    df = pd.DataFrame(details)
    df = adjust_cell_data_length(df, flag="HEADER")
    return df


def create_footer_data(summary_df):
    """
    Create footer dataframe from dict
    """
    summary_dict = summary_df.transpose().to_dict()
    print(summary_dict)
    details = {
        "Posting_Key": ["E", "F"],
        "Record_Type": [1, 1],
        "COA": [2, 2],
        "Special_GL": [
            summary_dict["Debit"]["Amount"],
            summary_dict["Credit"]["Amount"],
        ],
        "Amount": [summary_dict["Debit"]["Amount"], summary_dict["Credit"]["Amount"]],
    }
    df = pd.DataFrame(details)
    df = adjust_cell_data_length(df, flag="FOOTER")
    return df


def join_header_to_body(df, header_df):
    """
    Join two dataframes
    """
    # Add empty rows (2 rows)
    # header_df = header_df.reindex(header_df.index.tolist() + [header_df.index.max() + 1] * 2)
    result = pd.concat([header_df, df], ignore_index=True)
    return result


def join_footer_to_body(df, footer_df):
    """
    Join two dataframes
    """
    # Add empty rows (2 rows)
    # df = df.reindex(df.index.tolist() + [df.index.max() + 1] * 2)
    result = pd.concat([df, footer_df], ignore_index=True)
    return result


def prepere_df_for_download(df):
    """
    Prepare dataframe
    """
    # ['Posting_Key', 'Record_Type', 'COA', 'Amount', 'Assignment', 'Account_Description', 'Reference_Key_2', 'Underwriting_Year']
    column_name_and_index_dict = {
        "Special_GL": 3,
        "Base_Amount": 5,
        "Tax_Code": 6,
        "BaseLine_Date": 7,
        "Payment_Term": 8,
        "Payment_Method": 9,
        "Reference_Key_1": 12,
        "Reference_Key_3": 14,
        "Cost_Center": 15,
        "Internal_Order": 16,
        "Profit_Center": 17,
        "Branch": 18,
        "Contract_Group": 19,
        "Contract_Type": 21,
        "Business_Type": 23,
        "Agent_Broker": 24,
        "FAC": 25,
        "Handle": 26,
        "Fac_Treaty_CO": 27,
    }

    # Data cleaning
    df.rename(
        columns={
            "Total_Amount": "Amount",
            "PTFLO": "Reference_Key_2",
            "PTFLO_2": "Contract_Class",
            "COHT": "Underwriting_Year",
            "GOC": "Assignment",
        },
        inplace=True,
    )
    df.drop(columns=["Journal_Variables"], inplace=True)
    df["Underwriting_Year"] = df["Underwriting_Year"].astype(int)

    # Change column indexes
    df = df[
        [
            "Posting_Key",
            "Record_Type",
            "COA",
            "Amount",
            "Assignment",
            "Account_Description",
            "Reference_Key_2",
            "Contract_Class",
            "Underwriting_Year",
        ]
    ]
    # Set new column names
    for column_name, index in column_name_and_index_dict.items():
        # Standard column values as required by the template
        if column_name in ["Reference_Key_1", "Reference_Key_3"]:
            value = "NA"
        elif column_name == "Profit_Center":
            value = "2000-0000"
        else:
            value = ""
        df.insert(index, column_name, value)

    return df


def adjust_cell_data_length(df, flag="BODY"):
    """
    Adjust cell data length
    """
    default_columns = [
        "Posting_Key",
        "Record_Type",
        "COA",
        "Special_GL",
        "Amount",
        "Base_Amount",
        "Tax_Code",
        "BaseLine_Date",
        "Payment_Term",
        "Payment_Method",
        "Assignment",
        "Account_Description",
        "Reference_Key_1",
        "Reference_Key_2",
        "Reference_Key_3",
        "Cost_Center",
        "Internal_Order",
        "Profit_Center",
        "Branch",
        "Contract_Group",
        "Contract_Class",
        "Contract_Type",
        "Underwriting_Year",
        "Business_Type",
        "Agent_Broker",
        "FAC",
        "Handle",
        "Fac_Treaty_COde",
    ]

    default_length = [
        1,
        2,
        10,
        1,
        16,
        16,
        2,
        8,
        4,
        1,
        18,
        50,
        12,
        12,
        20,
        10,
        12,
        10,
        2,
        3,
        3,
        3,
        4,
        2,
        8,
        4,
        5,
        1,
    ]

    if flag == "BODY":
        cell_length = default_length
    elif flag == "HEADER":
        cell_length = [1, 2, 4, 8, 8, 4, 16, 25, 4]
    elif flag == "FOOTER":
        cell_length = [1, 10, 10, 20, 20]
    else:
        cell_length = default_length

    # Replace NaN values with empty space
    # df.replace(np.NaN, " ", inplace=True)

    # Adjust column data length
    if flag == "BODY":
        df["Account_Description"] = df["Account_Description"].apply(lambda x: x[0:50])

    # Create dictionary with column names and cell length
    columns = df.columns.values.tolist()
    cell_length_dict = dict(zip(columns, cell_length))
    for column in columns:
        df[column] = df[column].astype(str).str.ljust(cell_length_dict[column])

    # df.to_csv(f'{flag}.csv', index=False)
    return df


def get_table_name_by_journal_type(journal_type, journal="individual"):
    """
    Get table name by journal type
    """
    tables = {
        "individual": {
            "primary_life": "I_Accounting_Journal_Life_GMM",
            "primary_general": "I_Accounting_Journal_General_GMM",
            "primary_general_paa": "I_Accounting_Journal_General_PAA",
            "reinsurance_life": "I_Reins_Accounting_Journal_Life_GMM",
            "reinsurance_general": "I_Reins_Accounting_Journal_General_GMM",
            "reinsurance_general_paa": "I_Reins_Accounting_Journal_General_PAA",
        },
        "aggregated": {
            "primary_life": "A_Accounting_Journal_Life_GMM",
            "primary_general": "A_Accounting_Journal_General_GMM",
            "primary_general_paa": "A_Accounting_Journal_General_PAA",
            "reinsurance_life": "A_Reins_Accounting_Journal_Life_GMM",
            "reinsurance_general": "A_Reins_Accounting_Journal_General_GMM",
            "reinsurance_general_paa": "A_Reins_Accounting_Journal_General_PAA",
        },
    }
    result = None
    try:
        result = tables[journal][journal_type]
    except KeyError:
        pass
    print(f"Selected journal: {journal}, type: {journal_type}, table name: {result}")
    return result
