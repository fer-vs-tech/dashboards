from cm_dashboards.other_accounting import abstract_handler as gf


class VfaCsmHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "vfa_csm_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_VFA"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df["Interest_Expense_CSM_CSM_AMOR_Proc"] = 0
        df[
            "Recognition_interest_expense_for_CSM"
        ] = df.Interest_Expense_CSM_CSM_AMOR_Proc
        df["Writing_off_CSM_suspense_account"] = df.Pre_Amortized_CSM_CSM_AMOR_Proc
        df["Recognition_amortized_CSM"] = df.Writing_off_CSM_suspense_account

        return df
