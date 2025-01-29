from cm_dashboards.subledger import abstract_handler as gf


class LossCompHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "losscomp_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        # Confirmation of loss FCF according to the GOD loss rate at the end of the term
        df["Confirming_BEL_OtherComp"] = df.Ending_Reset_BEL_Loss_LossComp_Proc
        df["Confirming_RA_OtherComp"] = df.Ending_Reset_RA_Loss_LossComp_Proc
        # Writing the difference between the balance after economic assumption and the balance updated current EIR on OCI account
        df["AOCI(BEL)_Loss_OtherComp"] = self.pos(
            df.Ending_AOCI_BEL_Other_LossComp_Proc
        )
        df["AOCI(BEL)_Gain_OtherComp"] = self.change_sign(
            self.neg(df.Ending_AOCI_BEL_Other_LossComp_Proc)
        )
        df["AOCI(BEL)_Loss_LossComp"] = self.pos(df.Ending_AOCI_BEL_Loss_LossComp_Proc)
        df["AOCI(BEL)_Gain_LossComp"] = self.neg(df.Ending_AOCI_BEL_Loss_LossComp_Proc)
        df["AOCI(RA)_Loss_OtherComp"] = self.pos(df.Ending_AOCI_RA_Other_LossComp_Proc)
        df["AOCI(RA)_Gain_OtherComp"] = self.neg(df.Ending_AOCI_RA_Other_LossComp_Proc)
        df["AOCI(RA)_Loss_LossComp"] = self.pos(df.Ending_AOCI_RA_Loss_LossComp_Proc)
        df["AOCI(RA)_Gain_LossComp"] = self.neg(df.Ending_AOCI_RA_Loss_LossComp_Proc)
        # Writing deferred corporate tax anount derived from the OCI amount for the current term
        # BEL
        df["Ending_corporate_tax_AOCI_BEL_Loss_neg"] = self.neg(
            df.Ending_corporate_tax_AOCI_BEL_Loss
        )
        df["Ending_corporate_tax_AOCI_BEL_Other_neg"] = self.neg(
            df.Ending_corporate_tax_AOCI_BEL_Other
        )
        df["DTL_for_BEL_Loss"] = (
            df.Ending_corporate_tax_AOCI_BEL_Loss_neg
            + df.Ending_corporate_tax_AOCI_BEL_Other_neg
        )
        df["Ending_corporate_tax_AOCI_BEL_Loss_pos"] = self.change_sign(
            self.pos(df.Ending_corporate_tax_AOCI_BEL_Loss)
        )
        df["Ending_corporate_tax_AOCI_BEL_Other_pos"] = self.change_sign(
            self.pos(df.Ending_corporate_tax_AOCI_BEL_Other)
        )
        df["DTL_for_BEL_Gain"] = (
            df.Ending_corporate_tax_AOCI_BEL_Loss_pos
            + df.Ending_corporate_tax_AOCI_BEL_Other_pos
        )
        # RA
        df["Ending_corporate_tax_AOCI_RA_Loss_neg"] = self.neg(
            df.Ending_corporate_tax_AOCI_RA_Loss
        )
        df["Ending_corporate_tax_AOCI_RA_Other_neg"] = self.neg(
            df.Ending_corporate_tax_AOCI_RA_Other
        )
        df["DTL_for_RA_Loss"] = (
            df.Ending_corporate_tax_AOCI_RA_Loss_neg
            + df.Ending_corporate_tax_AOCI_RA_Other_neg
        )
        df["Ending_corporate_tax_AOCI_RA_Loss_pos"] = self.change_sign(
            self.pos(df.Ending_corporate_tax_AOCI_RA_Loss)
        )
        df["Ending_corporate_tax_AOCI_RA_Other_pos"] = self.change_sign(
            self.pos(df.Ending_corporate_tax_AOCI_RA_Other)
        )
        df["DTL_for_RA_Gain"] = (
            df.Ending_corporate_tax_AOCI_RA_Loss_pos
            + df.Ending_corporate_tax_AOCI_RA_Other_pos
        )
        return df
