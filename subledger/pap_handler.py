from cm_dashboards.subledger import abstract_handler as gf


class PapHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "pap_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        # Writing CSM/expense of the amount of BEL and RA after actuarial assumption based on initial EIR
        df["Writing_Expense_BEL_Loss_INIT_EIR_PAP"] = df.Initial_BEL_Loss_PAP_Proc
        df["Writing_Expense_BEL_Other_INIT_EIR_PAP"] = df.Initial_BEL_Other_PAP_Proc
        df["Writing_Expense_RA_Loss_INIT_EIR_PAP"] = df.Initial_RA_Loss_PAP_Proc
        df["Writing_Expense_RA_Other_INIT_EIR_PAP"] = df.Initial_RA_Other_PAP_Proc
        # Writing CSM/expense of the amount of BEL and RA after actuarial assumption based on initial EIR
        df["Redemption_Expense_BEL_Loss_INIT_EIR_PAP"] = df.Initial_BEL_Loss_PAP_Proc
        df["Redemption_Expense_BEL_Other_INIT_EIR_PAP"] = df.Initial_BEL_Other_PAP_Proc
        df["Redemption_Expense_RA_Loss_INIT_EIR_PAP"] = df.Initial_RA_Loss_PAP_Proc
        df["Redemption_Expense_RA_Other_INIT_EIR_PAP"] = df.Initial_RA_Other_PAP_Proc
        # Writing interest expense and the amount of BEL and RA after actuarial assumption based on reset EIR
        df["Writing_Expense_BEL_Loss_Reset_EIR_PAP"] = df.Reset_BEL_Loss_PAP_Proc
        df["Writing_Expense_BEL_Other_Reset_EIR_PAP"] = df.Reset_BEL_Other_PAP_Proc
        df["Writing_Expense_RA_Loss_Reset_EIR_PAP"] = df.Reset_RA_Loss_PAP_Proc
        df["Writing_Expense_RA_Other_Reset_EIR_PAP"] = df.Reset_RA_Other_PAP_Proc
        # Redemption of interest expense and the same amount of BEL and RA after actuarial assumption based on reset EIR
        df["Redemption_Expense_BEL_Loss_Reset_EIR_PAP"] = df.Reset_BEL_Loss_PAP_Proc
        df["Redemption_Expense_BEL_Other_Reset_EIR_PAP"] = df.Reset_BEL_Other_PAP_Proc
        df["Redemption_Expense_RA_Loss_Reset_EIR_PAP"] = df.Reset_RA_Loss_PAP_Proc
        df["Redemption_Expense_RA_Other_Reset_EIR_PAP"] = df.Reset_RA_Other_PAP_Proc
        return df
