import importlib.resources as pkg_resources

import pandas as pd

import cm_dashboards.bs_pl
from cm_dashboards.reinsurance import re_trial_balance_handler as r_tb
from cm_dashboards.subledger import abstract_handler as gf
from cm_dashboards.subledger import trial_balance_handler as o_tb


class ProfitLossHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "profit_loss_template.csv"

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def prepare_data(self, jobrun_id):
        profit_loss_tb = self.get_orig_trial_balance(jobrun_id)
        profit_loss_re = self.get_re_trial_balance(jobrun_id)

        # combine Original and Reinsurance fields
        profit_loss = profit_loss_tb.append(profit_loss_re)

        # TODO: Placeholder values
        profit_loss.loc["Expected Inspection Cost"] = 0
        profit_loss.loc["Expected Investment Management Cost"] = 0
        profit_loss.loc["Other Insurance Revenue"] = 0

        profit_loss.loc["Insurance Revenue"] = profit_loss.loc[
            profit_loss.index.isin(
                [
                    "Expected Insurance Claim",
                    "Expected Acquisition Cost (not relevant premium)",
                    "Expected Maintenance Cost",
                    "Expected Inspection Cost",
                    "Expected Investment Management Cost",
                    "RA Variance",
                    "CSM Amortization",
                    "Expected Acquisition Cost Amortization",
                    "Other Insurance Revenue",
                ]
            )
        ].sum()

        # TODO: Placeholder value
        profit_loss.loc["Reinsurance Revenue"] = 0

        profit_loss.loc["Net Insurance Revenue"] = (
            profit_loss.loc["Insurance Revenue"]
            + profit_loss.loc["Reinsurance Revenue"]
        )

        # TODO: Most of these rows not populated yet
        profit_loss.loc["Insurance Expense"] = profit_loss.loc[
            profit_loss.index.isin(
                [
                    "Incurred Insurance Claim",
                    "Incurred Acquisition Cost (not relevant premium)",
                    "Incurred Maintenance Cost",
                    "Incurred Inspection Cost",
                    "Incurred Investment Management Cost",
                    "Incurred Acquisition Cost Amortization",
                    "Expense from Loss Contracts",
                    "LIC Adjustment",
                    "Other Insurance Expense",
                ]
            )
        ].sum()

        # TODO: Last 4 rows not populated yet
        profit_loss.loc["Reinsurance Expense"] = profit_loss.loc[
            profit_loss.index.isin(
                [
                    "Re CSM Amortization",
                    "Re Expected Insurance Claim",
                    "Re Expected Adjustment Cost",
                    "Re Expected Profit Commission",
                    "Re RA Variance",
                    "Gain(Loss) from Expected Reinsurance Premium",
                    "Expected Reinsurance Claim Recovery",
                    "PAA Expense",
                    "Other Reinsurance Expense",
                ]
            )
        ].sum()

        profit_loss.loc["Net Insurance Expense"] = (
            profit_loss.loc["Insurance Expense"]
            + profit_loss.loc["Reinsurance Expense"]
        )

        profit_loss.loc["Insurance Service Result"] = (
            profit_loss.loc["Net Insurance Revenue"]
            + profit_loss.loc["Net Insurance Expense"]
        )

        # TODO: Last 4 entries don't exist yet
        profit_loss.loc["Insurance Finance Expense"] = profit_loss.loc[
            profit_loss.index.isin(
                [
                    "LRC Finance Gain (Loss)",
                    "LIC Finance Gain (Loss)",
                    "Discount Rate Variance Impact",
                    "Foreign Currency Exchange",
                    "Other Finance Gain (Loss)",
                ]
            )
        ].sum()

        # TODO: Last 5 entries don't exist yet
        profit_loss.loc["Reinsurance Finance Expense"] = profit_loss.loc[
            profit_loss.index.isin(
                [
                    "LRC Reinsurance Finance Gain (Loss)",
                    "LIC Reinsurance Finance Gain (Loss)",
                    "Reinsurer Credit Loss Variance",
                    "Discount Rate Variance Impact",
                    "Foreign Currency Exchange",
                    "Other Finance Gain (Loss)",
                ]
            )
        ].sum()

        # TODO: First 2 entries don't exist yet
        profit_loss.loc["Finance Expense"] = profit_loss.loc[
            profit_loss.index.isin(
                [
                    "Interest Expense (not insurance-relevant)",
                    "Realized Loss from Sales of Financial Instruments",
                    "Insurance Finance Expense",
                    "Reinsurance Finance Expense",
                ]
            )
        ].sum()

        # TODO: First 1 entries don't exist yet
        profit_loss.loc["Net Financial Results"] = profit_loss.loc[
            profit_loss.index.isin(
                [
                    "Finance Income",
                    "Finance Expense",
                ]
            )
        ].sum()

        # TODO: First 1 entries don't exist yet
        profit_loss.loc["Net Profit (Loss) before Tax"] = profit_loss.loc[
            profit_loss.index.isin(
                [
                    "Insurance Service Result",
                    "Net Financial Results",
                ]
            )
        ].sum()

        profit_loss.loc["Corporate Income Tax"] = (
            profit_loss.loc["Net Profit (Loss) before Tax"] * 0.2
        )
        profit_loss.loc["Net Profit (Loss) after Tax"] = (
            profit_loss.loc["Net Profit (Loss) before Tax"]
            - profit_loss.loc["Corporate Income Tax"]
        )

        self.prepared_data = profit_loss

    def get_orig_trial_balance(self, jobrun_id):
        """
        Prepare Original Trial Balance data
        """
        orig_handler = o_tb.TrialBalanceHandler()
        # Get trial balance data
        orig_handler.prepare_data(jobrun_id)
        orig_tb = orig_handler.prepared_data

        # Get Insurance, Interest Fields
        trimmed_orig_tb = orig_tb[orig_tb.index.str.startswith("Insurance Revenue New")]

        trimmed_orig_tb = trimmed_orig_tb.append(
            orig_tb.loc["Insurance Expense New Biz-DAC Amor."]
        )
        trimmed_orig_tb = trimmed_orig_tb.append(
            orig_tb[orig_tb.index.str.startswith("Interest Expense New")]
        )
        trimmed_orig_tb["IFRS17"] = trimmed_orig_tb["Credit"] - trimmed_orig_tb["Debit"]
        trimmed_orig_tb = trimmed_orig_tb.drop(
            [
                "Credit",
                "Debit",
            ],
            axis=1,
        )

        # Rename trial balance rows to match Profit Loss row names
        trimmed_orig_tb = trimmed_orig_tb.rename(
            index={
                "Insurance Revenue New Biz-Exp. Claim": "Expected Insurance Claim",
                "Insurance Revenue New Biz-Exp. DAC(Premium-irrelevant)": "Expected Acquisition Cost (not relevant premium)",
                "Insurance Revenue New Biz-Exp. Maint. Cost": "Expected Maintenance Cost",
                "Insurance Revenue New Biz-Exp. Insp. Cost": "Expected Inspection Cost",
                "Insurance Revenue New Biz-Exp. Inv. Mng. Cost": "Expected Investment Management Cost",
                "Insurance Revenue New Biz-RA Changes": "RA Variance",
                "Insurance Revenue New Biz-CSM Amor.": "CSM Amortization",
                "Insurance Revenue New Biz-DAC Amor": "Expected Acquisition Cost Amortization",
                "Insurance Expense New Biz-DAC Amor.": "Incurred Acquisition Cost Amortization",
            }
        )

        # Sum to calculate value in PL
        trimmed_orig_tb.loc["LRC Finance Gain (Loss)"] = trimmed_orig_tb.loc[
            trimmed_orig_tb.index.str.startswith("Interest Expense New Biz")
        ].sum()

        # Drop old expense columns
        trimmed_orig_tb = trimmed_orig_tb[
            ~trimmed_orig_tb.index.str.startswith("Interest Expense New")
        ]

        return trimmed_orig_tb

    def get_re_trial_balance(self, jobrun_id):
        """
        Prepare Reinsurance Trial Balance data
        """
        re_handler = r_tb.ReTrialBalanceHandler()
        # Get reinsurance trial balance data
        re_handler.prepare_data(jobrun_id)
        re_tb = re_handler.prepared_data

        # Get Insurance, Interest Fields
        trimmed_re_tb = re_tb[re_tb.index.str.startswith("Reinsurance Expense New")]

        trimmed_re_tb = trimmed_re_tb.append(
            re_tb[re_tb.index.str.startswith("Reinsurance Interest Expense New")]
        )
        trimmed_re_tb["IFRS17"] = trimmed_re_tb["Credit"] - trimmed_re_tb["Debit"]
        trimmed_re_tb = trimmed_re_tb.drop(
            [
                "Credit",
                "Debit",
            ],
            axis=1,
        )

        # Rename trial balance rows to match Profit Loss row names
        trimmed_re_tb = trimmed_re_tb.rename(
            index={
                "Reinsurance Expense New Biz-CSM Amor._REINS": "Re CSM Amortization",
                "Reinsurance Expense New Biz-Exp. Claim_REINS": "Re Expected Insurance Claim",
                "Reinsurance Expense New Biz-Exp. Adj. Cost_REINS": "Re Expected Adjustment Cost",
                "Reinsurance Expense New Biz-Exp. Profit Comm_REINS": "Re Expected Profit Commission",
                "Reinsurance Expense New Biz-RA Changes_REINS": "Re RA Variance",
            }
        )

        trimmed_re_tb.loc["LRC Reinsurance Finance Gain (Loss)"] = trimmed_re_tb.loc[
            trimmed_re_tb.index.str.startswith("Reinsurance Interest Expense New")
        ].sum()

        return trimmed_re_tb

    def subledger_apply_template(self):
        """
        Apply data to subledger template
        """
        # Get template for ledger table
        template_csv = pkg_resources.open_text(
            cm_dashboards.bs_pl, self.get_subledger_template()
        )
        self.template = pd.read_csv(template_csv)

        # Merge R3S data into template
        pop_template = pd.merge(
            self.template,
            self.prepared_data,
            left_on="ITEMS",
            right_on="Account_Name",
            how="left",
            suffixes=("", "_y"),
        )
        # Drop duplicate COA column
        pop_template.drop(
            pop_template.filter(regex="_y$").columns.tolist(), axis=1, inplace=True
        )
        return pop_template.fillna(0)
