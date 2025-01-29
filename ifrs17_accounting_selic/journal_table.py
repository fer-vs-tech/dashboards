from unittest import result
import cm_dashboards.ifrs17_accounting_selic.db_helper as db_helper
import cm_dashboards.ifrs17_accounting_selic.helpers as helpers


def get_data(wvr_path, url_path, journal_type):
    """
    Get tables from wvr
    """
    # Initialize DB instance
    table_name = helpers.get_table_name_by_journal_type(journal_type)
    journal_tables = db_helper.Journals(table_name=table_name)

    # Get data from wvr, unpack data (data, columns, conditional_style)
    journal_tables_df = helpers.get_df(journal_tables, wvr_path)

    journal_tables_df.loc[-1] = ["ALL"]  # adding a row
    journal_tables_df.index = journal_tables_df.index + 1  # shifting index
    journal_tables_df = journal_tables_df.sort_index()  # sorting by index

    # Add Download URL and View URL
    journal_tables_df["Journal"] = journal_tables_df.apply(
        lambda x: helpers.set_link(x, url_path, journal_type, "View"), axis=1
    )
    journal_tables_df["Download"] = journal_tables_df.apply(
        lambda x: helpers.set_link(x, url_path, journal_type, "Download"), axis=1
    )

    return journal_tables_df


def get_table_data(wvr_path, url_path, journal_type):
    """
    Get table data from df
    """
    # In case of failure, return None
    result = [None, None, None]
    try:
        df = get_data(wvr_path, url_path, journal_type)
        result = helpers.prepare_table_data(df)
        return result
    except Exception as e:
        print(e)
    return result
