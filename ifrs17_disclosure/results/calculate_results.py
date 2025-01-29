import logging

logger = logging.getLogger(__name__)

import concurrent.futures as concurrent

import numpy as np

import cm_dashboards.ifrs17_disclosure.db_helper as db_helper
import cm_dashboards.ifrs17_disclosure.helpers as helpers
import cm_dashboards.ifrs17_disclosure.results.utilities as utilities
from cm_dashboards.ifrs17_disclosure.app_config import cache, timeout


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, company_id, journal_name, journal_type):
    """
    Get table data from df
    """

    def calculate_result(df, ptflo):
        logger.info(f"Calculating results: {ptflo}")
        current_result = utilities.get_result(df, journal_name, journal_type)
        return current_result

    # Initialize DB instance
    if company_id != "ALL":
        logger.info(f"Calculating results for: {company_id}")
        table_name = helpers.get_table_name_by_journal_type(journal_name, "grouped")
        journal_tables = db_helper.Journal(table_name=table_name, ptflo=company_id)
        df = helpers.get_df(journal_tables, wvr_path, journal_name)
        final_df = utilities.get_result(df, journal_name, journal_type)
    else:
        table_name = helpers.get_table_name_by_journal_type(journal_name, "grouped")
        journals = db_helper.Journal(table_name=table_name, ptflo=company_id)
        journals_df = helpers.get_df(journals, wvr_path, journal_name)

        # Exclude non-numeric columns
        numeric_cl = journals_df.select_dtypes(include=[np.number]).columns.tolist()
        journals_df = journals_df.groupby(["PTFLO"])[numeric_cl].sum()

        # Calculate results for each company and sum up the results
        final_df = None
        with concurrent.ThreadPoolExecutor() as executor:
            futures = dict()
            # Loop through each row and submit the task to the executor
            for index, row in journals_df.iterrows():
                df = journals_df.loc[[index]]
                futures[executor.submit(calculate_result, df, index)] = index

            for future in concurrent.as_completed(futures):
                current_result = future.result()
                if final_df is None:
                    final_df = current_result
                else:
                    # Avoid duplicated description values
                    current_result.iloc[:, :1] = ""
                    final_df = final_df + current_result

    # Convert it to records
    final_df = final_df.to_dict(orient="records")
    logger.info(f"Results calculated successfully: {company_id}")
    return final_df


def prepare_table_data(records, journal_name, journal_type):
    """
    Convert df to suitable format for dash table
    """
    # Convert records to df, apply formating, get header rows, and prepare table data
    df = helpers.convert_to_df(records)
    df = helpers.convert_to_decimal(df, use_int=True)
    header_rows = utilities.get_header_rows_id(journal_name, journal_type)
    result = helpers.prepare_table_data(df, header_rows)
    return result
