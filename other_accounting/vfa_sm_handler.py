from cm_dashboards.other_accounting import abstract_handler as gf


class VfaSmHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "vfa_sm_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_VFA"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df["Insurance_Revenue_New_Biz_VFA"] = df.Change_in_RA_SM_Proc
        df[
            "Change_in_FCF_Death_Claim_SM_Proc_VFA"
        ] = df.Change_in_FCF_Death_Claim_SM_Proc
        df["Amortized_CSM_CSM_AMOR_Proc"] = 300
        df["Amortized_CSM_CSM_AMOR_Proc_VFA"] = df.Amortized_CSM_CSM_AMOR_Proc
        df["FCF_Death_Claims"] = df.Change_in_FCF_Death_Claim_SM_Proc
        df["Insurance Expense New Biz_VFA"] = df.FCF_Death_Claims
        return df
