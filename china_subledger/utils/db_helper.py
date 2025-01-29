from cm_dashboards.china_subledger.utils import abstract_handler as gf
from cm_dashboards.china_subledger.utils import helpers as helpers

"""
['A_Portfolio', 'G_Portfolio', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters',
'Rd_RuntimeParameters', 'Rn_RuntimeParameters', 'T_Table_Mapping', 'Z_Info_LRC_Premium',
'Z_Info_Portfolio', 'Zi_LRC_Premium', 'Zi_Portfolio', 'Zn_LRC_Premium', 'Zn_Portfolio']
"""


class TableInfos(gf.GenericHandler):
    """
    Table mapping is a special case, as it is used to get the list of tables
    """

    _DB_TABLE = "T_Table_Mapping"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"


class ControllersData(gf.GenericHandler):
    """
    Retrieve data for the controllers (dropdowns)
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = None

    def __init__(self):
        self._DB_QUERY = f"""
            SELECT
                [Step Date] as Report_Date,
                [IFRS_17 Call Date] as Call_Date,
                [Model_Value_Text] as Model,
                [PortfolioID] as Portfolio,
                Subledger_Table,
                Group_ID
            FROM [{self._DB_TABLE}]
            ORDER BY Group_ID DESC
            """


class PortfolioData(gf.GenericHandler):
    """
    Retrieve portfolio data by group ID
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = None

    def __init__(self, previous_report_date, report_date):
        self._DB_QUERY = f"""
            SELECT
                *
            FROM [{self._DB_TABLE}]
            WHERE [Step Date] = '{previous_report_date}' OR [Step Date] = '{report_date}'
            """
