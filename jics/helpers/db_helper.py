from cm_dashboards.jics.helpers import abstract_handler as gf
from cm_dashboards.jics.helpers import helpers as helpers

"""
['A_Balance_Sheet', 'A_ESR', 'A_MOCE', 'A_RC', 'A_RC_Market', 'R_Info_RuntimeParameters',
'Rc_RuntimeParameters', 'Rd_RuntimeParameters', 'Rn_RuntimeParameters', 'T_Table_Mapping',
'Z_Info_Balance_Sheet', 'Z_Info_DataProcess_ESR_Agg_Solo_CF_Excel', 'Z_Info_DataProcess_ESR_Agg_Solo_DB',
'Z_Info_ESR', 'Z_Info_MarketRisk_Base', 'Z_Info_Model', 'Z_Info_RC_Ops', 'Zc_DataProcess_ESR_Agg_Solo_CF_Excel',
'Zc_DataProcess_ESR_Agg_Solo_DB', 'Zc_MarketRisk_Base', 'Zc_Model', 'Zc_RC_Ops',
'Zn_Balance_Sheet', 'Zn_DataProcess_ESR_Agg_Solo_CF_Excel', 'Zn_DataProcess_ESR_Agg_Solo_DB', 'Zn_ESR', 'Zn_Model']
"""


class TableInfos(gf.GenericHandler):
    """
    Table mapping is a special case, as it is used to get the list of tables
    """

    _DB_TABLE = "T_Table_Mapping"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = f"SELECT * FROM [{self._DB_TABL}]"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class JournalReportDates(gf.GenericHandler):
    """
    Get the list of report dates for a given journal
    """

    _DB_TABLE = "A_ESR"
    _DB_QUERY = (
        f"SELECT [Step Date] as Report_Date FROM [{_DB_TABLE}] WHERE [Step Date] != ''"
    )

    def __init__(self, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = (
                f"SELECT [Step Date] as Report_Date FROM [{self._DB_TABLE}]"
            )

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class Journal(gf.GenericHandler):
    """
    Individual Journal Data by Report Date
    """

    _DB_TABLE = "A_ESR"
    _DB_QUERY = f"SELECT FROM [{_DB_TABLE}]"

    def __init__(self, table_name=None, report_date=None, select="*"):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = f"SELECT {select} FROM [{self._DB_TABLE}] WHERE [Step Date] = '{report_date}'"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df
