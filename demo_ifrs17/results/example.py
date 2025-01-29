#ifrs17/results/example.py

from cm_dashboards.demo_ifrs17.config.config import cache, timeout
import cm_dashboards.demo_ifrs17.utils.db_helper as db_helper
import cm_dashboards.demo_ifrs17.utils.helpers as helpers
import cm_dashboards.demo_ifrs17.results.prepare_results as prepare_results
import cm_dashboards.demo_ifrs17.results.prepare_components as prepare_components
import logging

logger = logging.getLogger(__name__)

@cache.memoize(timeout=timeout)
def get_charts (wvr_files, step_date, w, h, type):
    if wvr_files is None or step_date is None:
        return None
    data = prepare_results.get_icl_by_model(wvr_files, step_date)
    values, names = ("Model_Value", "Total_Ins")
    color_discrete_map = ['royalblue', 'cyan', 'darkblue', 'gray', 'orange']

    chart = prepare_components.create_pie_chart(
        df = data,
        values=values,
        names=names,
        color_schema=color_discrete_map,
        size_width = w,
        size_height = h,
    )

    return chart
