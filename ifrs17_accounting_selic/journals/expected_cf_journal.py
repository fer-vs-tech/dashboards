import cm_dashboards.ifrs17_accounting_selic.db_helper as db_helper
import cm_dashboards.ifrs17_accounting_selic.helpers as helpers


def get_data(wvr_path, company_id, journal_type):
    """
    Get tables from wvr
    """
    # Initialize DB instance
    if company_id == "ALL":
        table_name = helpers.get_table_name_by_journal_type(
            journal_type, journal="aggregated"
        )
        journal_db = db_helper.AggregatedJournal(table_name=table_name)
    else:
        table_name = helpers.get_table_name_by_journal_type(journal_type)
        journal_db = db_helper.Journal(table_name=table_name).add_where_clause(
            f"WHERE GOC = '{company_id}'"
        )

    mapping_db = db_helper.ExpectedCFMapping(journal_type=journal_type)

    # Get df from wvr
    journal_df = helpers.get_df(journal_db, wvr_path)

    # Raise error if no data is found
    if journal_df.shape[0] == 0:
        raise Exception(
            f"No data found for {journal_type} journal with company_id {company_id}"
        )

    # Add additional column from journal table
    mapping_df = helpers.get_df(mapping_db, wvr_path, "mapping")
    mapping_df["Posting_Key"] = "D"
    mapping_df["Total_Amount"] = mapping_df.apply(
        lambda x: helpers.set_value(journal_df, x["Journal_Variables"]), axis=1
    )
    mapping_df["GOC"] = mapping_df.apply(
        lambda _: helpers.set_value(journal_df, "GOC"), axis=1
    )
    mapping_df["PTFLO"] = mapping_df.apply(
        lambda _: helpers.set_value(journal_df, "PTFLO"), axis=1
    )
    mapping_df["COHT"] = mapping_df.apply(
        lambda _: helpers.set_value(journal_df, "COHT"), axis=1
    )
    mapping_df["PTFLO_2"] = mapping_df.apply(
        lambda _: helpers.set_value(journal_df, "PTFLO", apply_formatter=False), axis=1
    )

    return mapping_df


def get_table_data(wvr_path, company_id, journal_type="primary"):
    """
    Get table data from df
    """
    df = get_data(wvr_path, company_id, journal_type)

    # Get table data (data, columns, conditional_style)
    result = helpers.prepare_table_data(
        df,
        hidden_columns=["Posting_Key", "NB_IF", "GOC", "PTFLO", "COHT"],
    )

    return result
