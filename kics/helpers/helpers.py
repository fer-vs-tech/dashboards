"""
Author: Kamoliddin Usmonov
Date: 2022-12-29
Description: Helper functions for KICS dashboards
"""

import logging

logger = logging.getLogger(__name__)

import datetime
import os
import re

import numpy as np
import pandas as pd

import cm_dashboards.ifrs17_accounting.dash_utils as dash_utils
import cm_dashboards.wvr_data.wvr_functions as wvr_functions


def get_kics_model_name(wvr_path, pattern="KICS"):
    """
    This function returns the right model name for KICS QIS reporting dashboards
    :param wvr_path: path to the WVR file (str) (e.g. 'C:/temp/hanalife/20221228/KICS4.3.wvr)
    :return molde_name: actual model name (str)
    """
    # Define default model name in case not detected
    # or found multiple models within given filter
    model_name = "KICS4.3_DB"

    # Remove file extension .WVR
    wvr_path = wvr_path.replace(".wvr", "")
    model_names = wvr_functions.model_names_in_wvr(wvr_path)
    logger.info("Existing model names: {}".format(model_names))

    # Filter out names based on model names
    filtered_model_names = list(
        filter(
            lambda model_name: model_name.startswith(pattern)
            and "RISK" not in model_name.upper(),
            model_names,
        )
    )
    logger.info("Filtered model names: {}".format(filtered_model_names))

    # Check if filtered model names contains only one value
    if len(filtered_model_names) == 1:
        model_name = filtered_model_names[0]

    logger.info("Detected model name: {}".format(model_name))
    return model_name


def get_df(handler, wvr_path, model_name):
    """
    Get table data from wvr
    :param handler: DB handler
    :param wvr_path: path to wvr file
    :return: DataFrame
    """
    df = handler.get_wvr_data(wvr_path, model_name)
    return df


def get_template_df(
    journal_name, generate_header_rows=True, header=[0], kics_name=None
):
    """
    Get DataFrame by reading template csv file
    :param journal_name: journal name (e.g. "AC")
    :return: DataFrame, list of header rows
    """
    # Get path to template csv file by journal name and make dataframe from it
    current_path = os.path.dirname(os.path.abspath(__file__))
    # go to parent directory
    current_path = os.path.dirname(current_path)

    # Get DataFrame with column
    df = pd.read_csv(
        f"{current_path}\\templates\\{kics_name}\\{journal_name}.csv",
        header=header,
        encoding="utf-8",
    )

    # Rename "Unnamed" columns to empty string
    if len(header) == 1:
        logger.info("Renaming columns for template: {}".format(journal_name))
        df.columns = [remove_substring(col) for col in df.columns]

    # Get header rows
    header_rows = []
    if generate_header_rows:
        for index, row in df.iterrows():  # Iterate over rows
            # Get first cell value
            first_cell_value = row[0]
            # Check if first cell value not starts with empty space
            if (
                isinstance(first_cell_value, str)
                and first_cell_value
                and not first_cell_value.startswith(" ")
            ):
                header_rows.append(index)
    # logger.info("Header rows for {}: {}".format(journal_name, header_rows))
    return df, header_rows


def add_output_formula(df, results, output_column):
    """
    Add output formula to DataFrame
    :param df: DataFrame
    :param results: output results
    :param output_column: column name to be used for output formula to save
    :return: DataFrame
    """
    df[output_column] = df.apply(
        lambda x: set_value(results, "R3S VARIABLE NAME", x["R3S Variable Name"]),
        axis=1,
    )

    # Drop unnecessary columns
    df = df.drop(columns=["R3S Variable Name"])
    return df


def set_value(df, column_name, value):
    """
    Select row by column value and set value to another column
    :param df: DataFrame to be searched
    :param column_name: column name to be used for selection
    :param value: value to be used for selection
    :return: value of the selected row in the column "R3S OUTPUT FORMULA" or 0
    """
    result = 0
    # Special variables that value will be in percentage
    percentage_variables = get_percentage_variables()
    try:
        # Select row by column value
        df = df.loc[df[column_name] == value]
        # If row exists, get value of output formula column
        if len(df) > 0:  # If row exists
            result = df.iloc[0]["R3S OUTPUT FORMULA"].astype(float)
    except Exception as e:
        logger.error("Error occured while setting value: ", e)
    # logger.info(f"Output result for {value}: {result}")

    # Adjust result for some variables
    if value in percentage_variables:
        result = add_sign_and_round(result)

    return result


def add_sign_and_round(value, round_to=2, sign="%", after=True):
    """
    Add sign and round value
    :param value: value to be converted
    :param round_to: number of decimal places to round (default: 2)
    :param sign: sign to be added (default: %)
    :param after: True if sign should be added after value (default: True)
    :return: value in percentage
    """
    try:
        result = value * 100
        # Round to 2 decimal places
        result = round(result, round_to)
        # Convert to positive number
        result = abs(result)
        # Cast to string, add left padding with 0
        if after:
            result = f"{result:.2f}{sign}"
        else:
            result = f"{sign}{result:.2f}"
        return result
    except Exception as e:
        logger.error("Error occured while converting to percentage: ", e)
        return value


def prepare_dropdown_options(df):
    """
    Generate dropdown options
    :param df: DataFrame
    :return: list of dictionaries (value, label, title) for dropdown options
    """
    options = []
    for name in df["Report_Date"]:
        title = name.strftime("Report for %d %B %Y")
        option = {
            "label": name,
            "value": name,
            "title": title,
        }
        options.append(option)
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
    precision=0,
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
            df,
            show_negative_numbers=show_negative_numbers,
            precision=precision,
        )
    else:
        table_data = df.to_dict("records")
        table_columns = df.columns
        columns = dash_utils.set_column_names(
            table_columns,
            precision=precision,
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


def unpivot_df(df):
    """
    Unpivot DataFrame
    :param df: DataFrame
    :return: DataFrame
    """
    # Get list of columns
    columns = df.columns.tolist()

    # Filter out unnecessary columns
    unnecessary_columns = ["KICS Call Date", "KICS Scenario", "Step Date"]
    filtered_columns = [col for col in columns if col not in unnecessary_columns]

    # Unpivot df
    df = df.melt(
        value_vars=filtered_columns,
        var_name="R3S VARIABLE NAME",
        value_name="R3S OUTPUT FORMULA",
    )

    # Change column order
    df = df[["R3S OUTPUT FORMULA", "R3S VARIABLE NAME"]]
    return df


def get_table_name_by_journal_code(journal_code, journal_type="ordinary"):
    """
    Get table name by journal type
    :param journal_code: journal code (e.g. "1-1")
    :param journal_type: journal type (e.g. "ordinary", "with_selection", "mixed")
    :return: table name (str) or None
    """
    tables = {
        "ordinary": {
            "1-1": "A_KICS_PAP_BS",
            "1-13": "A_RC",
            "2-1": "A_AC",
            "2-2": "O_CAPITAL_SECURITIES",
            "2-3": "A_AC",
            "2-5": "A_RC",
            "3-2-1": "A_LIFE_CAT_RISK",
            "3-2-2": "A_LIFE_CAT_RISK",
            "5-1-1": "A_INT_RISK_TOT",
            "5-1-2": "A_INT_RISK_TOT",
            "5-1-3": "A_INT_RISK_TOT",
            "5-1-4": "A_INT_RISK_TOT",
            "5-3": "A_PROPERTY_RISK",
            "5-4": "A_MARKET_RISK",
            "5-5": "O_FOREX_RISK_GROUP",
            "9-12": "A_AC",
            "9-12-5": "O_CAPITAL_SECURITIES",
            "9-12-6": "O_CAPITAL_SECURITIES",
            "9-12-7": "A_COMPANY_KICS_DATA",
        },
        "with_selection": {
            "2-3": {
                "name": "A_AC",
                "columns": "RQUAT_AMT",
            },
            "2-4-2": {
                "name": "A_RC",
                "columns": "LFLT_INSU_RSKA, CRRK_DIRTY_DDAF_AMT, MKRSK_TOT_AMT, ORSK_TOT_AMT",
            },
            "2-5": {
                "name": "A_RC",
                "columns": "ISS_CP_NM, DMOS_DV_NM, Y3_AVG_TXRT, LY_PPD_MCSDAM, Y1B_ACBK_PED_BTPF_AMT, Y2B_ACBK_PED_BTPF_AMT, Y3B_ACBK_PED_BTPF_AMT, Y4B_ACBK_PED_BTPF_AMT, Y5B_ACBK_PED_BTPF_AMT, JB_Y5P_BTPF_AMT, RQUAT_RRAAF_DCTAB_AMT, TITL_CTE_AMT, RPEA_DFCT_AST_MPRC_AMT, RPEA_DFCT_LAT_MPRC_AMT, CTE_LMT_AMT, CTE_ACAM_AMT",
            },
            "9-9": {
                "name": "O_INT_RISK_CUR_GROUP",
                "columns": "QISTR_GRPG_CKND_AMT, IRRKEX_ASTT_BAS_CIRSRP_AMT,IRRKEX_ASTT_AVRC_CIRSRP_AMT,IRRKEX_ASTT_IRU_CIRSRP_AMT,IRRKEX_ASTT_IRDN_CIRSRP_AMT,IRRKEX_ASTT_IRPL_CIRSRP_AMT,IRRKEX_ASTT_IRDC_CIRSRP_AMT,IRRKEX_DHAS_TTAM_BAS_CIRSRP_AMT,IRRKEX_DHAS_TTAM_AVRC_CIRSRP_AMT,IRRKEX_DHAS_TTAM_IRU_CIRSRP_AMT,IRRKEX_DHAS_TTAM_IRDN_CIRSRP_AMT,IRRKEX_DHAS_TTAM_IRPL_CIRSRP_AMT,IRRKEX_DHAS_TTAM_IRDC_CIRSRP_AMT,IRRKEX_DHAS_CASH_BAS_AMT,IRRKEX_DHAS_CASH_AVRC_AMT,IRRKEX_DHAS_CASH_IRU_AMT,IRRKEX_DHAS_CASH_IRDN_AMT,IRRKEX_DHAS_CASH_IRPL_AMT,IRRKEX_DHAS_CASH_IRDC_AMT,IRRKEX_DHAS_BOND_BAS_AMT,IRRKEX_DHAS_BOND_AVRC_AMT,IRRKEX_DHAS_BOND_IRU_AMT,IRRKEX_DHAS_BOND_IRDN_AMT,IRRKEX_DHAS_BOND_IRPL_AMT,IRRKEX_DHAS_BOND_IRDC_AMT,IRRKEX_DHAS_LOAN_BAS_AMT,IRRKEX_DHAS_LOAN_AVRC_AMT,IRRKEX_DHAS_LOAN_IRU_AMT,IRRKEX_DHAS_LOAN_IRDN_AMT,IRRKEX_DHAS_LOAN_IRPL_AMT,IRRKEX_DHAS_LOAN_IRDC_AMT,IRRKEX_DHAS_NOAS_BAS_AMT,IRRKEX_DHAS_NOAS_AVRC_AMT,IRRKEX_DHAS_NOAS_IRU_AMT,IRRKEX_DHAS_NOAS_IRDN_AMT,IRRKEX_DHAS_NOAS_IRPL_AMT,IRRKEX_DHAS_NOAS_IRDC_AMT,IRRKEX_DHAS_RINSAT_RINSAT_UP_AMT,IRRKEX_DHAS_RINSAT_AVRC_AMT,IRRKEX_DHAS_RINSAT_IRU_AMT,IRRKEX_DHAS_RINSAT_IRDN_AMT,IRRKEX_DHAS_RINSAT_IRPL_AMT,IRRKEX_DHAS_RINSAT_IRDC_AMT,IRRKEX_DHAS_DRVT_BAS_AMT,IRRKEX_DHAS_DRVT_AVRC_AMT,IRRKEX_DHAS_DRVT_IRU_AMT,IRRKEX_DHAS_DRVT_IRDN_AMT,IRRKEX_DHAS_DRVT_IRPL_AMT,IRRKEX_DHAS_DRVT_IRDC_AMT,IRRKEX_DHAS_OTH_AMT,IRRKEX_DHAS_OTH_AMT,IRRKEX_DHAS_OTH_AMT,IRRKEX_DHAS_OTH_AMT,IRRKEX_DHAS_OTH_AMT,IRRKEX_DHAS_OTH_AMT,IRRKEX_IDOW_TTAM_BAS_CIRSRP_AMT,IRRKEX_IDOW_TTAM_AVRC_CIRSRP_AMT,IRRKEX_IDOW_TTAM_IRU_CIRSRP_AMT,IRRKEX_IDOW_TTAM_IRDN_CIRSRP_AMT,IRRKEX_IDOW_TTAM_IRPL_CIRSRP_AMT,IRRKEX_IDOW_TTAM_IRDC_CIRSRP_AMT,IRRKEX_IDOW_CASH_BAS_AMT,IRRKEX_IDOW_CASH_AVRC_AMT,IRRKEX_IDOW_CASH_IRU_AMT,IRRKEX_IDOW_CASH_IRDN_AMT,IRRKEX_IDOW_CASH_IRPL_AMT,IRRKEX_IDOW_CASH_IRDC_AMT,IRRKEX_IDOW_BOND_BAS_AMT,IRRKEX_IDOW_BOND_AVRC_AMT,IRRKEX_IDOW_BOND_IRU_AMT,IRRKEX_IDOW_BOND_IRDN_AMT,IRRKEX_IDOW_BOND_IRPL_AMT,IRRKEX_IDOW_BOND_IRDC_AMT,IRRKEX_IDOW_LOAN_BAS_AMT,IRRKEX_IDOW_LOAN_AVRC_AMT,IRRKEX_IDOW_LOAN_IRU_AMT,IRRKEX_IDOW_LOAN_IRDN_AMT,IRRKEX_IDOW_LOAN_IRPL_AMT,IRRKEX_IDOW_LOAN_IRDC_AMT,IRRKEX_IDOW_NOAS_BAS_AMT,IRRKEX_IDOW_NOAS_AVRC_AMT,IRRKEX_IDOW_NOAS_IRU_AMT,IRRKEX_IDOW_NOAS_IRDN_AMT,IRRKEX_IDOW_NOAS_IRPL_AMT,IRRKEX_IDOW_NOAS_IRDC_AMT,IRRKEX_IDOW_DRVT_BAS_AMT,IRRKEX_IDOW_DRVT_AVRC_AMT,IRRKEX_IDOW_DRVT_IRU_AMT,IRRKEX_IDOW_DRVT_IRDN_AMT,IRRKEX_IDOW_DRVT_IRPL_AMT,IRRKEX_IDOW_DRVT_IRDC_AMT,IRRKEX_IDOW_OTH_AMT,IRRKEX_IDOW_OTH_AMT,IRRKEX_IDOW_OTH_AMT,IRRKEX_IDOW_OTH_AMT,IRRKEX_IDOW_OTH_AMT,IRRKEX_IDOW_OTH_AMT,IRRKEX_LBTT_BAS_CIRSRP_AMT,IRRKEX_LBTT_AVRC_CIRSRP_AMT,IRRKEX_LBTT_IRU_CIRSRP_AMT,IRRKEX_LBTT_IRDN_CIRSRP_AMT,IRRKEX_LBTT_IRPL_CIRSRP_AMT,IRRKEX_LBTT_IRDC_CIRSRP_AMT,IRRKEX_DHLB_TTAM_BAS_CIRSRP_AMT,IRRKEX_DHLB_TTAM_AVRC_CIRSRP_AMT,IRRKEX_DHLB_TTAM_IRU_CIRSRP_AMT,IRRKEX_DHLB_TTAM_IRDN_CIRSRP_AMT,IRRKEX_DHLB_TTAM_IRPL_CIRSRP_AMT,IRRKEX_DHLB_TTAM_IRDC_CIRSRP_AMT,IRRKEX_DHLB_OCNT_PELBT_BAS_AMT,IRRKEX_DHLB_OCNT_PELBT_RGRS_AMT,IRRKEX_DHLB_OCNT_PELBT_UP_AMT,IRRKEX_DHLB_OCNT_PELBT_DOWN_AMT,IRRKEX_DHLB_OCNT_PELBT_FLAT_AMT,IRRKEX_DHLB_OCNT_PELBT_SLOPE_AMT,IRRKEX_DHLB_NINLB_BAS_CIRSRP_AMT,IRRKEX_DHLB_NINLB_AVRC_CIRSRP_AMT,IRRKEX_DHLB_NINLB_IRU_CIRSRP_AMT,IRRKEX_DHLB_NINLB_IRDN_CIRSRP_AMT,IRRKEX_DHLB_NINLB_IRPL_CIRSRP_AMT,IRRKEX_DHLB_NINLB_IRDC_CIRSRP_AMT,IRRKEX_DHLB_BWAM_BAS_CIRSRP_AMT,IRRKEX_DHLB_BWAM_AVRC_CIRSRP_AMT,IRRKEX_DHLB_BWAM_IRU_CIRSRP_AMT,IRRKEX_DHLB_BWAM_IRDN_CIRSRP_AMT,IRRKEX_DHLB_BWAM_IRPL_CIRSRP_AMT,IRRKEX_DHLB_BWAM_IRDC_CIRSRP_AMT,IRRKEX_DHLB_AOBW_BAS_CIRSRP_AMT,IRRKEX_DHLB_AOBW_AVRC_CIRSRP_AMT,IRRKEX_DHLB_AOBW_IRU_CIRSRP_AMT,IRRKEX_DHLB_AOBW_IRDN_CIRSRP_AMT,IRRKEX_DHLB_AOBW_IRPL_CIRSRP_AMT,IRRKEX_DHLB_AOBW_IRDC_CIRSRP_AMT,IRRKEX_DHLB_DRVT_BAS_AMT,IRRKEX_DHLB_DRVT_AVRC_AMT,IRRKEX_DHLB_DRVT_IRU_AMT,IRRKEX_DHLB_DRVT_IRDN_AMT,IRRKEX_DHLB_DRVT_IRPL_AMT,IRRKEX_DHLB_DRVT_IRDC_AMT,IRRKEX_DHLB_OTH_AMT,IRRKEX_DHLB_OTH_AMT,IRRKEX_DHLB_OTH_AMT,IRRKEX_DHLB_OTH_AMT,IRRKEX_DHLB_OTH_AMT,IRRKEX_DHLB_OTH_AMT,IRRKEX_IHAST_TTAM_BAS_CIRSRP_AMT,IRRKEX_IHAST_TTAM_AVRC_CIRSRP_AMT,IRRKEX_IHAST_TTAM_IRU_CIRSRP_AMT,IRRKEX_IHAST_TTAM_IRDN_CIRSRP_AMT,IRRKEX_IHAST_TTAM_IRPL_CIRSRP_AMT,IRRKEX_IHAST_TTAM_IRDC_CIRSRP_AMT,IRRKEX_IHAST_BWAM_BAS_AMT,IRRKEX_IHAST_BWAM_AVRC_AMT,IRRKEX_IHAST_BWAM_IRU_AMT,IRRKEX_IHAST_BWAM_IRDN_AMT,IRRKEX_IHAST_BWAM_IRPL_AMT,IRRKEX_IHAST_BWAM_IRDC_AMT,IRRKEX_IHAST_DRVT_BAS_AMT,IRRKEX_IHAST_DRVT_AVRC_AMT,IRRKEX_IHAST_DRVT_IRU_AMT,IRRKEX_IHAST_DRVT_IRDN_AMT,IRRKEX_IHAST_DRVT_IRPL_AMT,IRRKEX_IHAST_DRVT_IRDC_AMT,IRRKEX_IHAST_OTH_AMT,IRRKEX_IHAST_OTH_AMT,IRRKEX_IHAST_OTH_AMT,IRRKEX_IHAST_OTH_AMT,IRRKEX_IHAST_OTH_AMT,IRRKEX_IHAST_OTH_AMT,NASVAL_BAS_CIRSRP_AMT,NASVAL_AVRC_CIRSRP_AMT,NASVAL_IRU_CIRSRP_AMT,NASVAL_IRDN_CIRSRP_AMT,NASVAL_IRPL_CIRSRP_AMT,NASVAL_IRDC_CIRSRP_AMT",
            },
            "6-5": {
                "name": "O_CREDIT_RISK_REINS",
                "columns": "*",
            },
            "9-11": {
                "name": "O_CREDIT_RISK_REINS",
                "columns": "KICS_EXPI_MNCT, KICS_CRRT_NM, TRSC_NO, CREP_CRDT_REINS_PMLB_DDB_AMT, CREP_CRDT_REINS_RSLB_DDB_AMT",
            },
        },
        "mixed": {
            "2-4-1": {
                "RC": {
                    "name": "A_RC",
                    "columns": "RQUAT_DCTAA_AMT, CTE_ACAM_AMT, RQUAT_RRAAF_DCTAB_AMT, TOT__DEFT_AMT, LFLT_INSU_RSKA, MKRSK_TOT_AMT, CRRK_DIRTY_DDAF_AMT, ORSK_TOT_AMT, RQUAT_DCTAA_AMT",
                },
                "LIFE_RISK_TOT": {
                    "name": "A_LIFE_RISK_TOT",
                    "columns": "INSU_DTL_RSK_SUMA_DEFT_VLU, DTH_RSK_CLRITC_AMT, LGV_RSK_CLRITC_AMT, DSDS_RSK_CLRITC_AMT, CNC_RSK_CLRITC_AMT, BZCF_RSK_CLRITC_AMT, CTDS_RSK_VLU",
                },
                "MARKET_RISK": {
                    "name": "A_MARKET_RISK",
                    "columns": "MRSK_DEFT_AMT, IRRSK_TTAM_AMT, STK_RSKA, PPRSKA_AMT, FRSAM_TOT_AMT, ASFC_RSKA_TOT_AMT",
                },
            },
            "5-2": {
                "EQUITY_RISK": {
                    "name": "A_EQUITY_RISK",
                },
                "MARKET_RISK": {
                    "name": "A_MARKET_RISK",
                },
            },
            "5-4": {
                "MARKET_RISK": {
                    "name": "A_MARKET_RISK",
                    "columns": "FRSAM_ERTU_TOT_AMT, FRSAM_ERTD_TOT_AMT, FRSAM_RPCVA_AMT as FRSAM_RPCVA_AMT_TOT, FRSAM_TOT_AMT",
                },
                "FOREX_RISK_GROUP": {
                    "name": "O_FOREX_RISK_GROUP",
                    "columns": "FRSAM_GRPG_IDTFR_AMT, FRSAM_ERTU_AMT, FRSAM_ERTD_AMT, FRSAM_RPCVA_AMT",
                },
            },
            "5-6": {
                "G_RISK_GROUP": {
                    "name": "O_CONCEN_G_RISK_GROUP",
                    "columns": "ASFRS_SPRT_NM, KICS_CRRT_NM, TPTN_CNRSK_EXPS_DPST_CLN_AMT, TPTN_CNRSK_EXPS_STBD_CLN_AMT, TPTN_CNRSK_EXPS_CRGT_CLN_AMT, TPTN_CNRSK_EXPS_OUBND_AMT, TPTN_CNRSK_EXPS_DRVT_CLN_AMT, TPTN_CNRSK_EXPS_OITM_CLN_AMT, ASFRS_SGRP_EXPS_AMT, ASFRS_SGRP_LMT_CLNM_AMT, ASFRS_SGRP_LIEXD_EXPS_AMT, ASFRS_SGRP_RSKA",
                },
                "P_RISK_GROUP": {
                    "name": "O_CONCEN_P_RISK_GROUP",
                    "columns": "ASFRS_SPRT_NM, PPPT_ASFC_RSKEP_AMT,PPPT_LMT_CLNM, PPPT_LIEXD_ASFREP_AMT, PPPT_ASFC_RSKA, PPPT_ASFC_RSKA",
                },
                "MARKET_RISK": {
                    "name": "A_MARKET_RISK",
                    "columns": "FV_AMT, TPRP_ASFRS_EXPS_AMT, TPRP_LMT_CLNM, TPRP_LIEXD_ASFRS_EXPS_AMT, TPRP_ASFC_RSKA, ASFC_RSKA_TOT_AMT, ASFRS_SGRP_RSKA as ASFRS_SGRP_RSKA_M, PRPT_ASFRS_FNL_EXPS_AMT",
                },
            },
            "9-12-7": {
                "AC": {
                    "name": "A_AC",
                    "columns": "CSAT_TAMT, CSAT_NINC_TAMT, CSAT_SCDR_DCTA_AMT, CSAT_SCDR_DCTL_AMT, CSAT_LAT_RQUAT_AMT, CSCPV_RRC_EXCS_AMT",
                },
                "KICS": {
                    "name": "A_COMPANY_KICS_DATA",
                    "columns": "CSAT_IN_CBDM_AMT, CSAT_IN_CBGN_AMT, CSAT_IN_CBIGD_AMT, CSAT_IN_CBIGU_AMT, CSAT_IN_CNDPS_AMT, CSAT_IN_IVPT_AMT, CSAT_IN_NTBND_AMT, CSAT_IN_OAST_AMT, CSAT_IN_PBBND_AMT, CSAT_IN_SFPRT_AMT, CSAT_IN_STK_AMT",
                },
            },
            "6-1": {
                "CREDIT_RISK_TOT": {
                    "name": "A_CREDIT_RISK_TOT",
                    "columns": "CRSCR_OAST_CLEANDB_AMT, CRSCR_REINS_DDB_AMT, CRDCLCR_OAST_CLN_AMT, CRDGTCR_OAST_CLN_AMT",
                },
                "CREDIT_RISK": {
                    "name": "O_CREDIT_RISK",
                    "columns": "CRRK_MCLSF_NM, RDYN_AVCLT_AMT, CRDGT_DIRTY_AMT, CRSAM_CLEANDB_AMT, CRDCL_DIRTY_AMT",
                },
            },
            "6-2": {
                "CREDIT_RISK_TOT": {
                    "name": "A_CREDIT_RISK_TOT",
                    "columns": "*",
                },
                "CREDIT_RISK": {
                    "name": "O_CREDIT_RISK",
                    "columns": "*",
                },
                "CREDIT_RISK_OTHER": {
                    "name": "O_CREDIT_RISK_OTHER",
                    "columns": "CREP_CRDT_OAST_PCOAS_CLEANDB_AMT",
                },
            },
        },
    }

    result = None
    try:
        result = tables[journal_type][journal_code]
    except KeyError:
        pass
    logger.info(f"Selected journal: {journal_code} - {journal_type}")
    return result


def insert_actual_values(
    output_df, results_df, variables, start_row_index=0, start_col_index=0
):
    """
    Insert actual values to DataFrame
    :param output_df: DataFrame
    :param results_df: DataFrame with results
    :param variables: list of variables
    :param start_row_index: start row index (default: 0)
    :param start_col_index: start column index (default: 0)
    :return: DataFrame
    """
    logger.info("Inserting actual values...")
    for index, row in results_df.iterrows():
        # Convert current row to dictionary
        result_dict = row.to_dict()
        percentage_variables = get_percentage_variables()

        # Insert actual values to output DataFrame by variable name respectively
        updated_values = list()
        for variable in variables:
            # Check if variable is valid (not Unknown)
            if "Unnamed" in variable:
                updated_values.append("")
                continue

            # Get value from results df
            value = result_dict.get(variable, "")

            # Check if variable is percentage variable
            if variable in percentage_variables:
                value = add_sign_and_round(value)

            # Set value to output df
            updated_values.append(value)

        # Update output df with actual values by index
        # Skip the first column as it is the index
        output_df.iloc[index + start_row_index, start_col_index:] = updated_values

    return output_df


def remove_substring(string):
    """
    Remove substring from string
    :param string: string
    :return: string
    """
    if "." in string:
        string = string.split(".")[0]
    if "Unnamed" in string:
        string = ""
    return string


def apply_formatting(cell_value, lookup_dict):
    """
    Apply formatting to cell value
    :param cell_value: cell value
    :param lookup_dict: lookup dictionary
    :return: formatted cell value with replacement value if applicable
    """
    if pd.isna(cell_value) or pd.isnull(cell_value) or cell_value == "":
        return cell_value

    if lookup_dict is None or cell_value not in lookup_dict.keys():
        return cell_value

    percentage_variables = get_percentage_variables()
    # Remove substring from cell value if possible
    try:
        new_value = lookup_dict.get(cell_value, cell_value)
    except Exception as e:
        logger.info("Error occurred: {}".format(e))
        new_value = cell_value

    # Cast cell value to float if possible
    if not isinstance(new_value, (float, datetime.date)) and new_value.isdigit():
        new_value = float(new_value)

    # Check if cell value is percentage
    if cell_value in percentage_variables:
        new_value = add_sign_and_round(new_value)

    return new_value


def replace_template_values(
    template_df, lookup_dict, use_applymap=False, helper_df=None, product_sum=None
):
    """
    Replace template values by checking
    """
    df = template_df.copy()
    # Use applymap to replace values if there is no formula in the template
    if use_applymap:
        df = df.applymap(lambda x: apply_formatting(x, lookup_dict))
        return df

    # logger.info("Replacing template values...")
    columns = df.columns.tolist()
    # logger.info("Columns: {}".format(columns))
    calculate_formulas = list()

    # Iterate through each cell in template df
    for row_index, row in df.iterrows():
        # logger.info("Processing row {}".format(row_index))
        for current_column, cell_value in row.items():
            # Get current column name
            column_index = columns.index(current_column)

            # Replace cell value by checking
            new_value = lookup_and_replace(
                cell_value,
                lookup_dict,
                row_index,
                column_index,
                current_column,
                calculate_formulas,
            )

            # logger.info(
            #     "Row index: {}, Column index: {}".format(row_index, current_column)
            # )
            if isinstance(new_value, list) or isinstance(new_value, tuple):
                new_value = "IN PROGRESS"
            df.loc[row_index, current_column] = new_value

    logger.info("Finished replacing template values")

    # # Calculate formulas
    max_iterations = 0
    if len(calculate_formulas) > 0 and max_iterations < 10:
        calculate_formula(
            df,
            calculate_formulas,
            max_iterations,
            helper_df=helper_df,
            product_sum=product_sum,
        )

    return df


def lookup_and_replace(
    cell_value,
    lookup_dict,
    row_index,
    column_index,
    current_column,
    calculate_formulas,
):
    """
    Replace template cell values by checking
    :param cell_value: cell value (str)
    :param lookup_dict: Dictionary with lookup values (dict)
    :param row_index: row index (int)
    :param column_index: column index (int)
    :param current_column: current column name (str)
    :param calculate_formulas: list of formulas to calculate (list)
    :return: replaced cell value (str)
    """
    if pd.isna(cell_value) or pd.isnull(cell_value) or cell_value == "":
        return cell_value

    percentage_variables = get_percentage_variables()

    # Check if lookup dictionary is not empty or not None
    if lookup_dict is not None:
        # Check if cell value contains double key
        if isinstance(cell_value, str) and "VARIABLES" in cell_value:
            # Extract variables and operation
            var1, var2, operation = cell_value.replace("VARIABLES=", "").split("|")

            # Get values from lookup dictionary
            value1 = lookup_dict.get(var1, 0)
            value2 = lookup_dict.get(var2, 0)
            # Calculate new value
            new_value = calculate(value1, value2, operation)

            return new_value

        # Check if cell value is R3S variable name
        if isinstance(cell_value, str) and cell_value.strip() in lookup_dict.keys():
            new_value = lookup_dict[cell_value.strip()]

            # Check if it is percentage variable
            if (
                current_column in percentage_variables
                or cell_value in percentage_variables
            ):
                new_value = add_sign_and_round(new_value)

            # logger.info("Replacement for {}: {}".format(cell_value, new_value))
            return new_value

    # Check if any formula type is in cell value and add to calculate formulas
    formula_types = get_priority_level("ALL")
    if isinstance(cell_value, str) and any(
        formula_type in cell_value for formula_type in formula_types
    ):
        # Translate formula to pandas eval format
        eval_formula, formula_type, priority = transform_formula_to_eval(
            cell_value, column_index, row_index
        )
        calculate_formulas.append(
            {
                "index": row_index,
                "column": current_column,
                "formula": eval_formula,
                "formula_type": formula_type,
                "priority": priority,
            }
        )
        return eval_formula

    # Cast cell value to float if possible
    if not isinstance(cell_value, float) and cell_value.isdigit():
        cell_value = float(cell_value)

    # Return cell value without change if not found
    return cell_value


def calculate_formula(
    df, calculate_formulas, max_iteration, helper_df=None, product_sum=None
):
    """
    Calculate formula
    :param df: dataframe (pd.DataFrame)
    :param calculate_formulas: list of formulas to calculate (list)
    :param max_iteration: max iteration (int)
    :param helper_df: helper dataframe (pd.DataFrame)
    :return: dataframe with calculated formulas (pd.DataFrame)
    """
    logger.info(f"Current iteration: {max_iteration + 1}")
    logger.info(f"Calculating {len(calculate_formulas)} formulas...")
    later_calculations = []

    # Sort formulas by priority (SUMIF first)
    calculate_formulas.sort(key=lambda x: x["priority"])

    # Iterate through each formula
    for calculation in calculate_formulas:
        index = calculation["index"]
        column = calculation["column"]
        formula = calculation["formula"]
        formula_type = calculation["formula_type"]
        priority = calculation["priority"]
        # logger.info(
        #     "Priority: {}, index: {}, calculation type: {}".format(
        #         priority, index, formula_type
        #     )
        # )

        # Calculate formula
        result = 0
        calculation_note = "IN PROGRESS"
        try:
            match priority:
                # Calculate SUMRANGES formula
                case 0:
                    # Check if helper df is not None
                    if helper_df is not None:
                        # Loop through each formula range
                        for formula_index in formula:
                            # Split formula into query and eval formula
                            query_formula, eval_formula = formula_index
                            # Create mask df to filter rows by query formula
                            mask_df = helper_df.query(query_formula)
                            # Evaluate formula on mask df
                            sum_mask_df = mask_df.eval(eval_formula)
                            result += sum_mask_df

                # Calculate SUMIF formula
                case 1:
                    # Check if helper df is not None
                    if helper_df is not None:
                        # Split formula into query and eval formula
                        query_formula, eval_formula = formula

                        # logger.info("Query formula: {}".format(query_formula))
                        # logger.info("Eval formula: {}".format(eval_formula))

                        # Create mask df to filter rows by query formula
                        mask_df = helper_df.query(query_formula)
                        # logger.info(f"Mask DF: {mask_df}")

                        # Evaluate formula on mask df
                        if isinstance(eval_formula, list):
                            sum_result = mask_df.eval(eval_formula[0])
                            variable_value = mask_df.eval(eval_formula[1]).values[0]
                            result = sum_result + variable_value
                        else:
                            result = mask_df.eval(eval_formula)
                    # logger.info("Result: {}".format(result))

                # Calculate SUM_COLUMN formula
                case 2 if formula_type == "SUM_COLUMN":
                    # Get column index, row range and row index
                    column_index, row_index_range, row_index_single = formula

                    # Extract start and end index from formula
                    start, end = row_index_range

                    # logger.info("Column index: {}".format(column_index))
                    # logger.info("Row index range: {}".format(row_index_range))
                    # logger.info("Row index single: {}".format(row_index_single))

                    # Create mask df to filter rows by start and end index
                    mask_df = df.iloc[start : end + 1, column_index]

                    # Sum mask df
                    result = mask_df.sum(skipna=True)

                    # Add sum for single selection
                    if row_index_single is not None:
                        extra_row = df.iloc[row_index_single, column_index]
                        result += extra_row.sum()

                    # logger.info("Result for SUM COLUMN: {}".format(result))

                # Calculate MAX, COPY formula
                case 2 if formula_type != "SUM_COLUMN":
                    result = pd.eval(formula)
                    result = max(result, 0)

                # Calculate SUM_ROW formula
                case 3:
                    # Extract start and end index from formula
                    start, end = formula

                    # Create mask row to filter columns by start and end index
                    mask_row = df.iloc[index, start : end + 1]

                    # Sum mask row
                    result = mask_row.sum(skipna=True)

                    # Check to prevent summation of formula itself when recalation needed
                    if isinstance(result, str) or isinstance(result, list):
                        # Preserve formula for later calculation
                        result = calculation_note
                        later_calculations.append(calculation)

                    # logger.info("Result for SUM ROW: {}".format(result))
                    # logger.info("Formula for SUM ROW: {}".format(formula))

                # Calculate comparison formula
                case 4:
                    # Split formula into two parts
                    split_formula = formula.split("==")

                    # Evaluate both sides of the formula
                    a, b = list(map(pd.eval, split_formula))

                    # Compare and convert to string
                    result = str(int(a) == int(b))

                # Calculate SFORMULA, MFORMULA formula
                case 5 if formula_type in ["SFORMULA", "MFORMULA"]:
                    # Get column index, row range and row index
                    column_index, row_index_range, row_index_single = formula

                    # Extract start and end index from formula
                    start, end = row_index_range

                    # logger.info("Column index: {}".format(column_index))
                    # logger.info("Row index range: {}".format(row_index_range))
                    # logger.info("Row index single: {}".format(row_index_single))

                    # Create mask df to filter rows by start and end index
                    mask_df = df.iloc[start : end + 1, column_index]

                    # Sum mask df
                    result = mask_df.sum(skipna=True)

                    # Add sum for single selection
                    if row_index_single is not None:
                        extra_row = df.iloc[row_index_single, column_index]
                        result += extra_row.sum()

                    # Check to prevent summation of formula itself when recalation needed
                    if isinstance(result, str) or isinstance(result, list):
                        # Preserve formula for later calculation
                        result = calculation_note
                        later_calculations.append(calculation)

                    # Check if formula type is MFORMULA
                    elif formula_type == "MFORMULA":
                        result = max(result, 0)
                        # logger.info("MFORMULA result: {}".format(result))

                # Calculate FORMULA
                case 5 if formula_type in ["SUMIFPOSITIVE"]:
                    row_ids, col_id = formula
                    calc_result = None
                    for row_id in row_ids:
                        current_cell = df.iloc[row_id, col_id]

                        # Check to prevent summation of formula itself when recalation needed
                        if (
                            isinstance(current_cell, str)
                            or isinstance(current_cell, list)
                            or isinstance(current_cell, tuple)
                        ):
                            # Preserve formula for later calculation
                            result = calculation_note
                            later_calculations.append(calculation)
                            break

                        if calc_result is None:
                            calc_result = max(current_cell, 0)
                        else:
                            calc_result += max(current_cell, 0)

                    result = calc_result

                # Calculate FORMULA
                case 5 if formula_type not in [
                    "SFORMULA",
                    "MFORMULA",
                    "SUM_COLUMN_RANGES",
                    "SUMIFPOSITIVE",
                ]:
                    result = pd.eval(formula)
                    # Check to prevent summation of formula itself when recalation needed
                    if (
                        isinstance(result, str)
                        or isinstance(result, list)
                        or isinstance(result, tuple)
                    ):
                        # Preserve formula for later calculation
                        result = calculation_note
                        later_calculations.append(calculation)

                # Calculate PRODUCTSUM formula
                case 6:
                    # Get indexes (start and end)
                    start, end, only_positive_valus = formula
                    # Get product sum and df row for current index
                    row_product_sum = product_sum.iloc[index].tolist()
                    row_df = df.iloc[index, start:end].tolist()

                    # Normalize row df, replace negative values with 0
                    if only_positive_valus:
                        row_df = [max(0, x) for x in row_df]

                    # logger.info("Product sum: {}".format(row_product_sum))
                    # logger.info("Row df: {}".format(row_df))

                    result = sum_product(row_product_sum, row_df)

                # Calculate RATIO formula
                case 7:
                    # Eval pandas formula
                    x_cell, y_cell = formula
                    x_value = pd.eval(x_cell)
                    y_value = pd.eval(y_cell)
                    logger.info("X value: {}, Y value: {}".format(x_value, y_value))
                    try:
                        result = x_value / y_value
                        result = add_sign_and_round(result)
                    except ZeroDivisionError:
                        logger.error("Division by zero error")
                        result = 0
                    logger.info("Result for RATIO: {}".format(result))

                # Calculate SUM_COLUMN_RANGES
                case 8:
                    for row_indexes in formula:
                        start, end, column_index = row_indexes
                        # Create mask df to filter rows by start and end index
                        mask_df = df.iloc[start : end + 1, column_index]
                        # Sum mask df
                        sum_rows = mask_df.sum(skipna=True)
                        result += sum_rows

                    # Check to prevent summation of formula itself when recalation needed
                    if isinstance(result, str):
                        # Preserve formula for later calculation
                        result = calculation_note
                        later_calculations.append(calculation)

                # Calculate EVAL formula
                case 9:
                    result = pd.eval(formula)
                    result = str(round(result, 2))

                # Calculate other formula
                case _:
                    result = 0

            # Replace cell value with result
            df.loc[index, column] = result
            # logger.info("Formula: {}, Result: {}".format(formula, result))

        except Exception as e:
            # logger.error(
            #     "Error calculating formula: {}\nFormula: {}, Formula type: {}".format(
            #         e, formula, formula_type
            #     )
            # )
            later_calculations.append(calculation)
            continue

    logger.info("Finished calculating formula")
    logger.info(f"Later calculations: {len(later_calculations)} left")

    # If there are later calculations, calculate them
    if len(later_calculations) > 0 and max_iteration < 10:
        calculate_formula(
            df,
            later_calculations,
            max_iteration + 1,
            helper_df=helper_df,
            product_sum=product_sum,
        )

    return df


def sum_product(*arrays):
    """
    Calculate sum product of arrays
    :param arrays: list of arrays (list)
    :return: sum product (float)
    """
    # Convert to numpy array
    arrays = [np.array(array) for array in arrays]

    # Replace na, nan, str values with 0 in arrays to prevent errors
    arrays = list(
        map(
            lambda x: list(
                map(
                    lambda y: 0
                    if pd.isna(y) or isinstance(y, str) or y == np.nan
                    else y,
                    x,
                )
            ),
            arrays,
        )
    )

    # Sum product
    product = np.prod(arrays, axis=0)
    result = np.sum(product) / 100
    # logger.info("Sum product: {}".format(result))

    return result


def transform_formula_to_eval(evaluation, column_index, row_index):
    """
    Transform formula to pandas eval format
    :param evaluation: evaluation formula (str)
    :param column_index: column index (int)
    :param row_index: row index (int)
    :return: transformed formula, formula type, priority level (list)
    """
    formula_type, formula = evaluation.split("=", 1)

    # Replace indexes with column names
    match formula_type.strip():
        # Query data with given parameters and sum up
        case "SUMIF":
            # Define query and eval formula
            query_formula = None
            sum_formula = None

            # Get real variable name
            variables = get_masked_variables()

            # Split formula by pipe (|) to get if conditions
            conditions = formula.split("|")
            # logger.info("Conditions: {}".format(conditions))
            for condition in conditions:
                # logger.info("Condition: {}".format(condition))

                # Split condition by colon (:) to get column and value to make if expression
                column, value = condition.split(":")

                # Replace column with real variable name if exists
                column = variables.get(column, column)

                # If column is SUM, make query formula
                if column == "SUM":
                    if "+" in value:
                        value = value.split("+")
                        sum_variable, second_variable = [
                            variables.get(v, v) for v in value
                        ]
                        sum_formula = [f"{sum_variable}.sum()", second_variable]
                    else:
                        # Replace value with real variable name if exists
                        value = variables.get(value, value)
                        sum_formula = f"{value}.sum()"
                    continue

                # Try to cast value to float if possible
                # If successful, remove single quotes from query formula
                query_mask = f"{column} == '{value}'"
                try:
                    value = float(value)
                    query_mask = f"{column} == {value}"
                except ValueError:
                    pass

                # Bypass above casting if value must be string
                # Remove STR from value and add single quotes to query formula
                if isinstance(value, str) and value.endswith("STR"):
                    value = value.replace("STR", "")
                    # logger.info("Value is string: {}".format(value))
                    query_mask = f"{column} == '{value}'"
                elif isinstance(value, str):
                    query_mask = f"{column} == '{value}'"

                # Add "and" to eval formula if it is not the first condition
                if query_formula is None:
                    query_formula = f"{query_mask}"
                else:
                    query_formula += f" and {query_mask}"

            # Return result as tuple (query formula and eval formula)
            eval_formula = (query_formula, sum_formula)

        # Calculate col value(s) by given range of indexes formula (manual input)
        case "FORMULA":
            # Can be single range or multiple ranges, manually inputted
            eval_formula = re.sub(
                r"\d+", f"df.iloc[\\g<0>].values[{column_index}]", formula
            )

        # Sum column value(s) by given range of indexes formula
        case "SUM_COLUMN" | "SFORMULA" | "MFORMULA":
            # Can be multiple ranges separated by comma (:) and single range separated by comma (,)
            row_index_single = None
            row_index_range = None

            # Check if there is also single range selection
            if "," in formula:
                ranges, row_index_single = formula.split(",")
                row_index_single = int(row_index_single)
            else:
                ranges = formula

            # Extract start and end index
            row_index_range = list(map(int, ranges.split(":")))
            eval_formula = column_index, row_index_range, row_index_single

        # Sum column value(s) by given range of indexes formula
        case "SUM_COLUMN_RANGES":
            eval_formula = list()

            for index_range in formula.split(","):
                # Extract start and end index
                # Sample: 1:3, 5:7, 9:11
                index_range_list = list(map(int, index_range.split(":")))
                index_range_list.append(column_index)
                eval_formula.append(index_range_list)

        # Calculate MAX formula
        case "MAX":
            eval_formula = re.sub(
                r"\d+", f"df.iloc[{row_index}].values[\\g<0>]", formula
            )

        # Sum row formula
        case "SUM_ROW":
            # Extract start and end index
            start, end = list(map(int, formula.split(":")))
            eval_formula = (start, end)

            # logger.info("Eval formula: {}".format(eval_formula))

        # Copy cell value formula
        case "COPY":
            copy_col_index = int(formula)
            eval_formula = f"df.iloc[{row_index}].values[{copy_col_index}]"

        # Comparision formula
        case "COMPARISION":
            eval_formula = re.sub(
                r"\d+", f"df.iloc[{row_index}].values[\\g<0>]", formula
            )

        # Product sum formula
        case "PRODUCTSUM":
            only_positive_values = False
            if "POSITIVE" in formula:
                formula, _ = formula.split("|")
                only_positive_values = True

            # Extract start and end index (column index)
            start, end = list(map(int, formula.split(":")))
            eval_formula = start, end, only_positive_values

        # Ratio formula
        case "RATIO":
            x, y = list(map(int, formula.split("/")))
            x_cell = f"df.iloc[{x}].values[{column_index}]"
            y_cell = f"df.iloc[{y}].values[{column_index}]"
            eval_formula = [x_cell, y_cell]

        # Query data with given parameters and sum up
        case "SUMRANGES":
            eval_formula = list()
            variables = get_masked_variables()
            sum_ranges = formula.split("+")
            for sum_range in sum_ranges:
                # Define query and eval formula for each sum range
                query_formula = None
                sum_formula = None

                # Split formula by pipe (|) to get if conditions
                conditions = sum_range.split("|")
                logger.info("Conditions: {}".format(conditions))
                for condition in conditions:
                    # Split condition by colon (:) to get column and value to make if expression
                    column, value = condition.split(":")
                    # Replace column with real variable name if exists
                    column = variables.get(column, column)
                    # If column is SUM, make query formula
                    if column == "SUM":
                        # Replace value with real variable name if exists
                        value = variables.get(value, value)
                        sum_formula = f"{value}.sum()"
                        continue

                    # Try to cast value to float if possible
                    # If successful, remove single quotes from query formula
                    query_mask = f"{column} == '{value}'"
                    try:
                        value = float(value)
                        query_mask = f"{column} == {value}"
                    except ValueError:
                        pass

                    # Adjust condition if not equal (!) is given
                    if isinstance(value, str) and value.startswith("!"):
                        value = value.replace("!", "")
                        # logger.info("Value is string: {}".format(value))
                        query_mask = f"{column} != '{value}'"
                    elif isinstance(value, str):
                        query_mask = f"{column} == '{value}'"

                    # Add "and" to eval formula if it is not the first condition
                    if query_formula is None:
                        query_formula = f"{query_mask}"
                    else:
                        query_formula += f" and {query_mask}"

                # Return result as tuple (query formula and eval formula)
                eval_formula.append([query_formula, sum_formula])

        case "SUMIFPOSITIVE":
            row_ids = list(map(int, formula.split("+")))
            eval_formula = [row_ids, column_index]

        case "EVAL":
            # Replace "row" with row index
            eval_formula = formula.replace("row", str(row_index))
            logger.info("Eval formula: {}".format(eval_formula))
        # Default
        case _:
            eval_formula = re.sub(
                r"\d+", f"df.iloc[{row_index}].values[\\g<0>]", formula
            )

    # Get priority level
    priority = get_priority_level(formula_type)
    # logger.info(
    #     "Formula type: {}, Eval: {}, Priority level: {}".format(
    #         formula_type, eval_formula, priority
    #     )
    # )

    return eval_formula, formula_type, priority


def get_priority_level(formula_type):
    """
    Get priority level of formula
    :param formula_type: formula type (str)
    :return: list of formula types (list) or priority level (int)
    """
    # Define priority levels for each formula type
    priority_levels = {
        "SUMRANGES": 0,
        "SUMIF": 1,
        "MAX": 2,
        "COPY": 2,
        "SUM_COLUMN": 2,
        "SUM_ROW": 3,
        "COMPARISION": 4,
        "SFORMULA": 5,
        "MFORMULA": 5,
        "FORMULA": 5,
        "SUMIFPOSITIVE": 5,
        "PRODUCTSUM": 6,
        "RATIO": 7,
        "SUM_COLUMN_RANGES": 8,
        "EVAL": 9,
    }

    if formula_type == "ALL":
        return list(priority_levels.keys())

    # Return priority level
    return priority_levels.get(formula_type, 0)


def sum_specified_rows(df, row_indexes):
    """
    Sum specified rows
    :param df: DataFrame
    :param row_indexes: list of touple (start index, end index)
    :return: DataFrame with updated values
    """
    for i, j in row_indexes:
        # Sum specified row values
        result = df.iloc[[i, j], 1:].sum().to_dict()
        # Update df with sum values by "i" index
        df.loc[i, result.keys()] = tuple(result.values())
        # Assign "0" to "j" index
        df.loc[j, result.keys()] = 0
    return df


def update_values_row_wise(df, output_df, start_row=1, output_start_row=1):
    """
    Update row values row by row
    :param df: DataFrame with update needed values
    :param output_df: DataFrame with actual values
    :param start_row: start row index (int)
    :return: DataFrame with updated values
    """
    percentage_variables = get_percentage_variables()
    df = df.copy().reset_index(drop=True)
    output_df = output_df.copy().reset_index(drop=True)

    for index, row in df.iloc[start_row:].iterrows():  # Skip first row (header)
        logger.info("Updating row values, index: {}".format(index))

        try:
            # Check if output_df has current index
            if index - start_row not in output_df.index:
                # Clear row values as required
                df.iloc[index, 1:] = ""
                continue

            # Get row values
            output_row = output_df.iloc[index - output_start_row]
            current_row_values = row.to_dict()
            output_row_values = output_row.to_dict()

            # Update row values by checking
            n1_value = None
            for key, value in current_row_values.items():
                # Check if value of template exists in output_df column names
                if value in output_row_values.keys():
                    result = output_row_values[value]
                    # Check if result is percentage value
                    if value in percentage_variables:
                        result = add_sign_and_round(result)

                    # Replace evaluated expressions with desired values (N/NN)
                    if value == "N1":  # N1 = N1
                        n1_value = "Y" if result else "N"
                        result = n1_value

                    if value == "N2":  # N2 = N1 + N2
                        n2_value = "Y" if result else "N"
                        result = n1_value + n2_value

                    if value == "N3":  # N3 = N1 == N3 (Y)
                        n3_value = "Y" if (result and n1_value == "Y") else "N"
                        result = n3_value

                    current_row_values[key] = result
                    logger.info("Updated value for {}: {}".format(value, result))

            # Assign updated row to df by index
            # logger.info("Current row values: {}".format(current_row_values))
            df.loc[index, current_row_values.keys()] = current_row_values.values()

        except Exception as e:
            logger.error(f"Error while updating {index} row values: {e}")
            df.iloc[index, 1:] = ""
            continue

    return df


def update_common_rows_at_once(df, output_df):
    """
    Update common rows at once
    :param df: DataFrame with update needed values
    :param output_df: DataFrame with actual values
    """
    # Iterate through 3 rows at once
    for i, j in enumerate(range(0, len(df), 3)):
        # logger.info("Updating row {}, iteration number {}".format(j, i))

        # Check if output_df has current index
        if i not in output_df.index:
            # Clear row values as required
            df.iloc[j : j + 3, 1:] = ""
            continue

        # Iterate through each row
        for index in range(j, j + 3):
            # Get row values
            output_row = output_df.iloc[i]
            row_values = df.iloc[index, 1:].to_dict()
            output_row_values = output_row.to_dict()

            # Update row values by checking
            for key, value in row_values.items():
                if value in output_row_values.keys():
                    result = output_row_values[value]
                    row_values[key] = result
                    # logger.info("New value for {}: {}".format(value, result))

            # Assign updated values to df
            df.loc[index, row_values.keys()] = row_values.values()

    return df


def get_percentage_variables():
    """
    Retrive percentage variables
    :return: list of percentage variables (list)
    """
    variables = [
        "한도",
        "적용세율",
        "SMRT",
        "Y3_AVG_TXRT",
        "ASFRS_SGRP_LMT_CLNM_AMT",
        "TPRP_LMT_CLNM",
        "PPPT_LMT_CLNM",
        "AVCPT_TTL_AMT_RQUAT_DCTAA_AMT",
    ]
    return variables


def replace_header_values(df, output_dict):
    """
    Replace header values
    :param df: DataFrame with update needed values
    :param output_dict: Dictionary with actual values
    :return: DataFrame with updated values
    """
    # Get header values
    headers = df.columns.to_list()
    replace_dict = dict()

    # Iterate through each column
    for header in headers:
        if isinstance(header, tuple):
            for column in header:
                # Check if column is in output_dict
                if column in output_dict.keys():
                    result = output_dict[column]
                    if isinstance(result, float) or result.isdigit():
                        result = "{:,.0f}".format(result)
                    replace_dict[column] = result
        else:
            # Check if column is in output_dict
            if header in output_dict.keys():
                result = output_dict[header]
                if isinstance(result, float) or result.isdigit():
                    result = "{:,.0f}".format(result)
                replace_dict[header] = result

    # logger.info("Replace dict: {}".format(replace_dict))

    # Replace column values
    df.rename(columns=replace_dict, inplace=True)

    return df


def calculate(value1, value2, operator):
    """
    Calculate values
    :param value1: First value
    :param value2: Second
    :param operator: Operator (str) (+, -, *, /, //)
    :return: Calculated value
    """
    logger.info("Calculating values: {} {} {}".format(value1, operator, value2))
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


def get_masked_variables():
    """
    Retrive masked variables
    :return: Dictionary with masked variables (dict)
    """
    variables_dict = {
        "F": "KICS_EXPI_MNCT",
        "I": "CRRK_SCLSF_NM",
        "M": "RDYN_AVGT_AMT",
        "L": "RDYN_AVCLT_AMT",
        "T": "CREP_AVCLT_CLN_AMT",
        "J": "AVGT_KICS_GRP",
        "H": "CRRK_MCLSF_NM",
        "U": "CREP_AVGT_CLN_AMT",
        "P": "APPT_LTV_VLU",
        "Q": "APPT_DSCR_",
        "E": "KICS_EXPI_MNCT",
        "G": "CREP_CRDT_REINS_RSLB_DDB_AMT",
        "D": "KICS_CRRT_NM",
        "F2": "CREP_CRDT_REINS_PMLB_DDB_AMT",
        "I1": "CREP_RIRDAM_CRRK_DDAF_AMT",
        "H1": "CREP_CRDT_RIIDAM_CRRK_DDB_AMT",
        "R": "Credit_Exposure_Clean",
        "R1": "Credit_Exposure_Clean_2",
        "J1": "CRRK_SDCLSF_NAM",
        "J_HANA": "KICS_QG_Credit_Risk_Classification",
        "R_HANA": "EXPS_CLEANDB_AMT",
        "U_HANA": "AVGT_EXPS_DIRTY_AMT",
    }
    return variables_dict


def calculate_ranks(df, column_names):
    """
    This function is used to calculate ranks based on the available values of two columns
    Equivalent of RANK.EQ excel function with additional checkings to match template equation
    """
    l_values = df[column_names[0]].values.tolist()
    r_values = df[column_names[1]].values.tolist()

    logger.info("Calculating ranks...")
    # Loop through each row
    for i, _ in df.iterrows():
        # Get current value
        l_value = l_values[i]
        r_value = r_values[i]

        # Calculate ranking based on the values, and assign it to the df
        df.loc[i, "RANK"] = validate_rank(l_values, r_values, l_value, r_value)
    logger.info("Ranks calculated successfully")

    # Remove unranked and duplicate rows
    result = df[df["RANK"] > 0]
    result.sort_values(by="RANK", ascending=False, inplace=True)

    # Reset index, and sort by RANK (desc)
    result.drop_duplicates(subset=["RANK"], keep="first", inplace=True)
    result.reset_index(drop=True, inplace=True)

    # Remove duplicates
    result.drop_duplicates(subset=["RANK"], keep="first", inplace=True)

    return result


def rank_eq(value, values, is_ascending=False):
    """
    Get rank position of a value in a list
    """
    return values.index(value) + 1


def validate_rank(l_values, r_values, l_value, r_value):
    """
    Equivalent of RANK.EQ excel function with additional checkings to match template equation
    """
    result = 0

    try:
        # Check the first condition
        if sum(l_values) == 0:
            if int(r_value) != 0:
                result = rank_eq(r_value, r_values, 0)
                logger.info("Result for {}: {}".format(r_value, result))
        else:
            if int(l_value) != 0:
                result = rank_eq(l_value, l_values, 0)
                logger.info("Result for {}: {}".format(l_value, result))
    except Exception as e:
        logger.error("Error: {}".format(e))

    return result


def format_year_value(value):
    """
    This function helps to generate year value as desired for KICS QIS template
    :param value: value to format (str, int, float - number)
    :return: formated value (str) (e.g. "10-11년)
    """
    formated_values = {
        "0": "0-1년",
        "1": "1-2년",
        "2": "2-3년",
        "3": "3-4년",
        "4": "4-5년",
        "5": "5-6년",
        "6": "6-7년",
        "7": "7-8년",
        "8": "8-9년",
        "9": "9-10년",
        "10": "10-11년",
        "11": "11-12년",
        "12": "12-13년",
        "13": "13-14년",
        "14": "14년 +",
    }
    value = str(int(value))
    result = formated_values.get(value, "")
    # logger.info("Result for {}: {}".format(value, result))

    return result


def get_db_connection(wvr_path, model_name):
    """
    Get database connection (initalize connection for boost further processing)
    :param wvr_path: WVR path (str)
    :param model_name: Model name (str)
    :return: Database connection (pyodbc connection object)
    """
    connection = None
    try:
        connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model_name)
        logger.info("Connect string: {}".format(connect_string))
        connection = wvr_functions.get_connection(connect_string)
    except Exception as e:
        logger.error(f"Error while establishing connection: {e}")
    return connection
