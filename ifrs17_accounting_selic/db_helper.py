from cm_dashboards.ifrs17_accounting_selic import abstract_handler as gf
from cm_dashboards.ifrs17_accounting_selic import helpers as helpers

"""
['A_Accounting_Journal_General_GMM', 'A_Accounting_Journal_General_PAA', 'A_Accounting_Journal_Life_GMM',
'A_Reins_Accounting_Journal_General_GMM', 'A_Reins_Accounting_Journal_General_PAA', 'A_Reins_Accounting_Journal_Life_GMM',
'G_Accounting_Journal_General_GMM', 'G_Accounting_Journal_General_PAA', 'G_Accounting_Journal_Life_GMM',
'G_Reins_Accounting_Journal_General_GMM', 'G_Reins_Accounting_Journal_General_PAA', 'G_Reins_Accounting_Journal_Life_GMM',
'I_Accounting_Journal_General_GMM', 'I_Accounting_Journal_General_PAA', 'I_Accounting_Journal_Life_GMM',
'I_Reins_Accounting_Journal_General_GMM', 'I_Reins_Accounting_Journal_General_PAA', 'I_Reins_Accounting_Journal_Life_GMM',
'R_Info_RuntimeParameters', 'Rc_RuntimeParameters', 'Rd_RuntimeParameters', 'T_Table_Mapping']
"""
class Journals(gf.GenericHandler):
    """
    Individual Journal with GOC only for Primary and Reinsurance (Life and General)
    """
    _DB_TABLE = "I_Accounting_Journal"
    _DB_QUERY = "SELECT GOC as GoC_Name [{0}]".format(_DB_TABLE)

    def __init__(self, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = "SELECT GOC as GoC_Name FROM [{0}]".format(self._DB_TABLE)

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df

class Journal(gf.GenericHandler):
    """
    Individual Journal for Primary and Reinsurance (Life and General)
    """
    _DB_TABLE = "I_Accounting_Journal"
    _DB_QUERY = "SELECT * [{0}]".format(_DB_TABLE)

    def __init__(self, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = "SELECT * FROM [{0}]".format(self._DB_TABLE)

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df

class AggregatedJournal(gf.GenericHandler):
    """
    Aggregated Journal for Primary and Reinsurance (Life and General)
    """
    _DB_TABLE = "A_Accounting_Journal"
    _DB_QUERY = "SELECT * [{0}]".format(_DB_TABLE)
    
    def __init__(self, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = "SELECT * FROM [{0}]".format(self._DB_TABLE)

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df

class ActualCFMapping(gf.GenericHandler):
    """
    Actual CF Mapping for Primary and Reinsurance (Life and General)
    """
    _DB_TABLE = "I_Accounting_Mapping_ActCF"
    _DB_QUERY = f"SELECT COA, Record_Type, Account_Description, Journal_Variables FROM [{_DB_TABLE}]"
    _JOURNALS = {
        "primary_life": "I_Accounting_Mapping_ActCF",
        "primary_general": "I_Accounting_Mapping_ActCF",
        "primary_general_paa": "I_Accounting_Mapping_PAA",
        "reinsurance_life": "I_Reins_Accounting_Mapping_ActCF",
        "reinsurance_general": "I_Reins_Accounting_Mapping_ActCF",
        "reinsurance_general_paa": "I_Reins_Accounting_Mapping_PAA"
    }

    def __init__(self, journal_type=None):
        if journal_type is not None:
            self._DB_TABLE = self._JOURNALS[journal_type]
            self._DB_QUERY = f"SELECT COA, Record_Type, Account_Description, Journal_Variables FROM [{self._DB_TABLE}]"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df

class ExpectedCFMapping(gf.GenericHandler):
    """
    Expected CF Mapping for Primary and Reinsurance (Life and General)
    """
    _DB_TABLE = "I_Accounting_Mapping_ExpCF"
    _DB_QUERY = f"SELECT COA, Record_Type, Account_Description, Journal_Variables FROM [{_DB_TABLE}]"
    _JOURNALS = {
        "primary_life": "I_Accounting_Mapping_ExpCF",
        "primary_general": "I_Accounting_Mapping_ExpCF",
        "primary_general_paa": "I_Accounting_Mapping_PAA",
        "reinsurance_life": "I_Reins_Accounting_Mapping_ExpCF",
        "reinsurance_general": "I_Reins_Accounting_Mapping_ExpCF",
        "reinsurance_general_paa": "I_Reins_Accounting_Mapping_PAA"
    }

    def __init__(self, journal_type=None):
        if journal_type is not None:
            self._DB_TABLE = self._JOURNALS[journal_type]
            self._DB_QUERY = f"SELECT COA, Record_Type, Account_Description, Journal_Variables FROM [{self._DB_TABLE}]"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df
