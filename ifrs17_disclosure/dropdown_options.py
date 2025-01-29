import cm_dashboards.ifrs17_disclosure.db_helper as db_helper
import cm_dashboards.ifrs17_disclosure.helpers as helpers
from cm_dashboards.ifrs17_disclosure.app_config import cache, timeout


@cache.memoize(timeout=timeout)
def get_data(wvr_path, journal_name):
    """
    Get table data from df
    """
    # Initialize DB instance
    table_name = helpers.get_table_name_by_journal_type(journal_name, journal="grouped")
    journals = db_helper.JournalNames(table_name=table_name)

    # Get data from wvr, unpack data (data, columns, conditional_style)
    df = helpers.get_df(journals, wvr_path, journal_name)
    result = helpers.prepare_dropdown_options(df)

    return result
