import importlib.resources as pkg_resources

import pandas as pd

import cm_dashboards.bs_pl
from cm_dashboards.reinsurance import re_trial_balance_handler as r_tb
from cm_dashboards.subledger import abstract_handler as gf
from cm_dashboards.subledger import trial_balance_handler as o_tb


class BalanceSheetHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "balance_sheet_template.csv"

    def __init__(self, profit_loss_data_param):
        self.profit_loss_data = profit_loss_data_param

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def prepare_data(self, jobrun_id):
        balance_sheet_tb = self.get_orig_trial_balance(jobrun_id)
        balance_sheet_re = self.get_re_trial_balance(jobrun_id)

        # combine Original and Reinsurance fields
        balance_sheet = balance_sheet_tb.append(balance_sheet_re)

        # TODO: setting placeholder values
        balance_sheet.loc["Re Claim reserve"] = -11540111
        balance_sheet.loc["Premium reserve - unearned premium reserve"] = -50572903

        balance_sheet.loc["Reinsurance assets"] = (
            balance_sheet.loc["Re Claim reserve"]
            + balance_sheet.loc["Premium reserve - unearned premium reserve"]
        )

        balance_sheet.loc["Loans"] = -147462532
        balance_sheet.loc["Investment in securities"] = 0
        balance_sheet.loc["Investment assets"] = (
            balance_sheet.loc["Investment in securities"] + balance_sheet.loc["Loans"]
        )

        balance_sheet.loc["ARC Ceding"] = balance_sheet.loc[
            balance_sheet.index.str.startswith("ARC Ceding")
        ].sum()

        # TODO: setting placeholder values
        balance_sheet.loc["AIC Ceding"] = 0
        balance_sheet.loc["ARC Reinsurance"] = 0
        balance_sheet.loc["AIC Reinsurance"] = 0
        balance_sheet.loc["INSURANCE CONTRACT ASSETS"] = (
            balance_sheet.loc["ARC Ceding"]
            + balance_sheet.loc["AIC Ceding"]
            + balance_sheet.loc["ARC Reinsurance"]
            + balance_sheet.loc["AIC Reinsurance"]
        )
        balance_sheet.loc["TOTAL ASSETS"] = balance_sheet.loc[
            balance_sheet.index.isin(
                [
                    "INSURANCE CONTRACT ASSETS",
                    "Cash and cash equivalent",
                    "Premium receivables",
                    "Accrued investment income",
                    "Reinsurance assets",
                    "Amount due from reinsurers",
                    "Investment assets",
                    "Leasehold improvement and equipment",
                    "Intangible assets",
                    "Deferred tax assets",
                    "Other assets",
                    "INSURANCE CONTRACT ASSETS",
                ]
            )
        ].sum()

        # TODO: Setting placeholder values
        balance_sheet.loc["Long-tem insurance contract reserve"] = -22657777182
        balance_sheet.loc["Claim reserve"] = -40986107
        balance_sheet.loc["Reserves for incurred and reported"] = -17804570
        balance_sheet.loc["Reserves for claim (IBNR)"] = -23181537
        balance_sheet.loc["Premium reserve"] = -89732853
        balance_sheet.loc["Unearned premium reserve"] = -89732853
        balance_sheet.loc["Unpaid policy benefits"] = -46367447
        balance_sheet.loc["Other insurance liabilities"] = -81595118
        balance_sheet.loc["Insurance liabilities"] = balance_sheet.loc[
            balance_sheet.index.isin(
                [
                    "Long-tem insurance contract reserve",
                    "Claim reserve",
                    "Premium reserve",
                    "Unpaid policy benefits",
                    "Other insurance liabilities",
                ]
            )
        ].sum()

        pl_data = self.get_profit_loss()
        balance_sheet.loc["Corporate income tax"] = pl_data.loc["Corporate Income Tax"][
            "IFRS17"
        ]

        # TODO: Hardcoded
        balance_sheet.loc["IFRS17 adjustments"] = 4533179411

        balance_sheet.loc["LRC Ceding"] = balance_sheet.loc[
            balance_sheet.index.str.startswith("LRC")
        ].sum()

        balance_sheet.loc["LIC Ceding"] = balance_sheet.loc[
            balance_sheet.index.str.startswith("LIC")
        ].sum()

        balance_sheet.loc["TECHNICAL RESERVES (IFRS17)"] = balance_sheet.loc[
            balance_sheet.index.isin(
                [
                    "LRC Ceding",
                    "LIC Ceding",
                    "LRC Reinsurance",
                    "LIC Reinsurance",
                    "Liability of Investment contracts",
                ]
            )
        ].sum()

        balance_sheet.loc["TOTAL LIABILITIES"] = balance_sheet.loc[
            balance_sheet.index.isin(
                [
                    "Amount due to reinsurers",
                    "Income tax payable",
                    "Employee benefit obligations",
                    "Deferred tax liabilities",
                    "Finance lease liabilities",
                    "Other liabilities",
                    "TECHNICAL RESERVES (IFRS17)",
                ]
            )
        ].sum()

        balance_sheet.loc["IFRS17 adjustments (unapp.)"] = 18132717643
        balance_sheet.loc["Net profit (loss) after tax"] = pl_data.loc[
            "Net Profit (Loss) after Tax"
        ]["IFRS17"]
        balance_sheet.loc["Unappropriated"] = balance_sheet.loc[
            balance_sheet.index.isin(
                [
                    "T-GAAP balance",
                    "IFRS17 adjustments (unapp.)",
                    "Net profit (loss) after tax",
                ]
            )
        ].sum()

        balance_sheet.loc["ACCUMULATED OCI"] = balance_sheet.loc[
            balance_sheet.index.isin(
                [
                    "AOCI LRC before tax",
                    "AOCI LIC",
                    "AOCI reinsurance LRC before tax",
                    "AOCI reinsurance LIC",
                ]
            )
        ].sum()

        balance_sheet.loc["TOTAL OWNERS' EQUITY"] = balance_sheet.loc[
            balance_sheet.index.isin(
                [
                    "Issued and paid-up share capital",
                    "PREMIUM ON ORDINARY SHARE CAPITAL",
                    "Legal reserve",
                    "Unappropriated",
                    "OTHER COMPONENTS OF EQUITY",
                    "ACCUMULATED OCI",
                ]
            )
        ].sum()

        balance_sheet.loc["TOTAL LIABILITIES AND OWNERS' EQUITY"] = balance_sheet.loc[
            balance_sheet.index.isin(
                [
                    "TOTAL LIABILITIES",
                    "TOTAL OWNERS' EQUITY",
                ]
            )
        ].sum()

        # print(balance_sheet)
        self.prepared_data = balance_sheet

    def get_profit_loss(self):
        """
        Prepare Profit/Loss dataframe
        """
        pl_data = self.profit_loss_data
        # Reduce down to the entries that we are interested in
        pl_data_trimmed = pl_data[
            pl_data.index.isin(["Corporate Income Tax", "Net Profit (Loss) after Tax"])
        ]
        return pl_data_trimmed

    def get_orig_trial_balance(self, jobrun_id):
        """
        Prepare Original Trial Balance data
        """
        orig_handler = o_tb.TrialBalanceHandler()
        # Get trial balance data
        orig_handler.prepare_data(jobrun_id)
        orig_tb = orig_handler.prepared_data

        # Get Insurance, Interest Fields
        # Get BEL, RA, etc. Fields
        trimmed_orig_tb = orig_tb[
            orig_tb.index.isin(
                [
                    "BEL",
                    "RA",
                    "CSM",
                    "Deferred Tax Liabilities",
                    "AOCI",
                ]
            )
        ]
        trimmed_orig_tb["Adjustments"] = (
            trimmed_orig_tb["Credit"] - trimmed_orig_tb["Debit"]
        )
        trimmed_orig_tb = trimmed_orig_tb.drop(
            [
                "Credit",
                "Debit",
            ],
            axis=1,
        )

        # Rename trial balance rows to match Balance Sheet row names
        trimmed_orig_tb = trimmed_orig_tb.rename(
            index={
                "BEL": "LRC BEL",
                "RA": "LRC RA",
                "CSM": "LRC CSM",
                "Deferred Tax Liabilities": "AOCI LRC deferred tax",
                "AOCI": "AOCI LRC before tax",
            }
        )

        return trimmed_orig_tb

    def get_re_trial_balance(self, jobrun_id):
        """
        Prepare Reinsurance Trial Balance data
        """
        re_handler = r_tb.ReTrialBalanceHandler()
        # Get reinsurance trial balance data
        re_handler.prepare_data(jobrun_id)
        re_tb = re_handler.prepared_data

        # Get BEL, RA, etc. Fields
        trimmed_re_tb = re_tb[
            re_tb.index.isin(
                [
                    "BEL",
                    "RA",
                    "Credit Loss BEL",
                    "CSM",
                    "Deferred Tax Liabilities",
                    "AOCI",
                ]
            )
        ]

        trimmed_re_tb["Adjustments"] = trimmed_re_tb["Debit"] - trimmed_re_tb["Credit"]
        # Only these 2 fields subtracted opposite way round
        trimmed_re_tb.loc["Deferred Tax Liabilities"]["Adjustments"] = (
            trimmed_re_tb.loc["Deferred Tax Liabilities"]["Credit"]
            - trimmed_re_tb.loc["Deferred Tax Liabilities"]["Debit"]
        )
        trimmed_re_tb.loc["AOCI"]["Adjustments"] = (
            trimmed_re_tb.loc["AOCI"]["Credit"] - trimmed_re_tb.loc["AOCI"]["Debit"]
        )
        trimmed_re_tb = trimmed_re_tb.drop(
            [
                "Credit",
                "Debit",
            ],
            axis=1,
        )

        # Rename trial balance rows to match Balance Sheet row names
        trimmed_re_tb = trimmed_re_tb.rename(
            index={
                "BEL": "ARC Ceding BEL",
                "RA": "ARC Ceding RA",
                "Credit Loss BEL": "ARC Ceding Credit Loss BEL",
                "CSM": "ARC Ceding CSM",
                "Deferred Tax Liabilities": "AOCI reinsurance LRC deferred tax",
                "AOCI": "AOCI reinsurance LRC before tax",
            }
        )

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
            left_on="ASSETS",
            right_on="Account_Name",
            how="left",
            suffixes=("", "_y"),
        )
        # Drop duplicate COA column
        pop_template.drop(
            pop_template.filter(regex="_y$").columns.tolist(), axis=1, inplace=True
        )
        return pop_template  # .fillna(0)
