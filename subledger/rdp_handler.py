from cm_dashboards.subledger import abstract_handler as gf


class RdpHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "rdp_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        # Recognition of interest expense as actual rate applied
        df[
            "Loss_Reversal_for_Loss_Component_EXP_BEL_Actual_rate_Proc"
        ] = df.Exp_BEL_Loss_component_Diff_Actual_Rate_RDP_Proc
        df[
            "CSM_for_Loss_Component_EXP_BEL_Actual_rate"
        ] = df.Exp_BEL_Other_component_Diff_Actual_Rate_RDP_Proc
        df[
            "Loss_Reversal_for_Loss_Component_EXP_RA_Actual_rate"
        ] = df.Exp_RA_Loss_component_Diff_Actual_Rate_RDP_Proc
        df[
            "CSM_for_Loss_Component_EXP_RA_Actual_rate"
        ] = df.Exp_RA_Other_component_Diff_Actual_Rate_RDP_Proc
        return df
