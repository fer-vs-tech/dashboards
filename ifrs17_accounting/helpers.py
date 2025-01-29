import logging

logger = logging.getLogger(__name__)

import codecs
import concurrent.futures
import io

import pandas as pd

import cm_dashboards.ifrs17_accounting.dash_utils as dash_utils
import cm_dashboards.ifrs17_accounting.db_helper as db_helper
import cm_dashboards.wvr_data.wvr_functions as wvr_functions


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


def get_model_name(model="journal"):
    """
    Get model name
    """
    models = {
        "mapping": "IFRS17_Accounting_Mapping",
        "journal": "IFRS17_Accounting_Journal",
    }
    return models[model]


def get_dataframe(handler, connection):
    """
    Get table data from wvr
    """

    table_data_df = handler.get_data(connection)
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


def set_value(df, column_name, apply_formatter=False):
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


def set_value_by_checking(
    IF_df, NB_df, category_id, column_name, apply_formatter=False, select=0
):
    """
    Set value by checking
    """
    result = None
    try:
        if category_id == "IF":
            result = IF_df[column_name].iloc[select]
        elif category_id == "NB":
            result = NB_df[column_name].iloc[select]
        else:
            result = 0
    except IndexError:
        result = 0
    if apply_formatter:
        return formatter(result)
    return result


def set_link(df, encoded_path, url_path, journal_type, name):
    """
    Set link
    """
    # Adjust URL path
    if url_path is None:
        url_path = "?"
    else:
        url_path = url_path + "&"

    # Set link according to name
    if name == "View":
        link = f"[{name}](journal_view/{url_path}journal_type={journal_type}&company_id={df.GoC_Name})"
    elif name == "Download":
        link = (
            f"[{name}](/dash/download/{journal_type}/i/{df.GoC_Name}/?q={encoded_path})"
        )
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


def formatter(x, cast_to_float=False):
    if cast_to_float:
        x = float(x)
    result = x
    try:
        result = round(x, 2)
    except Exception as e:
        logger.error("Formatter failed for {} value with error: {}".format(x, e))

    # Add trailing zeros
    result = "{:.2f}".format(result)
    # logger.info("Result for {}: {}".format(x, result))
    return result


def create_headnote_data(journals_df):
    """
    Create header dataframe from dict
    """
    try:
        header_data = extract_header_data(journals_df)
        header_dict = header_data.transpose().to_dict()
    except IndexError:
        logger.error("No valid header data found")
        header_dict = {}

    details = {
        "Posting_Key": ["H"],
        "Record_Type": [header_dict.get("Record_Type_Text", "SA")],
        "COA": [2020],
        "Special_GL": [header_dict.get("Document_Date", "NONE")],
        "Amount": [header_dict.get("Posting_Date", "NONE")],
        "Base_Amount": ["THB"],
        "Tax_Code": [""],
        "BaseLine_Date": [header_dict.get("Document_Header_Text", "NONE")],
        "Payment_Term": ["0000"],
    }
    df = pd.DataFrame(details)
    df = adjust_cell_data_length(df, flag="HEADER")
    return df


def create_footnote_data(
    result_dict,
    total_transactions,
    total_blocks=None,
):
    """
    Create footer dataframe from dict
    :param summary_dict: dict of credit and debit summary (dict)
    :param total_transactions: total number of transactions (int)
    :param total_blocks: total number of blocks (int) (optional)
    :return df: Created footer dataframe (DataFrame)
    """
    # Round up values
    total_debt = formatter(result_dict.get("40"))
    total_credit = formatter(result_dict.get("50"))

    # Determine default footnote indicator
    indicator = "E"
    block_num = 1

    # Change footnote indicator if num of blocks is provided
    if total_blocks is not None:
        indicator = "F"
        block_num = total_blocks

    # Generate footnote
    details = {
        "Posting_Key": [indicator],
        "Record_Type": [block_num],
        "COA": [total_transactions],
        "Special_GL": [total_debt],
        "Amount": [total_credit],
    }

    # Perform needed operations
    df = pd.DataFrame(details)
    df = adjust_cell_data_length(df, flag="FOOTER")

    return df


def join_dfs(**kwargs):
    """
    Join two dataframes, ignore index and return result
    :param first_df: First dataframe (DataFrame)
    :param second_df: Second dataframe (DataFrame)
    :return result: Joined dataframe (DataFrame)
    """
    result = pd.concat(list(kwargs.values()), ignore_index=True)
    return result


def adjust_record_type(record_type, total_amount, return_record_type=True):
    """
    Helper function to adjust the record type for Deves outputs
    If total amount is negative, then change the record type accordingly
    :param record_type: Record type (str) (e.g. 40 or 50)
    :param total_amount: Total amount (e.g. 10.00)
    :param return_record_type: Flag indicating what to return (bool)
    :return record_type: Adjusted record type (str)
    """
    # Declare constraints
    updated_record_type = record_type
    updated_total_amount = total_amount
    record_types = {
        "50": "40",
        "40": "50",
    }

    # Check if total amount is negative
    if total_amount < 0:
        updated_record_type = record_types.get(record_type, record_type)
        updated_total_amount = abs(total_amount)

    # logger.debug("Type of record {}".format(type(record_type)))
    # logger.debug("Adjusting record type {} to {}".format(record_type, total_amount))

    # Return updated record type if return_record_type is True, otherwise return update_total_amount
    if return_record_type:
        return updated_record_type
    return updated_total_amount


def prepere_df_for_download(
    df,
    journals_df=None,
    include_footer=False,
    calculate_as_block=False,
):
    """
    Prepare dataframe
    """
    header_data = None
    df.drop(columns=["Journal_Variables"], inplace=True)

    # Remove unnecessary rows as per requirement
    df = df[df.Total_Amount != 0.00]

    # Check if df is not empty
    if len(df.index) == 0:
        logger.error("No valid data found")
        return None

    # Round up the amount values up to two decimal places
    df["Total_Amount"] = df.apply(
        lambda x: formatter(x["Total_Amount"], cast_to_float=True),
        axis=1,
    )

    # Remove rows
    df = df[df.Total_Amount != "0.00"]

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
        "Contract_Type": 21,
        "Business_Type": 23,
        "Agent_Broker": 24,
        "FAC": 25,
        "Handle": 26,
        "Fac_Treaty_CO": 27,
    }

    # Remove _R from contract class
    df["CONTRACT_CLASS"] = df["CONTRACT_CLASS"].apply(
        lambda x: x.replace("_R", "") if x.endswith("_R") else x
    )

    # Data cleaning
    df.rename(
        columns={
            "Total_Amount": "Amount",
            "PTFLO": "Reference_Key_2",
            "COHT": "Underwriting_Year",
            "GOC": "Assignment",
        },
        inplace=True,
    )
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
            "Profit_Center_Code",
            "Branch",
            "CONTRACT_GROUP",
            "CONTRACT_CLASS",
            "Underwriting_Year",
        ]
    ]

    # Set new column names
    for column_name, index in column_name_and_index_dict.items():
        # Standard column values as required by the template
        match column_name:
            case "Reference_Key_1" | "Reference_Key_3":
                value = "NA"
            case _:
                value = ""
        df.insert(index, column_name, value)

    # Adjust column value length
    df = adjust_cell_data_length(df)
    total_length = len(df.index)

    # Generate header data if exists
    if journals_df is not None:
        header_data = create_headnote_data(journals_df)

    # Divide df into blocks, calculate total credit and debt amounts per block, write the summary as footnotes
    if calculate_as_block:
        blocks = split_as_block(df, header_data, journals_df)
        return blocks

    # Add header data if exists
    if header_data is not None:
        # Generate header df
        header_data = create_headnote_data(journals_df)
        df = join_dfs(first_df=header_data, second_df=df)

    # Add footer data if needed
    if include_footer and not calculate_as_block:
        # Calculate total debit and credit before rounding up values
        credit_and_debt_sum = calculate_credit_and_debt_sum(df)
        footnote_data = create_footnote_data(credit_and_debt_sum, total_length, 1)
        df = join_dfs(first_df=df, second_df=footnote_data)
    return df


def clear_some_field_values_by_checking(df):
    """
    Clear some field values by checking
    """
    df.loc[
        (df.Record_Type.isin(["40", "50"]))
        & (
            df.COA.str.startswith("1")
            | df.COA.str.startswith("2")
            | df.COA.str.startswith("3")
        ),
        [
            "Reference_Key_3",
            "Branch",
            "CONTRACT_GROUP",
            "CONTRACT_CLASS",
            "Contract_Type",
        ],
    ] = ["".ljust(20), "".ljust(2), "".ljust(3), "".ljust(3), "".ljust(3)]
    return df


def split_as_block(df, header_data, goc):
    """
    Helper function to split df into blocks containing max 900 rows per block
    Calculates total number of blocks, credit and debt sum for each block
    Writes those informations as footer data
    :param df: needed data to operate on the required operations (dataframe)
    :param original_df: needed original df for total credit and debt sum calculations as footer data (dataframe)
    :param header_data: header data to include in the beggining of each block (dataframe)
    :param goc: list of produced GoC (dataframe)
    :return result: final result after completing (dataframe)
    """
    # Declare needed variables
    total_length = len(df.index)
    total_blocks = len(goc.index)

    logger.info("Total length of df: {}".format(total_length))
    logger.info("Total number of blocks: {}".format(total_blocks))

    # Check if loop is needed
    if total_blocks == 0:
        # Add equalizer data if needed
        eqalizer_data, default_total_amount = create_equalizer_data(df)

        # Increment total length if eqalizer data exists
        if eqalizer_data is not None:
            total_length += 1

        # Generate the last footer data
        default_footnote_data = create_footnote_data(default_total_amount, total_length)
        # Add "F" indicator as last row
        final_footnote_data = create_footnote_data(
            default_total_amount, total_length, 1
        )
        # Include header and footer blocks
        if eqalizer_data is not None:
            df = join_dfs(
                header=header_data,
                body=df,
                eqalizer=eqalizer_data,
                footnote=default_footnote_data,
                final_footnote=final_footnote_data,
            )
        else:
            df = join_dfs(
                header=header_data,
                body=df,
                footnote=default_footnote_data,
                final_footnote=final_footnote_data,
            )
        return df

    result = None
    total_valid_blocks = 0

    # Loop through each GOC
    for i, row in goc.iterrows():
        current_goc = row["GoC_Name"]
        # Create a block for current goc
        block = df[df["Assignment"].str.contains(current_goc)]
        # Reset the index
        block.reset_index(inplace=True, drop=True)
        block_size = len(block.index)

        logger.info(f"Block number: {i} / GOC: {current_goc}")
        logger.info("Length of current block: {}".format(block_size))

        # Check if it's valid block
        if block_size == 0:
            logger.info("Block {} is not valid".format(i))
            continue

        # If total block size is less than 900, just perform the needed operations as usual
        if block_size < 900:
            # Add equalizer data if needed
            eqalizer_data, credit_and_debt_sum = create_equalizer_data(
                df=block,
            )

            # Increment total length if eqalizer data exists
            if eqalizer_data is not None:
                total_length += 1
                block_size += 1

            # Generate headnote and footnote data, merge them with current block
            footnote_data = create_footnote_data(credit_and_debt_sum, block_size)
            if eqalizer_data is not None:
                current_block = join_dfs(
                    header=header_data,
                    body=block,
                    eqalizer=eqalizer_data,
                    footnote=footnote_data,
                )
            else:
                current_block = join_dfs(
                    header=header_data, body=block, footnote=footnote_data
                )

            # Update baseline date for the current block, append block number to it
            block_header = str(total_valid_blocks + 1).zfill(3)
            original_baseline_date = current_block["BaseLine_Date"][0].strip()
            current_block["BaseLine_Date"][0] = (
                f"{original_baseline_date}{block_header}".ljust(25)
            )

            # Merge the current block to the result if it exists
            result = (
                current_block
                if result is None
                else pd.concat([result, current_block], ignore_index=True)
            )

            # Increment the total number of valid blocks
            total_valid_blocks += 1
            continue

        # If block size is greater than 899, split it into multiple blocks and add equalizer data if needed
        total_inner_blocks = block_size // 899
        total_inner_blocks += 1 if block_size % 899 != 0 else 0
        logger.info(f"Splitted block {i} into {total_inner_blocks} inner blocks")

        # Get data for each inner block by splitting the current block
        inner_blocks = [block.iloc[i : i + 899] for i in range(0, block_size, 899)]

        # Loop through each inner block and perform the needed operations
        for j, inner_block in enumerate(inner_blocks, start=total_valid_blocks + 1):
            inner_block_size = len(inner_block.index)
            # Add equalizer data if needed
            eqalizer_data, credit_and_debt_sum = create_equalizer_data(
                df=inner_block,
            )

            # Increment total length if eqalizer data exists
            if eqalizer_data is not None:
                total_length += 1
                inner_block_size += 1

            # Generate headnote and footnote data, merge them with current inner block
            footnote_data = create_footnote_data(credit_and_debt_sum, inner_block_size)
            if eqalizer_data is not None:
                current_block = join_dfs(
                    header=header_data,
                    body=inner_block,
                    eqalizer=eqalizer_data,
                    footnote=footnote_data,
                )
            else:
                current_block = join_dfs(
                    header=header_data, body=inner_block, footnote=footnote_data
                )

            # Update baseline date for the current block, append block number to it
            block_header = str(j).zfill(3)
            original_baseline_date = current_block["BaseLine_Date"][0].strip()
            current_block["BaseLine_Date"][0] = (
                f"{original_baseline_date}{block_header}".ljust(25)
            )

            # Merge the current inner block to the result if it exists
            result = (
                current_block
                if result is None
                else pd.concat([result, current_block], ignore_index=True)
            )

        # Increment the total number of valid blocks
        total_valid_blocks += total_inner_blocks

    # logger.info(
    #     "Final result: out of total {} blocks found {} valid blocks".format(
    #         total_blocks, total_valid_blocks
    #     )
    # )

    # Generate the final footnote data
    filtered_rows = result[result["Posting_Key"] == "D"]
    final_total_amount = calculate_credit_and_debt_sum(filtered_rows)
    final_footnote_data = create_footnote_data(
        final_total_amount, total_length, total_valid_blocks
    )

    # Merge the last footer block
    result = join_dfs(main=result, footnote=final_footnote_data)

    # Reset the result df index
    result.reset_index(inplace=True, drop=True)
    return result


def create_equalizer_data(df):
    """
    Helper function to generate the equalizer data if needed
    :param df: the DF to add the equalizer row to
    :return tuple: the equalizer df and the credit and debt sum (to avoid recalculation)
    """
    record_type = None
    difference = None
    equalizer_data = None

    # Calculate the credit and debt sum and extract the needed values
    credit_and_debt_sum = calculate_credit_and_debt_sum(df)
    credit_sum = credit_and_debt_sum.get("50", 0)
    debit_sum = credit_and_debt_sum.get("40", 0)

    # Determine the record type and the difference
    if credit_sum > debit_sum:
        difference = credit_sum - debit_sum
        record_type = "40"
    else:
        difference = debit_sum - credit_sum
        record_type = "50"

    difference = formatter(difference)
    logger.info(
        "Equalizer record type: {}, difference: {}".format(record_type, difference)
    )
    if credit_sum == debit_sum or difference == "0.00":
        logger.info("Difference is 0, no need for equalizer data row")
        return equalizer_data, credit_and_debt_sum

    # Select the first row from the df and populate the equalizer data from it
    first_row = df.iloc[0:1]
    selected_row = first_row.to_dict("records")[0]

    # Replicate needed data
    assignment = selected_row.get("Assignment")
    reference_key_2 = selected_row.get("Reference_Key_2")
    profit_center = "2000-00000"
    branch = "00"
    contract_group = selected_row.get("CONTRACT_GROUP")
    contract_class = selected_row.get("CONTRACT_CLASS")
    underwriting_year = selected_row.get("Underwriting_Year")

    # Create equalizer data
    equalizer_row = {
        "Posting_Key": "D",
        "Record_Type": record_type,
        "COA": 999999,
        "Special_GL": "",
        "Amount": difference,
        "Base_Amount": "",
        "Tax_Code": "",
        "BaseLine_Date": "",
        "Payment_Term": "",
        "Payment_Method": "",
        "Assignment": assignment,
        "Account_Description": "Equalizer row",
        "Reference_Key_1": "NA",
        "Reference_Key_2": reference_key_2,
        "Reference_Key_3": "NA",
        "Cost_Center": "",
        "Internal_Order": "",
        "Profit_Center_Code": profit_center,
        "Branch": branch,
        "CONTRACT_GROUP": contract_group,
        "CONTRACT_CLASS": contract_class,
        "Contract_Type": "",
        "Underwriting_Year": underwriting_year,
        "Business_Type": "",
        "Agent_Broker": "",
        "FAC": "",
        "Handle": "",
        "Fac_Treaty_CO": "",
    }

    # Create df from the equalizer data
    equalizer_data = pd.DataFrame(equalizer_row, index=[0])
    equalizer_data = adjust_cell_data_length(equalizer_data, flag="EQUALIZER")

    # Update corresponding credit/debt sum value
    credit_and_debt_sum[record_type] += float(difference)
    return equalizer_data, credit_and_debt_sum


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
        "Profit_Center_Code",
        "Branch",
        "CONTRACT_GROUP",
        "CONTRACT_CLASS",
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

    match flag:
        case "BODY" | "EQUALIZER":
            cell_length = default_length
        case "HEADER":
            cell_length = [1, 2, 4, 8, 8, 4, 16, 25, 4]
        case "FOOTER":
            cell_length = [1, 10, 10, 20, 20]
        case _:
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

    # df.to_csv(f"{flag}.csv", index=False)
    return df


def get_record_type(n_clicks):
    """
    Get record type
    """
    record_type = "default"
    if n_clicks and n_clicks % 2 == 1:
        record_type = "reversed"
    return record_type


def extract_header_data(df):
    """
    Helper function to extract header data from the journal DF
    :param df: the journal DF object
    :return list of header data: header data (list)
    """
    # Select wanted columns and extract them from first row as it is repeated
    try:
        result = df[
            [
                "Document_Date",
                "Posting_Date",
                "Document_Header_Text",
                "Record_Type_Text",
            ]
        ].iloc[0]
        return result
    except IndexError:
        logger.error("No valid header data found")
        raise IndexError("No valid header data found")


def convert_to_float(value):
    """
    Helper function to convert str representation to float to float
    :param value: str representation of float value
    :return result: converted float data
    """
    result = float(value)
    # logger.info("Result for {}: {}".format(value, result))
    return result


def calculate_credit_and_debt_sum(df, cast_to_float=True):
    """
    Helper function to calculate credit and debit sum for a given document
    :param df: DataFrame object containing values for calculating
    :param convert_to_float: Whether to convert to float or not
    :return total_sum: Credit (50) and debit (0) sum (dict)
    """
    # Deep copy to avoid changing the original df
    df_copy = df.copy()

    # Conver to float if flag is set
    if cast_to_float:
        df_copy["Total_Amount"] = df_copy["Amount"].apply(lambda x: convert_to_float(x))

    # Group by record type (40, 50) as credit and debit sum
    result = df_copy.groupby("Record_Type")["Total_Amount"].sum()
    result = result.to_frame().to_dict()
    result = result.get("Total_Amount")
    del df_copy

    # Make sure that both keys exist as sometimes one of them is missing
    result["40"] = result.get("40", 0)
    result["50"] = result.get("50", 0)

    return result


def generate_export_file(df, index=False, header=False, float_format="%.2f", sep="\t"):
    """
    Helper function to generate the export file for a given DF using in-memory buffers
    :param df: the DF to generate the export (DataFrame)
    :return: generated export file (BytesIO)
    """
    # Create temporary file in memory
    memory_object = io.StringIO()
    df.to_csv(
        memory_object, index=index, header=header, float_format=float_format, sep=sep
    )

    # Store data in a temporary file (in-memory buffer)
    export_file = io.BytesIO()
    export_file.write(codecs.BOM_UTF8 + memory_object.getvalue().encode("utf-8"))
    export_file.seek(0)
    memory_object.close()

    return export_file


def get_connection_string(wvr_path, model):
    """
    Get connection string for a given model and wvr path
    """
    model = get_model_name(model)
    connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
    logger.info("Connect string: {}".format(connect_string))
    connection = wvr_functions.get_connection(connect_string)
    return connection


def populate_journal_data(
    df,
    company_id,
    in_journal_df=None,
    nb_journal_df=None,
    reverse=False,
    filter_zeros=False,
    mapping_key=None,
):
    """
    Populate journal data based on the parameters
    :param df: the DF to populate the journal data for (DataFrame)
    :param company_id: the company ID to use for filtering (str)
    :param in_journal_df: the in journal DF to use for filtering (DataFrame)
    :param nb_journal_df: the nb journal DF to use for filtering (DataFrame)
    :param reversed: whether to reverse the record type or not (bool)
    :param mapping_key: journal mapper name
    :return df: the DF after populating the journal data (DataFrame)
    """
    # Check if passed DF are valid
    if df.empty:
        logger.error("Passed DF are empty, returning original DF")
        return df

    # Define new column names and default values
    transition_journal = mapping_key == "transition"
    new_columns = {
        "Posting_Key": "D",
        "Total_Amount": 0,
        "GOC": "",
        "PTFLO": "",
        "CONTRACT_GROUP": "",
        "CONTRACT_CLASS": "",
        "COHT": 0,
        "Branch": "00" if transition_journal else "",
        "Profit_Center_Code": "2000-00000" if transition_journal else "",
    }
    df = df.assign(**new_columns)

    # Define columns to be used for data retrieval from journals df
    journal_columns = [
        "GOC",
        "PTFLO",
        "CONTRACT_GROUP",
        "CONTRACT_CLASS",
        "COHT",
    ]
    if not transition_journal:
        journal_columns.append("Profit_Center_Code")

    original_size = len(df.index)
    skipped_data = 0
    record_type_switcher = {
        "40": "50",
        "50": "40",
    }
    journal_mapping = {
        "IF": in_journal_df,
        "NB": nb_journal_df,
    }
    for index, row in df.iterrows():
        aggregates = row["Aggregates"]
        nb_if = row["NB_IF"]
        journal_variable = row["Journal_Variables"]
        journal_data = journal_mapping.get(nb_if, pd.DataFrame())
        if journal_data is None or journal_data.empty:
            skipped_data += 1
            continue

        # Select only the needed columns from the journal df
        journal_data = journal_data[[*journal_columns, journal_variable]]

        # If filter_zeros is set to True, prevent writing zero-valued data to the report file
        # On dashboard, this is not needed as whole data should be shown
        if filter_zeros:
            total_sum = formatter(journal_data[journal_variable].sum())
            if total_sum == "0.00":
                # logger.warning(f"Current {index}: {nb_if} is empty, skipping")
                skipped_data += 1
                # Remove current row as it won't be needed
                # df.drop(index, inplace=True)
                continue

        # If "aggregates" is set to yes, then sum the values and assign other values from the first row
        # of the journal data as they are the same for all rows
        if aggregates == "Yes":
            # Get absolute value if total amount is negative, and switch record type
            total_amount = journal_data[journal_variable].sum()
            record_type = row["Record_Type"]
            if total_amount < 0:
                total_amount = abs(total_amount)
                record_type = record_type_switcher.get(record_type, record_type)

            # Switch record type if reversed flag is set
            if reverse:
                record_type = record_type_switcher.get(record_type, record_type)

            # Set final values
            journal_data = journal_data.copy()
            journal_data.loc[:, "Profit_Center_Code"] = "2000-00000"
            df.loc[index, "Total_Amount"] = total_amount
            df.loc[index, "Record_Type"] = record_type
            df.loc[index, journal_columns] = (
                journal_data[journal_columns].iloc[0].values.tolist()
            )
            if not transition_journal:
                df.loc[index, "Branch"] = parse_branch_code(
                    journal_data["Profit_Center_Code"].astype(str).iloc[0]
                )
            continue

        # If "aggregates" is set to no and selected company is ALL, just set profit center and total amount values
        if company_id == "ALL" and aggregates == "No":
            # logger.info("Company ID is ALL, prepare data for only dashboard")
            total_amount = journal_data[journal_variable].sum()
            record_type = row["Record_Type"]

            # Get absolute value if total amount is negative, and switch record type
            if total_amount < 0:
                total_amount = abs(total_amount)
                record_type = record_type_switcher.get(record_type, record_type)

            # Switch record type if reversed flag is set
            if reverse:
                record_type = record_type_switcher.get(record_type, record_type)

            # Set final values
            df.loc[index, "Total_Amount"] = total_amount
            df.loc[index, "Record_Type"] = record_type
            df.loc[index, journal_columns] = (
                journal_data[journal_columns].iloc[0].values.tolist()
            )
            # Set profit center code if required
            if not transition_journal:
                df.loc[index, "Profit_Center_Code"] = (
                    journal_data["Profit_Center_Code"].astype(str).iloc[0]
                )
                df.loc[index, "Branch"] = parse_branch_code(
                    journal_data["Profit_Center_Code"].astype(str).iloc[0]
                )
            continue

        # logger.info(
        #     f"Current {index}, {journal_variable} is not aggregated = {nb_if}, total data {len(journal_data)}"
        # )

        # If "aggregates" is set to no, prepare journal data and concatenate it with the current row
        if filter_zeros:
            journal_data = journal_data[
                ~journal_data[journal_variable].isin([0, 0.0, 0.00, -0.00])
            ]

        # Add mapping columns to journal df
        journal_data = journal_data.assign(
            **{
                "Posting_Key": "D",
                "Record_Type": row["Record_Type"],
                "COA": row["COA"],
                "Account_Description": row["Account_Description"],
                "Aggregates": row["Aggregates"],
                "Journal_Variables": row["Journal_Variables"],
                "NB_IF": row["NB_IF"],
            }
        )
        journal_data.rename(
            columns={journal_variable: "Total_Amount"},
            inplace=True,
        )

        # Add branch code column to journal data if required
        if not transition_journal:
            journal_data["Branch"] = journal_data["Profit_Center_Code"].apply(
                lambda x: parse_branch_code(x)
            )

        # Cast total amount to positive value and switch record type if total amount is negative
        journal_data[["Total_Amount", "Record_Type"]] = journal_data.apply(
            lambda x: (
                (
                    abs(x["Total_Amount"]),
                    record_type_switcher.get(x["Record_Type"], x["Record_Type"]),
                )
                if x["Total_Amount"] < 0
                else (x["Total_Amount"], x["Record_Type"])
            ),
            axis=1,
        ).values.tolist()

        # Switch record type if reversed flag is set
        if reverse:
            journal_data["Record_Type"] = journal_data["Record_Type"].apply(
                lambda x: record_type_switcher.get(x, x)
            )

        # Remove current row
        # df.drop(index, inplace=True)

        # Concatenate current journal data with the original DF
        df = pd.concat([df, journal_data], ignore_index=True)

    after_population = df.shape[0]
    logger.info(
        f"GOC: {company_id}, original: {original_size}, populated: {after_population - original_size}, skipped: {skipped_data}, total size: {after_population}"
    )

    return df


def parse_branch_code(profit_center_code):
    """
    Helper function to extract branch code from given profit center code
    :param profit_center_code: the profit center code to parse (2000-00000) (str)
    :return branch_code: the branch code (00) (str)
    """
    branch_code = "00"
    try:
        branch_code = profit_center_code.split("-")[0][-2:]
    except Exception:
        logger.error("No valid branch code found, using default '00' value")
    return branch_code


def get_results_from_db(journal_type, journal_cn_string, mapping_cn_string):
    """
    Get results from database for all mappings and journals
    :param journal_type: type of journal (str) (primary or reinsurance)
    :param journal_cn_string: the journal connection string (str)
    :param mapping_cn_string: the mapping connection string (str)
    """
    mappers = ["actual", "expected_if", "expected_nb", "lic", "transition"]
    journals = ["if", "nb", "transition"]
    results = dict(mapping={}, journal={})
    for mapper in mappers:
        db = db_helper.GetMappingData(journal_type=journal_type, journal_name=mapper)
        df = get_dataframe(db, mapping_cn_string)
        results["mapping"][mapper] = df
        logger.info(f"Results for {mapper} mapper: {df.shape[0]}")

    for journal in journals:
        db = db_helper.GetJournalData(journal_type=journal_type, journal_name=journal)
        df = get_dataframe(db, journal_cn_string)
        results["journal"][journal] = df
        logger.info(f"Results for {journal} journal: {df.shape[0]}")

    return results


def filter_by_goc(df, goc_names):
    """
    Helper function to filter DF by GOC name
    """
    return df[df["GOC"] == goc_names]


def generate_report_date(journals_df, db_results, reverse=False):
    """
    Generate report date for each journal based on DB results
    :param journals_df: the journals DF that contains GOC names (DataFrame)
    :param db_results: DB results (dict of DFs)
    """

    mappings = db_results["mapping"]
    journals = db_results["journal"]
    results = list()

    # Cache filtered DataFrames
    filtered_journals = dict()
    for key in journals.keys():
        filtered_journals[key] = dict()
        for goc in journals_df["GoC_Name"].unique():
            filtered_journals[key][goc] = filter_by_goc(journals[key], goc)

    # Define worker function for concurrent.futures
    def worker(index, row):
        logger.info(f"Processing row {index} of {len(journals_df.index)}")
        current_goc = row["GoC_Name"]
        row_results = list()
        for mapping_key in mappings.keys():
            mapping_df = mappings[mapping_key]

            # Get corresponding journal DF based on mapping key
            match mapping_key:
                case "actual" | "lic":
                    journal_if_df = filtered_journals["if"][current_goc]
                    journal_nb_df = filtered_journals["nb"][current_goc]

                case "expected_if":
                    journal_if_df = filtered_journals["if"][current_goc]

                case "expected_nb":
                    journal_nb_df = filtered_journals["nb"][current_goc]

                case "transition":
                    journal_if_df = filtered_journals["transition"][current_goc]

            # Populate journal data for current GOC and mapping key
            auto_select = journal_if_df is not None and journal_nb_df is not None
            result = populate_journal_data(
                df=mapping_df,
                company_id=current_goc,
                in_journal_df=journal_if_df,
                nb_journal_df=journal_nb_df,
                filter_zeros=True,
                reverse=reverse,
                mapping_key=mapping_key,
            )
            if not result.empty:
                row_results.append(result)

        return pd.concat(row_results, ignore_index=True)

    # Process single GOC data in parallel using concurrent futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(worker, index, row) for index, row in journals_df.iterrows()
        ]
        # Wait for all threads to finish and gather results
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    return pd.concat(results, ignore_index=True)


def reverse_journal_dates(df):
    """
    Update document date and posting date for reversed journals
    For example: 31012022 -> 28022022 (last day of the next month)
    :param df: the DF to update the dates for (DataFrame)
    :return df: the DF after updating the dates (DataFrame)
    """
    try:
        df["Posting_Date"] = df["Posting_Date"].apply(
            lambda x: (
                pd.to_datetime(x, format="%d%m%Y") + pd.offsets.MonthEnd(1)
            ).strftime("%d%m%Y")
        )
        logger.info("Dates updated successfully")
    except Exception as e:
        logger.error("Error while updating dates: {}".format(e))

    return df


def generate_filename(doc_type, report_type, report_date, reverse=False):
    """
    Create filename for the generated report
    :param doc_type: the document type (str) (YQ, YR)
    :param report_type: the report type (str) (primary, reinsurance)
    :param reverse: whether the report is reversed or not (bool)
    """
    doc_type = doc_type.upper()
    report_type = report_type.title()
    report_type = report_type.replace("Reinsurance", "Reins")
    report_date = pd.to_datetime(report_date, format="%d%m%Y")
    report_date = report_date.strftime("%Y%m%d")
    reverse = "D" if not reverse else "R"
    filename = f"2020{doc_type}{report_date}-{report_type}-{reverse}.txt"
    return filename
