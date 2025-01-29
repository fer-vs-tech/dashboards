from cm_dashboards.ifrs17_disclosure import abstract_handler as gf
from cm_dashboards.ifrs17_disclosure import helpers as helpers

"""
['A_BBA_Primary', 'G_BBA_Primary', 'I_BBA_Primary',
'R_Info_RuntimeParameters', 'Rc_RuntimeParameters',
'Rd_RuntimeParameters', 'Rn_RuntimeParameters', 'T_Table_Mapping']

['A_BBA_OUT_Reinsurance', 'G_BBA_OUT_Reinsurance',
'I_BBA_OUT_Reinsurance', 'R_Info_RuntimeParameters',
'Rc_RuntimeParameters', 'Rd_RuntimeParameters', 'Rn_RuntimeParameters',
'T_Table_Mapping']
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


class JournalNames(gf.GenericHandler):
    """
    Grouped Journals with PTFLO
    """

    _DB_TABLE = "I_BBA_Primary"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}] LIMIT 5"

    def __init__(self, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = f"SELECT DISTINCT(PTFLO) FROM [{self._DB_TABLE}] WHERE PTFLO != '' AND PTFLO != 'Null'"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class Journal(gf.GenericHandler):
    """
    Individual Journal selected by PTFLO
    """

    _DB_TABLE = "G_BBA_Primary"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}] LIMIT 5"

    def __init__(self, table_name, ptflo):
        self._DB_TABLE = table_name
        if ptflo == "ALL":
            self._DB_QUERY = f"SELECT * FROM [{self._DB_TABLE}] WHERE PTFLO != '' AND PTFLO != 'Null'"
        else:
            self._DB_QUERY = f"SELECT * FROM [{self._DB_TABLE}] WHERE PTFLO = '{ptflo}'"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df
