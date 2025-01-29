from cm_dashboards.reinsurance import abstract_handler as gf


class RwaHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "rwa_template.csv"

    DB_QUERY = (
        "select A00_Treaty as COA, * from FMP_WAP.I_Reins_RWA f "
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
        df["CSM_REINS_Suspense_account_value"] = df.Initial_CSM_REINS_RWA_Proc

        return df
