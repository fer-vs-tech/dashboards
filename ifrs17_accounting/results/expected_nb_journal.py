import cm_dashboards.ifrs17_accounting.db_helper as db_helper
import cm_dashboards.ifrs17_accounting.helpers as helpers


def get_data(
    company_id,
    journal_type,
    reversed=False,
    wvr_path=None,
    journal_connection=None,
    mapping_connection=None,
):
    """
    Get tables from wvr
    """
    # Initialize DB instance
    journal = "JournalNB"
    if company_id == "ALL":
        journal_db = db_helper.AggJournalDB(journal, journal_type)
    else:
        journal_db = db_helper.JournalDB(journal, journal_type, company_id)

    mapping_db = db_helper.ExpectedCFJournalNB(journal_type=journal_type)

    # Get df from wvr
    if wvr_path is not None:
        journal_df = helpers.get_df(journal_db, wvr_path)
        mapping_df = helpers.get_df(mapping_db, wvr_path, "mapping")
        filter_zeros = False
    else:
        journal_df = helpers.get_dataframe(journal_db, journal_connection)
        mapping_df = helpers.get_dataframe(mapping_db, mapping_connection)
        filter_zeros = True

    mapping_df = helpers.populate_journal_data(
        mapping_df,
        company_id,
        journal_df,
        reverse=reversed,
        filter_zeros=filter_zeros,
    )

    return mapping_df


def get_table_data(wvr_path, company_id, journal_type="primary", reversed=False):
    """
    Get table data from df
    """
    df = get_data(company_id, journal_type, reversed=reversed, wvr_path=wvr_path)

    # Get table data (data, columns, conditional_style)
    result = helpers.prepare_table_data(
        df,
        hidden_columns=[
            "Posting_Key",
            "GOC",
            "PTFLO",
            "COHT",
            "Profit_Center_Code",
        ],
    )

    return result
