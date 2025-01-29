from cm_dashboards.reinsurance import abstract_handler as gf


class RwuHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "rwu_template.csv"

    DB_QUERY = (
        "select A00_Treaty as COA, * from FMP_WAP.I_Reins_RNC_RWU f "
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
        # CSM adjustment for the difference between initial recognition and weighted average for New Businesses(Cohort-open)
        df["CSM_Adjustment_for_Diff_REINS"] = (
            df.NB_WA_BEL_Diff_REINS_RNC_RWU_Proc
            + df.NB_WA_RA_Diff_REINS_RNC_RWU_Proc
            - df.NB_WA_CL_BEL_Diff_REINS_RNC_RWU_Proc
        )
        # CSM adjustment for expected reinsurance premium
        df[
            "CSM_Adjustment_for_expected_Prem_REINS"
        ] = df.Exp_Reins_Prem_Total_REINS_RNC_RWU_Proc
        # Reversal of profit for expected direct adjustment cost
        df[
            "Reversal_Profit_Expected_Direct_Adjust_Cost_REINS"
        ] = df.Exp_Direct_Adjust_Cost_REINS_RNC_RWU_Proc
        # Reversal of profit for expected claim (insurance component)
        df[
            "Reversal_Profit_Expected_Prem_REINS"
        ] = df.Exp_Reins_Benefit_REINS_RNC_RWU_Proc
        # Reversal of profit for expected profit commission
        df[
            "Reversal_Profit_Expected_Profit_Commission_REINS"
        ] = df.Exp_Reins_Benefit_Profit_Comm_REINS_RNC_RWU_Proc
        # Reversal of profit for expected RA amortization
        df[
            "Reversal_Profit_Expected_RA_Amort_REINS"
        ] = -df.Exp_RA_Amort_REINS_RNC_RWU_Proc
        # Recognition of intereset expense for BEL difference between beginning and end of the term
        df[
            "Recognition_Interest_Expense_BEL_DIFF_REINS"
        ] = df.Interest_Expense_WA_BEL_REINS_RNC_RWU_Proc
        # Recognition of intereset expense for RA difference between beginning and end of the term
        df[
            "Recognition_Interest_Expense_RA_DIFF_REINS"
        ] = df.Interest_Expense_WA_RA_REINS_RNC_RWU_Proc
        # Recognition of intereset expense for credit loss BEL difference between beginning and end of the term
        df[
            "Recognition_Interest_Expense_Credit_Loss_DIFF_REINS"
        ] = df.Interest_Expense_WA_CL_BEL_REINS_RNC_RWU_Proc
        # Recovery of CSM as redeeming interest expense based on initial BEL, RA and credit loss BEL
        df["Recovery_CSM_Redeeming_Interest_Expense_REINS"] = (
            df.Exp_Initial_BEL_REINS_RNC_RWU_Proc
            + df.Exp_Initial_RA_REINS_RNC_RWU_Proc
            - df.Exp_Initial_Credit_Loss_BEL_REINS_RNC_RWU_Proc
        )
        # Interest expense adjustment for reversal of reset BEL, RA and credit loss BEL
        df[
            "Interest_Expense_Adjustment_to_Reverse_BEL_REINS"
        ] = df.Exp_WA_BEL_REINS_RNC_RWU_Proc
        df[
            "Interest_Expense_Adjustment_to_Reverse_RA_REINS"
        ] = df.Exp_WA_RA_REINS_RNC_RWU_Proc
        df[
            "Interest_Expense_Adjustment_to_Reverse_CSM_REINS"
        ] = df.Exp_WA_Credit_Loss_BEL_REINS_RNC_RWU_Proc

        return df
