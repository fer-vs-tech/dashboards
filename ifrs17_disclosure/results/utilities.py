"""
@author: Kamoliddin Usmonov
@date: 2022-09-14
@description: This file contains functions to calculate IFRS17 disclosure
"""
import logging

logger = logging.getLogger(__name__)

import pandas as pd

from cm_dashboards.ifrs17_disclosure.results.formulas import (
    COLUMN_NAMES,
    DESCRIPTIONS,
    FORMULAS,
)


def create_df(columns):
    """
    Create new DF
    """
    df = pd.DataFrame(columns=columns)
    return df


def add_row(df, row):
    """
    Add row to DF
    """
    df.loc[len(df)] = row
    return df


def update_row(df, index, result):
    """
    Update row in DF
    """
    df.iloc[index] = result
    return df


def add_rows(df, new_df, journal_name, journal_type):
    """
    Add rows to DF
    """
    try:
        descriptions = DESCRIPTIONS[journal_name][journal_type]
        formulas = FORMULAS[journal_name][journal_type]
    except KeyError:
        raise Exception("Invalid journal name or journal type")

    # Add ordinary rows
    headers = {}
    for description in descriptions:
        results = do_calculation(df, new_df, description, formulas, headers)
        new_df = add_row(new_df, results)

    # Add header rows
    for key, val in headers.items():
        results = do_calculation(df, new_df, key, formulas)
        new_df = update_row(new_df, val["index"], results)

    return new_df


def get_result(df, journal_name, journal_type):
    """
    Generate result after calculation
    """

    try:
        columns = COLUMN_NAMES[journal_name][journal_type]
    except Exception as err:
        logger.error("Error occured while getting results: {}".format(err))
        raise Exception("Invalid journal name or journal type")

    new_df = create_df(columns)
    new_df = add_rows(df, new_df, journal_name, journal_type)
    return new_df


def get_header_rows_id(journal_name, journal_type):
    """
    Get header rows
    """
    try:
        formulas = FORMULAS[journal_name][journal_type]
    except KeyError as err:
        logger.error("Could not find journal: {}".format(err))
        raise Exception("Invalid journal name or journal type")

    rows_id = []
    for val in formulas.values():
        if val is not None and "index" in val:
            rows_id.append(val["index"])
    return rows_id


def do_calculation(df, result_df, key, formulas, headers=None):
    """
    This function is used to calculate the values for the IFRS17 disclosure
    """
    # Remove the brackets from the key that is used to prevent double key error
    description = key.replace("(2)", " ").strip()
    if key not in formulas:
        logger.error("Formula not found for {}".format(key))
        return [description, "", "", "", ""]

    # Get the formula for the key
    formula = formulas[key]
    # logger.info("Formula for {}".format(key))

    # Check if calculation is required
    if formula is None or "LRC" not in formula:
        return [description, "", "", "", 0]

    # Check if auto-fill is required
    if "auto-fill" in formula:
        # logger.info("Auto-fill: {}".format(formula["auto-fill"]))
        return [
            description,
            formula["auto-fill"],
            formula["auto-fill"],
            formula["auto-fill"],
            formula["auto-fill"],
        ]

    # Check if it's a header row
    if headers is not None and formula.get("header", False):
        # Add the header to the list
        header = {
            key: formula,
        }
        headers.update(header)
        # logger.info("Header row detected: {}".format(key))
        return [description, "", "", "", 0]

    # Calculate the values with the defined formula
    result = []
    total_sum = 0
    # Copy the result_df to a new df to avoid changing the original df
    result_df = result_df.copy()
    for k, v in formula.items():
        # logger.info("Key: {}, val: {}".format(k, v))
        if k == "LRC":
            # Check if the formula is valid
            if v is None:
                result.append("")
                continue

            # Check if there is auto-fill value
            if "auto-fill" in v:
                result.append(v["auto-fill"])
                continue

            # Calculate the LRC
            current_sum = eval_formula(df, result_df, v)
            total_sum += current_sum
            result.append(current_sum)

        if k == "LC":
            # Check if the formula is valid
            if v is None:
                result.append("")
                continue

            # Check if there is auto-fill value
            if "auto-fill" in v:
                result.append(v["auto-fill"])
                continue

            # Calculate the LC
            current_sum = eval_formula(df, result_df, v)
            total_sum += current_sum
            result.append(current_sum)

        if k == "LIC":
            # Check if the formula is valid
            if v is None:
                result.append("")
                continue

            # Check if there is auto-fill value
            if "auto-fill" in v:
                result.append(v["auto-fill"])
                continue

            # Calculate the LIC
            current_sum = eval_formula(df, result_df, v)
            total_sum += current_sum
            result.append(current_sum)

        if k == "TOTAL":
            # Check if there is auto-fill value
            if v is not None and "auto-fill" in v:
                result.append(v["auto-fill"])
                continue

            # Calculate the TOTAL
            result.append(total_sum)

    # Append description
    # logger.info("Calculated result for {} is {}".format(key, result))
    result.insert(0, description)
    return result


def eval_formula(df, result_df, formula):
    """
    This function is used to evaluate the formula
    """
    # Check if the formula is valid
    if formula is None:
        return ""

    # Store calculated value
    result = None

    # Calculate value
    if formula.get("calculate", False):
        if formula.get("self-reference", False):
            # logger.info(f"Self-reference: {formula['self-reference']}")
            # logger.info(f"Formula: {formula['calculate']}")
            result_df.replace("", 0, inplace=True)
            # result_df.to_csv("new_df.csv")
            # logger.info(result_df)
            current_sum = pd.eval(formula["calculate"])
            # logger.info(f"Sum: {sum}, type: {type(sum)}")
            result = round(current_sum, 6)
        else:
            current_sum = df.eval(formula["calculate"]).sum()
            # logger.info(sum)
            result = round(current_sum, 6)

    # Evaluate the expression
    if formula.get("expression", False):
        expression = f"{result} {formula['expression']['condition']}"
        # logger.info("Eval expression: {}".format(expression))

        # Check if the expression is true
        if not eval(expression):
            # Check if replacement is required
            # if formula["expression"]["replace"] == "zero":
            result = 0

        # Check if the negative value is required
        elif formula["expression"].get("positive", False):
            logger.info("Converting to positive value as required")
            result = abs(result)

        # Add extra value if required
        if formula["expression"].get("add_max", False):
            calculate_max = df.eval(formula["expression"]["add_max"]).sum()
            # logger.info("Calculate max: {}".format(calculate_max))
            max_sum = max(calculate_max, 0)
            result += max_sum

        # Check if the negative value is required
        if formula.get("negative", False):
            result = -abs(result)

        # Round up the result
        result = round(result, 6)

    return result
