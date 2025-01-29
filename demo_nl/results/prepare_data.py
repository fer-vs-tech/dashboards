import logging

logger = logging.getLogger(__name__)
import pandas as pd

replace_zero: str = None

import cm_dashboards.demo_nl.utils.db_helper as db_helper
import cm_dashboards.demo_nl.utils.helpers as helpers
from cm_dashboards.demo_nl.config.config import cache, timeout
from cm_dashboards.demo_nl.results.program_names import ProgramNames

@cache.memoize(timeout=timeout)
def get_report_dates(wvr_path, model_name, program):
    comp_db = db_helper.nl_Dates(program)
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    return comp_result

@cache.memoize(timeout=timeout)
def get_programs(wvr_path, model_name):
    comp_db = db_helper.nl_Programs()
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    return comp_result

@cache.memoize(timeout=timeout)
def get_portfolios(wvr_path, model_name, program):
    comp_db = db_helper.nl_Portfolios(program)
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    return comp_result

@cache.memoize(timeout=timeout)
def get_triangleSize(wvr_path, model_name, program):
    comp_db = db_helper.nl_TriangleSize(program)
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    return comp_result

@cache.memoize(timeout=timeout)
def get_triangleData(wvr_path, model_name, program, portfolio, method, var, rep_date, dev_value, orig_value):
    comp_db = db_helper.nl_ClaimData(program, portfolio, method, var, rep_date, dev_value, orig_value)
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    comp_result = comp_result.replace({0: replace_zero})
    return comp_result

@cache.memoize(timeout=timeout)
def get_ATA_Post_Stats_Data(wvr_path, model_name, program, portfolio, method, rep_date, dev_value, orig_value):
    comp_db = db_helper.nl_ATA_Post_Stats(program, portfolio, method, rep_date, dev_value, orig_value)
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    comp_result = comp_result.replace({0: replace_zero})
    return comp_result

@cache.memoize(timeout=timeout)
def get_ATA_Pre_Stats_Data(wvr_path, model_name, program, portfolio, method, rep_date, dev_value, orig_value):
    comp_db = db_helper.nl_ATA_Pre_Stats(program, portfolio, method, rep_date, dev_value, orig_value)
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    comp_result = comp_result.replace({0: replace_zero})
    return comp_result

@cache.memoize(timeout=timeout)
def get_ATA_Pre_LinkRatios_Data(wvr_path, model_name, program, portfolio, method, rep_date, dev_value, orig_value):
    comp_db = db_helper.nl_ATA_Pre_Link_Ratios(program, portfolio, method, rep_date, dev_value, orig_value)
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    comp_result = comp_result.replace({0: replace_zero})
    return comp_result

@cache.memoize(timeout=timeout)
def get_ATA_Post_LinkRatios_Data(wvr_path, model_name, program, portfolio, method, rep_date, dev_value, orig_value):
    comp_db = db_helper.nl_ATA_Post_Link_Ratios(program, portfolio, method, rep_date, dev_value, orig_value)
    comp_result = helpers.get_df(comp_db, wvr_path, model_name)
    comp_result = comp_result.replace({0: replace_zero})
    return comp_result
