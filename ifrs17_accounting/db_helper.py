from cm_dashboards.ifrs17_accounting import abstract_handler as gf
from cm_dashboards.ifrs17_accounting import helpers as helpers

"""
['A_Accounting_Journal_IF', 'A_Accounting_Journal_NB', 'A_Reins_Accounting_Journal_IF',
'A_Reins_Accounting_Journal_NB', 'A_Reins_Transition_Journal', 'A_Transition_Journal',
'G_Accounting_Journal_IF', 'G_Accounting_Journal_NB', 'G_Reins_Accounting_Journal_IF',
'G_Reins_Accounting_Journal_NB', 'G_Reins_Transition_Journal',
'G_Transition_Journal', 'I_Accounting_Journal_IF', 'I_Accounting_Journal_NB',
'I_Reins_Accounting_Journal_IF', 'I_Reins_Accounting_Journal_NB', 'I_Reins_Transition_Journal',
'I_Transition_Journal', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters', 'Rd_RuntimeParameters',
'T_Table_Mapping', 'Z_Info_Model', 'Zc_Model', 'Zn_Model']
"""


class AccountingModelSchema(gf.GenericHandler):
    _DB_TABLE = "G_Accounting_Journal_IF"
    _DB_QUERY = "SELECT * FROM [{0}] WHERE GOC = 'GMI_2020_AVI_B'".format(_DB_TABLE)

    def __init__(self, table="G_Reins_Transition_Journal"):
        self._DB_QUERY = self._DB_QUERY.format(table)

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class JournalDB(gf.GenericHandler):
    """
    Generic handler for all journals in the database (IF, NB, Transition)
    """

    _JOURNALS = {
        "JournalIF": {
            "primary": "I_Accounting_Journal_IF",
            "reinsurance": "I_Reins_Accounting_Journal_IF",
        },
        "JournalNB": {
            "primary": "I_Accounting_Journal_NB",
            "reinsurance": "I_Reins_Accounting_Journal_NB",
        },
        "JournalTransition": {
            "primary": "I_Transition_Journal",
            "reinsurance": "I_Reins_Transition_Journal",
        },
    }

    _DB_QUERY = "SELECT * FROM [{table_name}] WHERE GOC = '{company_id}'"

    def __init__(self, journal_name, journal_type, company_id, limit=None):
        self._DB_TABLE = self._get_table_name(journal_name, journal_type)
        self._DB_QUERY = self._DB_QUERY.format(
            table_name=self._DB_TABLE, company_id=company_id
        )
        if limit is not None:
            self.set_limit(limit)

    def _get_table_name(self, journal_name, journal_type):
        return self._JOURNALS[journal_name][journal_type]

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class AggJournalDB(gf.GenericHandler):
    """
    Generic handler for all aggrigated journals in the database (IF, NB, Transition)
    """

    _JOURNALS = {
        "JournalIF": {
            "primary": "A_Accounting_Journal_IF",
            "reinsurance": "A_Reins_Accounting_Journal_IF",
        },
        "JournalNB": {
            "primary": "A_Accounting_Journal_NB",
            "reinsurance": "A_Reins_Accounting_Journal_NB",
        },
        "JournalTransition": {
            "primary": "A_Transition_Journal",
            "reinsurance": "A_Reins_Transition_Journal",
        },
    }

    _DB_QUERY = "SELECT * FROM [{table_name}] LIMIT 1"

    def __init__(self, journal_name, journal_type, limit=None):
        self._DB_TABLE = self._get_table_name(journal_name, journal_type)
        self._DB_QUERY = self._DB_QUERY.format(table_name=self._DB_TABLE)
        if limit is not None:
            self.set_limit(limit)

    def _get_table_name(self, journal_name, journal_type):
        return self._JOURNALS[journal_name][journal_type]

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class UnionJournals(gf.GenericHandler):
    """
    Generic handler to union all journals
    """

    _JOURNALS = {
        "primary": {
            "if": "I_Accounting_Journal_IF",
            "nb": "I_Accounting_Journal_NB",
        },
        "reinsurance": {
            "if": "I_Reins_Accounting_Journal_IF",
            "nb": "I_Reins_Accounting_Journal_NB",
        },
    }

    _DB_QUERY = """
        (SELECT GOC as GoC_Name, NB_IF, Document_Date, Posting_Date, Document_Header_Text FROM [{if_table}] WHERE GOC != '' AND GOC != 'Null' AND NB_IF != '')
        UNION
        (SELECT GOC as GoC_Name, NB_IF, Document_Date, Posting_Date, Document_Header_Text FROM [{nb_table}] WHERE GOC != '' AND GOC != 'Null' AND NB_IF != '')
        ORDER BY NB_IF ASC
        """

    def __init__(self, journal_type, limit=None):
        self._IF_TABLE = self._JOURNALS[journal_type]["if"]
        self._NB_TABLE = self._JOURNALS[journal_type]["nb"]
        self._DB_QUERY = self._DB_QUERY.format(
            if_table=self._IF_TABLE, nb_table=self._NB_TABLE
        )
        if limit is not None:
            self.set_limit(limit)

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class SingleJournal(gf.GenericHandler):
    """
    Generic handler to union journals for a single company
    """

    _JOURNALS = {
        "primary": {
            "if": "I_Accounting_Journal_IF",
            "nb": "I_Accounting_Journal_NB",
            "select": "GOC as GoC_Name, NB_IF, Document_Date, Posting_Date, Document_Header_Text, Profit_Center_Code",
        },
        "reinsurance": {
            "if": "I_Reins_Accounting_Journal_IF",
            "nb": "I_Reins_Accounting_Journal_NB",
            "select": "GOC as GoC_Name, NB_IF, Document_Date, Posting_Date, Document_Header_Text",
        },
    }

    _DB_QUERY = """
        (SELECT {select} FROM [{if_table}] WHERE GOC = '{company_id}' LIMIT 1)
        UNION
        (SELECT {select} FROM [{nb_table}] WHERE GOC = '{company_id}' LIMIT 1)
        """

    def __init__(self, journal_type, company_id):
        self._IF_TABLE = self._JOURNALS[journal_type]["if"]
        self._NB_TABLE = self._JOURNALS[journal_type]["nb"]
        self._SELECT = self._JOURNALS[journal_type]["select"]
        self._DB_QUERY = self._DB_QUERY.format(
            select=self._SELECT,
            if_table=self._IF_TABLE,
            nb_table=self._NB_TABLE,
            company_id=company_id,
        )

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class Mappings(gf.GenericHandler):
    """
    Generic handler for all accounting journals in the database (Actual, Expected IF, Expected NB, LIC, Transition)
    """

    _JOURNALS = {
        "ExpectedCFJournalInForce": {
            "primary": "I_Accounting_Mapping_ExpCF_IF",
            "reinsurance": "I_Reins_Accounting_Mapping_ExpCF_IF",
        },
        "ExpectedCFJournalNB": {
            "primary": "I_Accounting_Mapping_ExpCF_NB",
            "reinsurance": "I_Reins_Accounting_Mapping_ExpCF_NB",
        },
        "ActualCFJournal": {
            "primary": "I_Accounting_Mapping_ActCF",
            "reinsurance": "I_Reins_Accounting_Mapping_ActCF",
        },
        "LicCFJournal": {
            "primary": "I_Accounting_Mapping_LIC",
            "reinsurance": "I_Reins_Accounting_Mapping_AIC",
        },
        "TransitionJournal": {
            "primary": "I_Accounting_Mapping_Transit",
            "reinsurance": "I_Reins_Accounting_Mapping_Transit",
        },
    }

    _DB_QUERY = """
        SELECT
            COA, Record_Type, Account_Description, NB_IF, Journal_Variables, Aggregates
        FROM [{table_name}]
        WHERE
            NB_IF != ''
        ORDER BY COA ASC
        """

    def __init__(self, journal_type, journal_name):
        self._DB_TABLE = self._JOURNALS[journal_name][journal_type]
        self._DB_QUERY = self._DB_QUERY.format(table_name=self._DB_TABLE)

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class ExpectedCFJournalInForce(Mappings):
    def __init__(self, journal_type):
        super().__init__(journal_type, "ExpectedCFJournalInForce")


class ExpectedCFJournalNB(Mappings):
    def __init__(self, journal_type):
        super().__init__(journal_type, "ExpectedCFJournalNB")


class ActualCFJournal(Mappings):
    def __init__(self, journal_type):
        super().__init__(journal_type, "ActualCFJournal")


class LicCFJournal(Mappings):
    def __init__(self, journal_type):
        super().__init__(journal_type, "LicCFJournal")


class TransitionJournal(Mappings):
    def __init__(self, journal_type):
        super().__init__(journal_type, "TransitionJournal")


class GetMappingData(gf.GenericHandler):
    """
    Join all mapping tables and return a single table
    """

    _MAPPING_TABLES = {
        "primary": {
            "actual": "I_Accounting_Mapping_ActCF",
            "expected_if": "I_Accounting_Mapping_ExpCF_IF",
            "expected_nb": "I_Accounting_Mapping_ExpCF_NB",
            "lic": "I_Accounting_Mapping_LIC",
            "transition": "I_Accounting_Mapping_Transit",
        },
        "reinsurance": {
            "actual": "I_Reins_Accounting_Mapping_ActCF",
            "expected_if": "I_Reins_Accounting_Mapping_ExpCF_IF",
            "expected_nb": "I_Reins_Accounting_Mapping_ExpCF_NB",
            "lic": "I_Reins_Accounting_Mapping_AIC",
            "transition": "I_Reins_Accounting_Mapping_Transit",
        },
    }

    def __init__(self, journal_type, journal_name):
        self._DB_TABLE = self._MAPPING_TABLES[journal_type][journal_name]
        self._DB_QUERY = f"""
            SELECT COA, Record_Type, Account_Description, NB_IF, Journal_Variables, Aggregates FROM [{self._DB_TABLE}] WHERE NB_IF != ''
            """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class GetJournalData(gf.GenericHandler):
    """
    Merge all journals into a single table
    """

    _JOURNAL_TABLES = {
        "primary": {
            "if": "I_Accounting_Journal_IF",
            "nb": "I_Accounting_Journal_NB",
            "transition": "I_Transition_Journal",
        },
        "reinsurance": {
            "if": "I_Reins_Accounting_Journal_IF",
            "nb": "I_Reins_Accounting_Journal_NB",
            "transition": "I_Reins_Transition_Journal",
        },
    }

    def __init__(self, journal_type, journal_name):
        self._DB_TABLE = self._JOURNAL_TABLES[journal_type][journal_name]
        self._DB_QUERY = f"""
            (SELECT * FROM [{self._DB_TABLE}] WHERE GOC != '' AND GOC != 'Null' AND NB_IF != '')
            ORDER BY NB_IF ASC
            """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df
