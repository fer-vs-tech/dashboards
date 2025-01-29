import pandas as pd
import plotly.express as px
from sqlalchemy import column
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
import cm_dashboards.nonlife_standalone.dash_utils as dash_utils
import cm_dashboards.ifrs17_accounting.db_helper as db_helper
import cm_dashboards.ifrs17_accounting.helpers as helpers


def get_tables(wvr_path):
    """
    Get tables from wvr
    """
    # Initialize DB instance
    schema_handler = db_helper.AccountingModelSchema()
    journal_if = db_helper.JournalIF(limit=5)
    journal_nb = db_helper.JournalNB(limit=5)
    mapping_act_cf = db_helper.MappingActCF()
    mapping_exp_cfif = db_helper.MappingExpCFIF()

    # Get data from wvr (data, columns, conditional_style)
    journal_schema_df = helpers.get_df(schema_handler, wvr_path)
    journal_schema_data = helpers.prepare_table_data(journal_schema_df)

    mapping_schema_df = helpers.get_df(schema_handler, wvr_path, "mapping")
    mapping_schema_data = helpers.prepare_table_data(mapping_schema_df)

    journal_if_df = helpers.get_df(journal_if, wvr_path)
    journal_if_data = helpers.prepare_table_data(journal_if_df)

    journal_nb_df = helpers.get_df(journal_nb, wvr_path)
    journal_nb_data = helpers.prepare_table_data(journal_nb_df)

    mapping_act_cf_df = helpers.get_df(mapping_act_cf, wvr_path, "mapping")
    mapping_act_cf_data = helpers.prepare_table_data(mapping_act_cf_df)

    mapping_exp_cfif_df = helpers.get_df(mapping_exp_cfif, wvr_path, "mapping")
    mapping_exp_cfif_data = helpers.prepare_table_data(mapping_exp_cfif_df)

    return (
        *mapping_schema_data,
        *journal_schema_data,
        *journal_if_data,
        *journal_nb_data,
        *mapping_act_cf_data,
        *mapping_exp_cfif_data,
    )
