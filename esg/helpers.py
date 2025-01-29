"""
Author: Kamoliddin Usmonov
Date: 2022-12-29
Description: Helper functions for ESG dashboards
"""

import logging

logger = logging.getLogger(__name__)

import datetime
import statistics
import time

import numpy as np

import cm_dashboards.dash_utils as dash_utils


def get_df(handler, wvr_path, model_name, replace_na=None):
    """
    Get table data from wvr
    :param handler: DB handler
    :param wvr_path: path to wvr file
    :return: DataFrame
    """
    df = handler.get_wvr_data(wvr_path, model_name)
    # Replace NaN values if provided
    if replace_na is not None:
        df = df.replace(np.nan, 0)
    return df


def prepare_dropdown_options(option_names, name="Model", default=None):
    """
    Generate dropdown options
    :param option_names: List of option names
    :return: list of dictionaries (value, label, title) for dropdown options
    """
    # logger.info("Generating dropdown options: {}".format(option_names))
    if default is not None:
        option_names.insert(0, default)

    # Loop through list of option names and create a list of dropdown options
    options = []
    for option_name in option_names:
        # Flat list if it exists
        if isinstance(option_name, list):
            option_name = option_name[0]

        # Format date if flag is set
        if name == "Report date" and not isinstance(option_name, str):
            title = option_name.strftime("Report date %d-%b-%Y")
        else:
            title = "{} '{}'".format(name, option_name)

        # Generate new option
        option = {
            "label": option_name,
            "value": option_name,
            "title": title,
        }
        options.append(option)

    # logger.info("Dropdown options for {}: {}".format(name, options))
    return options


def prepare_table_data(
    df,
    header_rows=[],
    hidden_columns=[],
    filter_column_style=None,
    additional_header=[],
    replace_zero=None,
    multi_index=False,
    show_negative_numbers=True,
):
    """
    Prepare table data
    :param df: DataFrame
    :param header_rows: list of header rows
    :param hidden_columns: list of hidden columns
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Check if replacement is needed
    if replace_zero is not None:
        df = df.replace({0: replace_zero})

    # Set multiindex table data, column if needed
    if multi_index:
        table_data, columns = dash_utils.set_multi_index_column_names(
            df, show_negative_numbers=show_negative_numbers
        )
    else:
        table_data = df.to_dict("records")
        table_columns = df.columns
        columns = dash_utils.set_column_names(
            table_columns,
            precision=0,
            hidden_columns=hidden_columns,
            show_negative_numbers=show_negative_numbers,
            additional_header=additional_header,
        )
    conditional_style = dash_utils.set_table_style_kics(
        columns, show_negative_numbers=show_negative_numbers
    )
    row_style = dash_utils.set_row_style(header_rows)
    style = conditional_style + row_style

    # Add conditional style for filter column
    if filter_column_style is not None:
        result = dash_utils.set_conditional_style_by_filtering(
            column=filter_column_style
        )
        style = style + result

    return table_data, columns, style


def get_color_plate(graph_name):
    """
    Get the color plate for the graph
    """
    colors = [
        "#7990FF",
        "#39C0BE",
        "#3C62F1",
        "#F8981D",
        "#FA7F7F",
        "#EC008C",
        "#9B51E0",
        "#EB5757",
        "#F7E11E",
        "#1693A5",
    ]
    colors_two = ["#1B238C", "#2741BC", "#4364F7", "#7992FF", "A0B1F1"]
    color_plate = {
        "line": colors,
        "bar": colors_two,
        "pie": colors,
    }

    return color_plate.get(graph_name)


def get_date_dropdown_options(report_date=None, select_after=False):
    """
    Helper function to create a dropdown for date selection
    :param report_date: report date to select (optional)
    :return default: dict of lists that contain date as key and model name as value
    """
    default = {
        datetime.date(2019, 12, 31): "IFRS_17_t000",
        datetime.date(2020, 12, 31): "IFRS_17_t001",
        datetime.date(2021, 12, 31): "IFRS_17_t002",
        datetime.date(2022, 12, 31): "IFRS_17_t003",
        datetime.date(2023, 12, 31): "IFRS_17_t004",
        datetime.date(2024, 12, 31): "IFRS_17_t005",
        datetime.date(2025, 12, 31): "IFRS_17_t006",
        datetime.date(2026, 12, 31): "IFRS_17_t007",
        datetime.date(2027, 12, 31): "IFRS_17_t008",
        datetime.date(2028, 12, 31): "IFRS_17_t009",
        datetime.date(2029, 12, 31): "IFRS_17_t010",
        datetime.date(2030, 12, 31): "IFRS_17_t011",
        datetime.date(2031, 12, 31): "IFRS_17_t012",
        datetime.date(2032, 12, 31): "IFRS_17_t013",
        datetime.date(2033, 12, 31): "IFRS_17_t014",
        datetime.date(2034, 12, 31): "IFRS_17_t015",
        datetime.date(2035, 12, 31): "IFRS_17_t016",
        datetime.date(2036, 12, 31): "IFRS_17_t017",
        datetime.date(2037, 12, 31): "IFRS_17_t018",
        datetime.date(2038, 12, 31): "IFRS_17_t019",
        datetime.date(2039, 12, 31): "IFRS_17_t020",
        datetime.date(2040, 12, 31): "IFRS_17_t021",
        datetime.date(2041, 12, 31): "IFRS_17_t022",
        datetime.date(2042, 12, 31): "IFRS_17_t023",
        datetime.date(2043, 12, 31): "IFRS_17_t024",
        datetime.date(2044, 12, 31): "IFRS_17_t025",
        datetime.date(2054, 12, 31): "IFRS_17_t035",
        datetime.date(2059, 12, 31): "IFRS_17_t040",
        datetime.date(2064, 12, 31): "IFRS_17_t045",
        datetime.date(2069, 12, 31): "IFRS_17_t050",
        datetime.date(2079, 12, 31): "IFRS_17_t060",
        datetime.date(2089, 12, 31): "IFRS_17_t070",
        datetime.date(2099, 12, 31): "IFRS_17_t080",
        datetime.date(2109, 12, 31): "IFRS_17_t090",
        datetime.date(2119, 12, 31): "IFRS_17_t100",
    }

    if report_date is None:
        return default

    # Selec specified date, get its model name
    date = datetime.datetime.strptime(report_date, "%Y-%m-%d").date()

    # Filter options if select after is specified
    if select_after:
        after_options = dict()
        # Check if it exists in default settings
        if default.get(date) is None:
            logger.error("Graph max date not found in default settings")
            return after_options

        # Filter out date options that comes before selected period
        after_options = dict(
            filter(
                lambda current_date: filter_date(current_date, date), default.items()
            )
        )
        return after_options

    # Selec specified date, get its model name
    date = datetime.datetime.strptime(report_date, "%Y-%m-%d").date()
    result = default.get(date)
    logger.info("Selected date: {} - {}".format(report_date, result))
    return result


def filter_date(current_date, target_date):
    """
    Filter out dates that represent past dates than tagret date
    :param current_date: date and name of the current date (tuple)
    :return result: boolean indicating if the date should be filtered
    """
    result = current_date[0] > target_date
    return result


def pivot_df(df):
    """
    Helper function to rotate the df
    :param df: the df to rotate
    :param result: rotated result
    """
    # Rotate DF
    df = df.reset_index(drop=True).transpose()

    # Make the first row as header row
    df.columns = df.iloc[0]
    df = df[1:]

    # Convert datetime object to string in column names
    df.rename(
        columns=lambda t: t.strftime("%Y-%m-%d") if isinstance(t, datetime.date) else t,
        inplace=True,
    )

    # Reset index, rename 'index' column name
    df.reset_index(inplace=True)
    df.rename(columns={"index": ""}, inplace=True)

    return df


def calculate_percentile(df, variable, report_dates):
    """
    Helper function to calculate needed percentile stats for a given dataset
    :param df: DF to operate on
    :param variable: Variable (or column) name to calculate percentage on its value
    :param report_dates: List of report dates
    :return result: DF result that holds result of calculations
    """
    logger.info("Variable name: {}".format(variable))
    start_time = time.perf_counter()

    # Define constants
    percentile_values = [0, 1, 2.5, 5, 10, 25, 75, 90, 95, 97.5, 99, 100]
    percentile_columns = [f"{percentile}%" for percentile in percentile_values]

    # Needed new columns
    columns_names = [
        "1%-0%",
        "2.5%-1%",
        "5%-2.5%",
        "10%-5%",
        "25%-10%",
        "75%-25%",
        "90%-75%",
        "95%-90%",
        "97.5%-95%",
        "99%-97.5%",
        "100%-99%",
        "Median",
        "Average",
    ]
    columns_values = [""] * len(columns_names)
    new_columns = dict(zip(columns_names, columns_values))

    # Add needed columns
    logger.info("Adding columns: {}".format(columns_names))
    df = df.assign(**new_columns)

    # Loop through each row, calculate and add percentiles
    keep_track_results = dict(zip(percentile_columns, percentile_values))
    for report_date in report_dates:
        current_date = report_date[0]
        logger.info("Calculating data: {}".format(current_date))

        # Select all rows that match the report date, extract values as list
        current_values = df.query("Report_date == @current_date")
        current_list = current_values[variable].values.tolist()

        # Add median and average values
        indexes = list(current_values.index)
        first_row = indexes[0]
        new_columns["Median"] = statistics.median(current_list)
        new_columns["Average"] = statistics.mean(current_list)

        # Calculate and add percentiles
        # logger.info("Presented values {}".format(current_list))
        last_percentile_index = None
        for i, percentile in enumerate(percentile_values):
            # Skip the first percentile as it is not part of update results
            if i != 0:
                last_percentile_index = i - 1

            percentile_column = "{}%".format(percentile)
            result = calc_percentile(current_list, percentile)

            # Update tracking dict
            current_percentile = keep_track_results.get(percentile_column)
            if current_percentile is not None:
                keep_track_results[percentile_column] = result

            # logger.info(
            #     "{} Current percentile {}: {}".format(i, percentile_column, result)
            # )

            # Skip the first percentile result (0%)
            # Subtract the previous percentile result from the current percentile result
            # Sample: 1% - 0%, 2-5% - 1%, 5% - 2.5%
            # Add original cell value after subtracting
            if last_percentile_index is not None:
                column_name = columns_names[i - 1]
                last_percentile = percentile_columns[last_percentile_index]
                calc_result = keep_track_results[last_percentile]

                # Perform needed calculation then insert the result into final result dictionary
                # Subtract previous results from the current percentailed one, add original cell value
                final_result = result - calc_result  # + current_list[0]
                new_columns[column_name] = final_result
                # logger.info("Last percentile result: {}".format(calc_result))

        # Update current row values
        # logger.info("Final result: {}".format(new_columns))
        df.loc[first_row, new_columns.keys()] = new_columns.values()

    # Drop unnecessary rows that do not hold percentile values
    df = df[df["1%-0%"] != ""]
    # df = df.drop(columns=[variable])
    end_time = time.perf_counter()
    logger.info("Time took for calculation: {} seconds".format(end_time - start_time))

    return df


def calc_percentile(data, percentile_value):
    """
    Calculates the value at a given percentile in a dataset.
    param data (list or tuple): The dataset for which to calculate the percentile.
    param percentile_value (float): The percentile value, expressed as a decimal between 0 and 1.
    return result (float): The value at the given percentile in the dataset.
    """
    # Use numpy built-in function for computing percentile
    result = np.percentile(data, percentile_value)
    # logger.info("Percentile value for {} is {}".format(percentile_value, result))

    return result


def apply_threshold(df, threshold):
    """
    Helper function for computing median values,
    and applying a threshold to the values to filter out unmatched rows
    :param df: the data set to filter (dateframe)
    :param treshold: the threshold value to apply (int)
    :return df: updated data set
    """
    logger.info(f"Threshold value: {threshold}")
    if threshold is None:
        return df

    # Reset index
    df = df.reset_index(drop=True)
    df["Valid"] = ""

    # Calculate MAX median value across all rows, excluding the first row
    max_median = df[1:].Median.max()
    logger.info(f"Maxmedian value: {max_median}")

    # Check if there are valid values before calculating
    if max_median <= 0:
        return df[df.Valid != ""]

    # Loop through over all rows and calculate ratios between the max median
    # and the median value across all rows starting from the the current one
    for index, _ in df[1:].iterrows():
        # Calculate ratio
        median_sum = df[index:].Median.abs().sum()
        ratio = median_sum / max_median * 100
        # Check if ratio is greater the threshold
        is_valid = ratio > threshold
        # Save the validity status
        df.loc[index, "Valid"] = is_valid

        # logger.info(
        #     f"{index} Median sum {median_sum}, Current ratio for {row.Report_date}: {ratio}"
        # )

    # Filter out rows that are not satisfied by the specified threshold
    df.loc[0, "Valid"] = True
    df = df[df.Valid == True]

    return df


def calculate_and_add_needed_values(df):
    """
    Helper function to add needed columns  as per requirement
    Function will use several operators to add required columns and their values
    :param df: Data frame to add rows to
    :return df: complete Data frame
    """
    # Define new columns and values for its required calculations
    # "current_" indicates the value needs to be grabbed current row
    # "previous_" indicates the value needs to be grabbed from previous row
    operation_units = {
        "Release_of_BEL": {
            "previous_x": "PV_Net_CF_RN",
            "previous_y": "PV_Net_CF_RN_Next",
        },
        "Release_of_RA": {
            "previous_x": "PV_RA_Total_RN",
            "previous_y": "PV_RA_Total_RN_NExt",
        },
        "Release_of_RC": {
            "previous_x": "RC_Calc_RN",
            "previous_y": "RC_Calc_RN_Next",
        },
        "Current_CF": {
            "current_x": "Net_CF",
            "current_y": "Int_On_CF",
            "operation": "+",
        },
        "Change_in_BEL": {
            "previous_x": "PV_Net_CF_RN_Next",
            "current_y": "PV_Net_CF_RN",
        },
        "Change_in_RA": {
            "previous_x": "PV_RA_Total_RN_NExt",
            "current_y": "PV_RA_Total_RN",
        },
        "Change_in_RC": {
            "previous_x": "RC_Calc_RN_Next",
            "current_y": "RC_Calc_RN",
        },
        "temp": {
            "current_x": "Net_CF_RN_Next",
            "current_y": "Int_On_CF_RN_Next",
            "operation": "+",
        },
        "Change_in_current_CF": {
            "current_x": "Current_CF",
            "current_y": "temp",
            "self": True,
        },
    }

    # Assign new columns before updating
    new_columns = [column for column in operation_units.keys() if column != "temp"]
    new_columns_values = [0] * len(new_columns)
    df = df.assign(**dict(zip(new_columns, new_columns_values)))

    # Iterate over each row, skip the first one
    for index, row in df[1:].iterrows():
        # Get needed informations
        previus_row = df.loc[index - 1].to_dict()
        current_row = row.to_dict()
        results = dict()
        logger.info("Index: {}".format(index))
        # logger.info("Current row: {}".format(current_row))
        # logger.info("Previus row: {}".format(previus_row))

        for column, formula in operation_units.items():
            operation = formula.get("operation", "-")
            x = None
            y = None

            # Set x value
            if formula.get("current_x") and formula.get("self"):
                x = results.get(formula.get("current_x"))
            elif formula.get("current_x"):
                x = current_row.get(formula.get("current_x"), 0)
            else:
                x = previus_row.get(formula.get("previous_x"), 0)

            # Set y value
            if formula.get("current_y") and formula.get("self"):
                y = results.get(formula.get("current_y"))
            elif formula.get("current_y"):
                y = current_row.get(formula.get("current_y"), 0)
            else:
                y = previus_row.get(formula.get("previous_y"), 0)
            # logger.info("Column {}: {} {} {}".format(column, x, operation, y))

            # Calculate and update results dictionary
            result = calculate(x, y, operation)
            results[column] = result

        # Delete temp key, add new one as summary result
        results.pop("temp", None)
        results["RW_Profit"] = sum(results.values())

        # Append results to the current row
        df.loc[index, results.keys()] = results.values()

    return df


def calculate(value1, value2, operator):
    """
    Calculate values
    :param value1: First value
    :param value2: Second
    :param operator: Operator (str) (+, -, *, /, //)
    :return: Calculated value
    """
    # logger.info("Calculate: {} {} {}".format(value1, operator, value2))
    match operator:
        case "+":
            result = value1 + value2
        case "-":
            result = value1 - value2
        case "*":
            result = value1 * value2
        case "/":
            result = value1 / value2
        case "//":
            result = value1 // value2
        case _:
            result = value1 + value2

    return result
