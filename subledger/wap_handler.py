from cm_dashboards.subledger import abstract_handler as gf


class WapHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "wap_template.csv"

    DB_QUERY = "SELECT A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        # CSM adjustment for the difference between initial recognition and weighted average for New Businesses(Cohort-open)
        df["Insurance_Expense_for_Loss_component_BEL_RA_DIFF"] = (
            df.New_Biz_Weighted_Avg_Loss_BEL_Diff_RSP_WAP_Proc
            + df.New_Biz_Wwighted_Avg_Loss_RA_Diff_RSP_WAP_Proc
        )
        df["CSM_Adjustment_for_Other_component_BEL_RA_DIFF"] = (
            df.New_Biz_Weighted_Avg_Other_BEL_Diff_RSP_WAP_Proc
            + df.New_Biz_Weighted_Avg_Other_RA_Diff_RSP_WAP_Proc
        )
        # CSM adjustment for expected premium
        df["CSM_Adjustment_for_expected_Prem"] = df.Expected_Premium_Total_RSP_WAP_Proc
        # Reversal of profit/loss for expected claim (insurance component)
        # TODO: Change sign
        df[
            "Insurance_Revenue_for_Other_component_Expected_Claim"
        ] = df.Exp_Claim_Insurance_Component_Other_RSP_WAP_Proc = self.change_sign(
            df.Exp_Claim_Insurance_Component_Other_RSP_WAP_Proc
        )
        df[
            "Insurance_Expense_for_Loss_component_Expected_Claim"
        ] = df.Exp_Claim_Insurance_Component_Loss_RSP_WAP_Proc = self.change_sign(
            df.Exp_Claim_Insurance_Component_Loss_RSP_WAP_Proc
        )
        # Reversal of CSM/loss for expected claim (investment component)
        df[
            "CSM_Reversal_for_Other_component_Expected_Claim"
        ] = df.Exp_Claim_Investment_Component_Other_RSP_WAP_Proc = self.change_sign(
            df.Exp_Claim_Investment_Component_Other_RSP_WAP_Proc
        )
        df[
            "Loss_Reversal_for_Loss_component_Expected_Claim"
        ] = df.Exp_Claim_Investment_Component_Loss_RSP_WAP_Proc = self.change_sign(
            df.Exp_Claim_Investment_Component_Loss_RSP_WAP_Proc
        )
        # Reversal of CSM/loss for expected direct acquisition cost (premium-relevant)
        df[
            "CSM_Reversal_for_Other_component_Expected_Direct_Acq_Cost_PremR"
        ] = df.Exp_Direct_Acq_Cost_Prem_Other_RSP_WAP_Proc = self.change_sign(
            df.Exp_Direct_Acq_Cost_Prem_Other_RSP_WAP_Proc
        )
        df[
            "Loss_Reversal_for_Loss_component_Expected_Direct_Acq_Cost_PremR"
        ] = df.Exp_Direct_Acq_Cost_Prem_Loss_RSP_WAP_Proc = self.change_sign(
            df.Exp_Direct_Acq_Cost_Prem_Loss_RSP_WAP_Proc
        )
        # Reversal of profit/loss for expectaed direct acquisition cost (premium-irrelevant)
        df[
            "Profit_Reversal_for_Other_component_Expected_Direct_Acq_Cost_NonPremR"
        ] = df.Exp_Direct_Acq_Cost_Non_Prem_Other_RSP_WAP_Proc = self.change_sign(
            df.Exp_Direct_Acq_Cost_Non_Prem_Other_RSP_WAP_Proc
        )
        df[
            "Loss_Reversal_for_Loss_component_Expected_Direct_Acq_Cost_NonPremR"
        ] = df.Exp_Direct_Acq_Cost_Non_Prem_Loss_RSP_WAP_Proc = self.change_sign(
            df.Exp_Direct_Acq_Cost_Non_Prem_Loss_RSP_WAP_Proc
        )
        # Reversal of profit/loss for expected direct maintenance cost
        df[
            "Profit_Reversal_for_Other_component_Expected_Direct_Maint_Cost"
        ] = df.Exp_Direct_Maintenance_Cost_Other_RSP_WAP_Proc = self.change_sign(
            df.Exp_Direct_Maintenance_Cost_Other_RSP_WAP_Proc
        )
        df[
            "Loss_Reversal_for_Loss_component_Expected_Direct_Maint_Cost"
        ] = df.Exp_Direct_Maintenance_Cost_Loss_RSP_WAP_Proc = self.change_sign(
            df.Exp_Direct_Maintenance_Cost_Loss_RSP_WAP_Proc
        )
        # Reversal of profit/loss for expected direct inspection cost
        df[
            "Profit_Reversal_for_Other_component_Expected_Direct_Inspection_Cost"
        ] = df.Expected_Direct_Inspection_Cost_Other_RSP_WAP_Proc = self.change_sign(
            df.Expected_Direct_Inspection_Cost_Other_RSP_WAP_Proc
        )
        df[
            "Loss_Reversal_for_Loss_component_Expected_Direct_Inspection_Cost"
        ] = df.Expected_Direct_Inspection_Cost_Loss_RSP_WAP_Proc = self.change_sign(
            df.Expected_Direct_Inspection_Cost_Loss_RSP_WAP_Proc
        )
        # Reversal of profit/loss for expected direct investment management cost
        df[
            "Profit_Reversal_for_Other_component_Expected_Direct_Invest_Manage_Cost"
        ] = df.Exp_Direct_Invest_Manage_Cost_Other_RSP_WAP_Proc = self.change_sign(
            df.Exp_Direct_Invest_Manage_Cost_Other_RSP_WAP_Proc
        )
        df[
            "Loss_Reversal_for_Loss_component_Expected_Direct_Invest_Manage_Cost"
        ] = df.Exp_Direct_Invest_Manage_Cost_Loss_RSP_WAP_Proc = self.change_sign(
            df.Exp_Direct_Invest_Manage_Cost_Loss_RSP_WAP_Proc
        )
        # Reversal of CSM/loss for expected policy loan cash flows
        df[
            "CSM_Reversal_for_Other_componenet_Expected_PL"
        ] = df.Expected_Policy_Loan_Cash_Flows_Other_RSP_WAP_Proc = self.change_sign(
            df.Expected_Policy_Loan_Cash_Flows_Other_RSP_WAP_Proc
        )
        df[
            "Loss_Reversal_for_Loss_component_Expected_PL"
        ] = df.Expected_Policy_Loan_Cash_Flows_Loss_RSP_WAP_Proc = self.change_sign(
            df.Expected_Policy_Loan_Cash_Flows_Loss_RSP_WAP_Proc
        )
        # Reversal of profit/loss for expected RA amortization
        df[
            "Profit_Reversal_for_Other_component_RA_Amort"
        ] = df.RA_amortization_Other_RSP_WAP_Proc = self.change_sign(
            df.RA_amortization_Other_RSP_WAP_Proc
        )
        df[
            "Loss_Reversal_for_Loss_component_RA_Amort"
        ] = df.RA_amortization_Loss_RSP_WAP_Proc = self.change_sign(
            df.RA_amortization_Loss_RSP_WAP_Proc
        )
        # TODO: End of Change sign
        # Recognition of interest expense for BEL difference between beginning and end of the term
        df["Interest_Expense_Recognition_for_BEL_DIFF"] = (
            df.Reset_BEL_Interest_Expense_Other_RSP_WAP_Proc
            + df.Reset_BEL_Interest_Expense_Loss_RSP_WAP_Proc
        )
        # Recognition of intereset expense for RA difference between beginning and end of the term
        df["Interest_Expense_Recognition_for_RA_DIFF"] = (
            df.Reset_RA_Interest_Expense_Other_RSP_WAP_Proc
            + df.Reset_RA_Interest_Expense_Loss_RSP_WAP_Proc
        )
        # Redemption of CSM / reversal of loss component based on initial BEL and RA
        df[
            "Loss_Reversal_for_Loss_component_Initial_BEL"
        ] = df.Exp_Initial_BEL_Loss_RSP_WAP_Proc
        df[
            "CSM_Reversal_for_Other_componenet_Initial_BEL"
        ] = df.Exp_Initial_BEL_Other_RSP_WAP_Proc
        df[
            "Loss_Reversal_for_Loss_component_Initial_RA"
        ] = df.Exp_Initial_RA_Loss_RSP_WAP_Proc
        df[
            "CSM_Reversal_for_Other_componenet_Initial_RA"
        ] = df.Exp_Initial_RA_Other_RSP_WAP_Proc
        # Interest expense adjustment for reversal of reset BEL and RA
        df[
            "Interest_Expense_Adjust_for_Loss_componenet_BEL"
        ] = df.Expected_WA_BEL_Loss_RSP_WAP_Proc
        df[
            "Interest_Expense_Adjust_for_Other_componenet_BEL"
        ] = df.Expected_WA_BEL_Other_RSP_WAP_Proc
        df[
            "Interest_Expense_Adjust_for_Loss_componenet_RA"
        ] = df.Expected_WA_RA_Loss_RSP_WAP_Proc
        df[
            "Interest_Expense_Adjust_for_Other_componenet_RA"
        ] = df.Expected_WA_RA_Other_RSP_WAP_Proc

        return df
