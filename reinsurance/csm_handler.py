from cm_dashboards.reinsurance import abstract_handler as gf


class CsmHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "csm_template.csv"

    DB_QUERY = (
        "select A00_Treaty as COA, * from FMP_WAP.I_Reins_CSM_AMOR f "
        + "inner join FMP_WAP.T_Runs r on f.ExecutionID = r.ExecutionID "
        + "where r.Job_Run = {0}"
    )

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df[
            "Recognition_CSM_Interest_Expense_REINS"
        ] = df.Interest_Expense_CSM_REINS_CSM_AMOR_Proc_Reins
        df[
            "Writing_Off_CSM_Suspense_Account_REINS"
        ] = df.Ending_CSM_REINS_CSM_AMOR_Proc_Reins
        df[
            "Amort_Amt_CSM_REINS_CSM_AMOR_Proc_Reins"
        ] = -df.Amort_Amt_CSM_REINS_CSM_AMOR_Proc_Reins
        df[
            "Recognition_CSM_Amortization_REINS"
        ] = df.Amort_Amt_CSM_REINS_CSM_AMOR_Proc_Reins

        return df
