from cm_dashboards.subledger import abstract_handler as gf


class FapHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "fap_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df["mr_initial_biz_loss"] = (
            df.Initial_Loss_BEL_FMP_Proc * df.Initial_Loss_RA_FMP_Proc
        )
        df["mr_csm_new_biz"] = df.Initial_CSM_FMP_Proc
        return df
