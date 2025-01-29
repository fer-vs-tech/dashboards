import logging

logger = logging.getLogger(__name__)

import cm_dashboards.ifrs17_accounting.db_helper as db_helper
import cm_dashboards.ifrs17_accounting.helpers as helpers
import cm_dashboards.utilities as utils


def get_schema(wvr_path):
    """
    Get schema from wvr
    """
    schema = db_helper.AccountingModelSchema()
    schema_df = helpers.get_df(schema, wvr_path)
    results = helpers.prepare_table_data(schema_df)
    return results


def get_data(wvr_path, url_path, journal_type, add_headnote=False, reversed=False):
    """
    Get tables from wvr
    """
    # Initialize DB instance
    journal_tables = db_helper.UnionJournals(journal_type)
    journal_tables_df = helpers.get_df(journal_tables, wvr_path)
    suffix_mappings = {
        "primary": {True: "REVDIR", False: "DIR"},
        "reinsurance": {True: "REVRE", False: "RE"},
    }
    suffix = suffix_mappings.get(journal_type, {}).get(reversed, "")

    # Add needed columns
    if add_headnote:
        journal_tables_df["Record_Type_Text"] = "YR" if reversed else "YQ"
        # Rewrite Document_Header_Text to include suffix
        journal_tables_df["Document_Header_Text"] = journal_tables_df[
            "Document_Header_Text"
        ].apply(lambda x: f"{x}-{suffix}")
    else:
        # Add new row for summary
        journal_tables_df.loc[-1] = ["ALL", "IF", "", "", ""]
        journal_tables_df.index = journal_tables_df.index + 1
        journal_tables_df = journal_tables_df.sort_index()

        # Add links to be used in the homepage
        encoded_path = utils.encode_and_decode_string(wvr_path)
        journal_tables_df["Journal"] = journal_tables_df.apply(
            lambda x: helpers.set_link(x, encoded_path, url_path, journal_type, "View"),
            axis=1,
        )
        journal_tables_df["Download"] = journal_tables_df.apply(
            lambda x: helpers.set_link(
                x, encoded_path, url_path, journal_type, "Download"
            ),
            axis=1,
        )

    return journal_tables_df


def get_table_data(wvr_path, url_path, journal_type):
    """
    Get table data from df
    """
    df = get_data(wvr_path, url_path, journal_type)
    result = helpers.prepare_table_data(df)

    return result


def get_single_journal(wvr_path, journal_type, company_id, add_headnote=False):
    """
    Get a single journal for creating single report data per journal
    :param wvr_path: path to WVR file
    :return result: DF with single journal
    """
    # Initialize DB instance
    try:
        journal_table = db_helper.SingleJournal(journal_type, company_id)
        result = helpers.get_df(journal_table, wvr_path)
        # Add needed columns
        if add_headnote:
            result["Record_Type_Text"] = "YQ"

    except Exception as e:
        logger.error(f"Failing to get single journal: {e}")
        result = None

    return result
