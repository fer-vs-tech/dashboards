import enum
import io
import logging

import pandas as pd

import cm_dashboards.china_subledger.utils.db_helper as db_helper
import cm_dashboards.china_subledger.utils.helpers as helpers
from cm_dashboards.utilities import timeit

logger = logging.getLogger(__name__)


@timeit()
def populate_results(
    wvr_path: str,
    previous_reporting_date: str,
    reporting_date: str,
) -> dict[str, str]:
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param opening_date: opening date
    :param reporting_date: reporting date
    :param group_id: group id
    :return: tuple (data, columns, conditional_style)
    """
    db_query = db_helper.PortfolioData(previous_reporting_date, reporting_date)
    data = helpers.get_df(db_query, wvr_path)
    data.rename(
        columns={
            "Step Date": "Report_Date",
            "IFRS_17 Call Date": "Call_Date",
            "Model_Value_Text": "Model",
            "PortfolioID": "Portfolio",
            "Subledger_R3S_Variable_Table": "Subledger_Variable_Table",
        },
        inplace=True,
    )
    data.drop(
        columns=[
            "Group_ID Value",
            "Group_Identifier",
        ],
        inplace=True,
    )
    data.fillna(0, inplace=True)
    data = data.to_dict()
    return data


class RecordType(enum.Enum):
    """
    Data transformation indicators
    """

    VARIABLE_MAPPING = 1
    EVENT_MAPPING = 2


def generate_dashboard_data(
    variable_mappings: pd.DataFrame,
    event_mappings: pd.DataFrame,
    model_output: pd.DataFrame,
    previous_report_date: str,
    report_date: str,
    for_export=False,
) -> dict[str, dict[str, pd.DataFrame]]:
    """
    Generate dashboard data based on the results dictionary and dashboard id
    """

    def transform_row_values(row: pd.Series, record_type: RecordType) -> pd.Series:
        """
        Transform row values based on the record type
        """
        try:
            match record_type:
                case RecordType.VARIABLE_MAPPING:
                    needed_result = previous_results if row.Date_Index == 0 else current_results
                    date = needed_result["Report_Date"].iloc[0]
                    if row.R3S_Variable in [0, "0", ""]:
                        # logger.info(
                        #     f"Invalid variable found, setting up zero value and skipping"
                        # )
                        return [date, 0]
                    if row.R3S_Variable not in needed_result.columns:
                        logger.error(f"Variable '{row.R3S_Variable}' is missing in model output, setting up zero value")
                        return [date, 0]
                    output_value = needed_result[row.R3S_Variable].iloc[0]
                    if "-" in row.Sign:
                        output_value = output_value * -1
                    result = [date, output_value]

                case RecordType.EVENT_MAPPING:
                    matched_row = variable_mappings[variable_mappings["报表项 (CoA)"] == row.CoA]
                    if matched_row.empty:
                        if not for_export:
                            results["missing_mappings"].append(row.CoA)
                            logger.error(f"Subledger event mapping key '{row.CoA}' not in variable mappings")
                        return row

                    matched_row = matched_row.to_dict("records")[0]
                    sum_value = matched_row.get("金额 (Value)", 0)
                    debt_credit_indicator = row.Debit_Credit

                    if debt_credit_indicator.startswith("C"):
                        sum_value = sum_value * -1
                    row.Value = sum_value
                    mapped_event_id = row.Events_ID

                    if "/" in mapped_event_id:
                        split_event_id = mapped_event_id.split("/")
                        if future_service_csm_value != 0:
                            mapped_event_id = split_event_id[0]
                        else:
                            mapped_event_id = split_event_id[1]

                    row.Accounting_event = mapped_event_id
                    account_event_code = mapped_event_id.split("-")[0]
                    row.Accounting_Event_Code = account_event_code
                    subject_id = row.Accounting_ID.split("-")[0]
                    row.Subject = subject_id
                    result = row
            return result
        except Exception as e:
            logger.error(f"Error transforming row values, setting to default: {e}")
            return row

    dashboards = helpers.dashboards_list()
    results = {"validation_table": {}, "missing_mappings": []}
    results.update({dash_id: {"mapping_data": pd.DataFrame(), "table_data": pd.DataFrame()} for dash_id in dashboards.keys()})
    variable_mappings["Value"] = variable_mappings["R3S_Variable"]
    previous_results = model_output[model_output["Report_Date"] == previous_report_date]
    current_results = model_output[model_output["Report_Date"] == report_date]
    for dash_id in dashboards.keys():
        prepared_data = {}
        try:
            match dash_id:
                case "variable_mapping":
                    variable_mappings[["Date_Index", "Value"]] = variable_mappings[["Date_Index", "R3S_Variable", "Sign"]].apply(
                        lambda x: transform_row_values(x, RecordType.VARIABLE_MAPPING),
                        axis=1,
                        result_type="expand",
                    )
                    variable_mappings.drop(columns=["Sign"], inplace=True)
                    variable_mappings.rename(
                        columns={
                            "CoA": "报表项 (CoA)",
                            "Date_Index": "日期 (Date)",
                            "R3S_Variable": "变量 (Variable)",
                            "Value": "金额 (Value)",
                        },
                        inplace=True,
                    )
                    prepared_data["mapping_data"] = variable_mappings
                    if not for_export:
                        prepared_table_data = helpers.prepare_table_data(
                            variable_mappings,
                        )
                        prepared_data["table_data"] = prepared_table_data

                case "event_mapping":
                    common_values = current_results if not current_results.empty else previous_results
                    common_values = common_values.to_dict("records")[0]
                    future_service_csm_value = int(common_values.get("Experience_Adj_Future_Service_CSM", 0))
                    default_value = "NOT FOUND"
                    new_event_mappings = {
                        "Value": 0,
                        "Subject": default_value,
                        "Accounting_event": default_value,
                        "Accounting_Event_Code": default_value,
                        "Model": common_values.get("Model", default_value),
                        "Group": common_values.get("Group_ID", default_value),
                        "Portfolio": common_values.get("Portfolio", default_value),
                    }
                    event_mappings = event_mappings.assign(**new_event_mappings)
                    event_mappings = event_mappings.apply(
                        lambda x: transform_row_values(x, RecordType.EVENT_MAPPING),
                        axis=1,
                    )
                    event_mappings["Value_2"] = event_mappings["Value"]
                    event_mappings = event_mappings[
                        [
                            "CoA",
                            "Accounting_ID",
                            "Events_ID",
                            "Value",
                            "Debit_Credit",
                            "Account_Category",
                            "Accounting_event",
                            "Ledger",
                            "Subject",
                            "Portfolio",
                            "Group",
                            "Model",
                            "Accounting_Event_Code",
                            "Value_2",
                        ]
                    ]
                    event_mappings.rename(
                        columns={
                            "CoA": "报表项 (CoA)",
                            "Accounting_ID": "科目 (Accounting_ID)",
                            "Events_ID": "变动原因 (Events_ID)",
                            "Value": "金额 (Value)",
                            "Debit_Credit": "借贷序号 (Debit_Credit)",
                            "Account_Category": "科目大类 (Account_Category)",
                            "Accounting_event": "变动原因-2 (Accounting event-2)",
                            "Ledger": "帐务别 (Ledger)",
                            "Subject": "科目 (Subject)",
                            "Portfolio": "合同组合 (Portfolio)",
                            "Group": "合同组 (Group)",
                            "Model": "模型 (Model)",
                            "Accounting_Event_Code": "变动原因 (Accounting Event Code)",
                            "Value_2": "金额 (Value 2)",
                        },
                        inplace=True,
                    )

                    prepared_data["mapping_data"] = event_mappings
                    if not for_export:
                        prepared_table_data = helpers.prepare_table_data(
                            event_mappings,
                        )
                        prepared_data["table_data"] = prepared_table_data

                case "validation_subledger":
                    if event_mappings.empty:
                        raise ValueError("Event mapping table is missing")

                    # Calculate the total value for that group and store it for subledger-level validation
                    group_id = event_mappings["合同组 (Group)"].unique().tolist()[0]
                    total_value = event_mappings["金额 (Value 2)"].sum(numeric_only=True).astype(int)
                    checked_validation = {
                        "合同组 (GroupID)": group_id,
                        "汇总额 (Total)": total_value,
                        "借贷科目是否配平 (Balance)": total_value == 0,
                    }
                    results["validation_table"] = checked_validation

                    grouped_data = event_mappings.groupby(["科目 (Subject)", "科目 (Accounting_ID)"])
                    grouped_data = grouped_data["金额 (Value)"].sum()
                    prepared_df = grouped_data.reset_index()
                    prepared_df["科目 (Accounting_ID)"] = prepared_df["科目 (Accounting_ID)"].apply(lambda x: "-".join(x.split("-")[1:]))
                    prepared_df.rename(
                        columns={
                            "科目 (Subject)": "科目 (Accounting_ID)",
                            "科目 (Accounting_ID)": "科目描述 (Description)",
                        },
                        inplace=True,
                    )

                    prepared_data["mapping_data"] = prepared_df
                    if not for_export:
                        prepared_table_data = helpers.prepare_table_data(
                            prepared_df,
                        )
                        prepared_data["table_data"] = prepared_table_data

            results[dash_id] = prepared_data

        except Exception as e:
            if not for_export:
                logger.error(f"Error generating {dash_id} dashboard: {e}")
            continue

    if for_export:
        del results["variable_mapping"]
    return results


def get_mapping_tables(assumptions: dict, model_results: pd.DataFrame):
    """
    Get mapping tables
    """
    variable_mappings = []
    event_mappings = []
    try:
        variable_mapper_name = model_results["Subledger_Variable_Table"].iloc[0]
        if not variable_mapper_name:
            raise ValueError(f"Subledger variable table is missing: {variable_mapper_name}")

        variable_mappings = assumptions.get(variable_mapper_name, [])
        if not variable_mappings:
            raise ValueError(f"Could not find the subledger variable '{variable_mapper_name}' table in assumptions")

        event_mapper_name = model_results["Subledger_Table"].iloc[0]
        if not event_mapper_name:
            raise ValueError(f"Subledger event table is missing: {event_mapper_name}")

        event_mappings = assumptions.get(event_mapper_name, [])
        if not event_mappings:
            raise ValueError(f"Could not find the subledger event '{event_mapper_name}' table in assumptions")
        logger.info(f"Variable mapping table: {variable_mapper_name}")
        logger.info(f"Subledger mapping table: {event_mapper_name}")
        variable_mappings = variable_mappings[1:]
        event_mappings = event_mappings[1:]
    except Exception as error:
        logger.error(error)

    variable_mappings = pd.DataFrame.from_records(variable_mappings)
    event_mappings = pd.DataFrame.from_records(event_mappings)
    return variable_mappings, event_mappings


@timeit()
def generate_export_file(
    model_results: pd.DataFrame,
    assumptions: dict,
    previous_report_date: str,
    report_date: str,
):
    """
    Generate data for export file
    """
    group_ids = model_results["Group_ID"].unique()
    logger.info(f"Total groups to proceed: {len(group_ids)}")

    def process_group(group_id):
        result = None
        try:
            group_results = model_results[model_results["Group_ID"] == group_id]
            if group_results.empty:
                raise ValueError("No data found in model output")
            variable_mappings, event_mappings = get_mapping_tables(assumptions, group_results)
            if variable_mappings.empty or event_mappings.empty:
                return result

            result = generate_dashboard_data(
                variable_mappings,
                event_mappings,
                group_results,
                previous_report_date,
                report_date,
                for_export=True,
            )
        except Exception as error:
            logger.info(f"Failed to generate group results for: '{group_id}': {error}")
        return result

    consolidated_results = []
    consolidated_validations = []
    for group_id in group_ids:
        result_dict = process_group(group_id)
        if result_dict is None:
            continue
        subledger_results = result_dict["event_mapping"]["mapping_data"]
        validation_results = result_dict["validation_table"]
        consolidated_results.append(subledger_results)
        consolidated_validations.append(validation_results)
        logger.info(f"Populated results for '{group_id}': {subledger_results.shape}")

    results_dataframe = pd.concat(consolidated_results, ignore_index=True)
    valiations_dataframe = pd.DataFrame.from_records(consolidated_validations)

    results_dataframe = results_dataframe.reset_index(drop=True)
    results_dataframe.insert(loc=0, column="模型", value=results_dataframe["模型 (Model)"])
    results_dataframe.insert(loc=1, column="Group", value=results_dataframe["合同组 (Group)"])
    results_dataframe.rename(
        columns={
            "报表项 (CoA)": "报表项",
            "科目 (Accounting_ID)": "科目",
            "变动原因 (Events_ID)": "变动原因",
            "金额 (Value)": "R3S金额",
            "借贷序号 (Debit_Credit)": "借贷序号",
            "科目大类 (Account_Category)": "科目大类",
            "变动原因-2 (Accounting event-2)": "变动原因-2",
            "帐务别 (Ledger)": "报表字段",
            "科目 (Subject)": "科目 (2)",
            "合同组合 (Portfolio)": "合同组合",
            "合同组 (Group)": "合同组",
            "模型 (Model)": "模型",
            "变动原因 (Accounting Event Code)": "变动原因 (2)",
            "金额 (Value 2)": "R3S金额 (2)",
        },
        inplace=True,
    )

    sheet_names = ["Subledger Results", "Validation Results"]
    dfs = [results_dataframe, valiations_dataframe]
    return write_multiple_dfs_into_one_file(dfs, sheet_names)


def write_multiple_dfs_into_one_file(dfs: list[pd.DataFrame], sheet_names: list[str]) -> bytes:
    """
    Merge multiple dataframes into one file (in-memery writing)
    """
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for df, sheet_name in zip(dfs, sheet_names):
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        output = output.getvalue()
    except Exception as error:
        output = None
        logger.info(f"Failed to write dataframes into one file: {error}")
    return output
