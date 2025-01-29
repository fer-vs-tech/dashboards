from cm_dashboards.other_accounting import abstract_handler as gf


class PaaSmHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "paa_sm_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_PAA"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df["BEL_Difference_Vol_Adj_SM_Proc_PAA"] = df.BEL_Difference_Vol_Adj_SM_Proc

        df["Amortization_Amount_DAC_SM_Proc_PAA"] = df.Amortization_Amount_DAC_SM_Proc

        df["Recognized_Ins_Revenue_SM_Proc_PAA"] = df.Recognized_Ins_Revenue_SM_Proc
        return df
