import logging

logger = logging.getLogger(__name__)

import pandas as pd
import plotly.graph_objects as go

import cm_dashboards.flaor.utils.helpers as helpers
from cm_dashboards.flaor.results.prepare_data import get_data
from cm_dashboards.flaor.results.program_names import ChartNames, ProgramNames


def get_chart(
    wvr_files=None,
    name=None,
    prepared_data=None,
    with_table_data=False,
    hide_title=False,
):
    """
    Helper function to generate bar charts
    :param wvr_files: dict of WVR paths
    :param name: chart name (Enum)
    :param prepared_data: dict of prepared data
    """
    # Initialize variables
    color_schema = helpers.set_color_schema(name)
    header_rows = []
    multi_index = True

    # Extract wvr paths
    if wvr_files is not None:
        kics_path = wvr_files.get("kics")
        base_path = wvr_files.get("base")

    # Check if prepared data is provided
    if prepared_data is not None:
        data = pd.DataFrame(prepared_data)

    match name:
        case ChartNames.SOLVENCY_OVERALL:
            # Clean 'KICS_Ratio' column
            data["KICS_Ratio"] = data["KICS_Ratio"].apply(
                lambda x: float(x.replace("%", ""))
            )
            title = "Solvency Overall"
            x = "Report_Date"
            y = ["Available_Capital", "Required_Capital"]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                secondary_y="KICS_Ratio",
            )

            # Give space between y-axis and legend
            chart.update_layout(legend=dict(y=0.5, x=1.05))

        case ChartNames.AVAILABLE_CAPITAL:
            title = "Available Capital"
            x = "Report_Date"
            y = [
                "Capital_Surplus",
                "AOCI",
                "Capital_Adjustments",
                "Retained_Earnings",
                "Capital_Securities",
                "Common_Equity",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="stack",
            )

        case ChartNames.REQUIRED_CAPITAL:
            title = "Required Capital"
            x = "After_Before_Div"
            y = [
                "Required_Capital",
                "Operational_Risk",
                "Life_and_Hearth_Risk",
                "Market_Risk",
                "Credit_Risk",
                "Nonlife_Risk",
            ]

            # Duplicate each row
            data = helpers.duplicate_rows(
                data, y, "After_Before_Div", ["After Div", "Before Div"]
            )
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="stack",
                facet_col="Report_Date",
                pattern_shape="x",
            )

        case ChartNames.ASSET_PORTFOLIO:
            data = get_data(wvr_files, ProgramNames.ASSET_PORTFOLIO)
            title = "Asset Portfolio"
            x = "Report_Date"
            y = [
                "Bond",
                "Loan",
                "Cash",
                "Equity",
                "Property",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
            )

            for bar in chart.data:
                name = bar.name
                bar["text"] = data[name + "_Percent"]

            chart.update_traces(
                textfont=dict(size=13, color="#FFFFFF"),
                texttemplate="%{text}",
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate="<br>Value: %{y}<br>Percentage: %{text}<extra></extra>",
                selector=dict(type="bar"),
            )

            data = helpers.pivot_dataframe(data)

        case ChartNames.PROJECTED_RISK_REGULATORY:
            data = get_data(wvr_files, ProgramNames.PROJECTED_RISK_REGULATORY)
            title = "Projected MV B/S under Risk Regulation"
            x = "Report_Date"
            y = [
                "Assets_Total",
                "Liabilities_Total",
                "Capital_Total",
            ]

            risk_data = data[[x, *y]]
            risk_data = helpers.duplicate_rows(risk_data, y, "Divider", ["1", "2"])
            risk_regulation_chart = helpers.create_bar_chart(
                df=risk_data,
                x="Divider",
                y=y,
                title=title,
                color_schema=color_schema,
                facet_col="Report_Date",
            )

            title = "Projected MV Liability - Details"
            x = "Report_Date"
            y = [
                "BE_Liabilities_WO_TVOG",
                "TVOG",
                "LIC",
                "Risk_Margin",
                "Other_Liabilities",
            ]
            liability_details_chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
            )
            chart = [risk_regulation_chart, liability_details_chart]
            template, _ = helpers.get_template_df("projected_risk_regulatory")
            data = helpers.replace_template_values(template, data, True)

        case ChartNames.LIFE_AND_HEALTH_INSURANCE_RISK:
            title = "Life & Health Insurance Risk"
            x = "Report_Date"
            y = "Life_Health_Risk"
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
            )

        case ChartNames.LIFE_AND_HEALTH_RISK_OVERALL:
            title = "Life& Health Risk Overall"
            x = "Report_Date"
            y = [
                "Life_Health_Risk",
                "Mortality",
                "Longevity",
                "Morbidity",
                "Lapse",
                "Expense",
                "Catastrophe",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

        case ChartNames.MORTALITY_RISK:
            title = "Mortality Risk"
            x = "Report_Date"
            y = "Mortality"
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
            )

        case ChartNames.LONGEVITY_RISK:
            title = "Longevity Risk"
            x = "Report_Date"
            y = "Longevity"
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
            )

        case ChartNames.MORBITITY_RISK:
            title = "Morbidity Risk"
            x = "Report_Date"
            y = [
                "Morbidity",
                "Morbidity_Fixed",
                "Morbidity_Indemnity",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

        case ChartNames.LAPSE_RISK:
            title = "Lapse Risk"
            x = "Report_Date"
            y = ["Lapse", "Lapse_Up", "Lapse_Down", "Lapse_Mass"]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

        case ChartNames.EXPENSE_RISK:
            title = "Expense Risk"
            x = "Report_Date"
            y = "Expense"
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
            )

        case ChartNames.CATASTROPHE_RISK:
            title = "Catastrophe Risk"
            x = "Report_Date"
            y = "Catastrophe"
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
            )

        case ChartNames.MARKET_RISK:
            title = "Market Risk"
            x = "Report_Date"
            y = "Market_Risk"
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
            )

        case ChartNames.MARKET_RISK_OVERALL:
            title = "Market Risk Overall"
            x = "Report_Date"
            y = [
                "Market_Risk",
                "Interest",
                "Equity",
                "Forex",
                "Property",
                "Concentration",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

        case ChartNames.INTEREST_RISK:
            title = "Interest Risk"
            x = "Report_Date"
            y = [
                "Interest",
                "Interest_RM",
                "Interest_LU",
                "Interest_LD",
                "Interest_Flat",
                "Interest_Slope",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

        case ChartNames.EQUITY_RISK:
            title = "Equity Risk"
            x = "Report_Date"
            y = [
                "Equity",
                "Equity_Developed",
                "Equity_Emerging",
                "Equity_Infra",
                "Equity_Preferred",
                "Equity_Long_Term",
                "Equity_Other",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

        case ChartNames.FOREX_RISK:
            title = "Forex Risk"
            x = "Report_Date"
            y = [
                "Forex",
                "Forex_Up",
                "Forex_Down",
                "Volatility",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

        case ChartNames.PROPERTY_RISK:
            title = "Property Risk"
            x = "Report_Date"
            y = "Property"
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
            )

        case ChartNames.CONCENTRATION_RISK:
            title = "Concentration Risk"
            x = "Report_Date"
            y = [
                "Concentration",
                "Counterparty_Conc",
                "Property_Conc",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

        case ChartNames.CREDIT_RISK:
            template, _ = helpers.get_template_df("credit_risk")
            data = helpers.replace_template_values(template, data, True)
            title = "Credit Risk"
            x = "Category"
            y = [
                "Credit Risk",
                "Risk-free",
                "Public Inst",
                "General Corp",
                "Securitisation",
                "Re-Securitisation",
                "Reinsurance Assets",
                "Other Assets",
                "Commercial",
                "Mortgage",
            ]
            chart = helpers.create_bar_chart(
                df=data,
                x=x,
                y=y,
                title=title,
                color_schema=color_schema,
                barmode="stack",
                pattern_shape="x",
                facet_col="Report_Date",
            )

            chart.update_xaxes(tickangle=-90)
            for annotation in chart.layout.annotations:
                annotation["y"] = -0.46

        case _:
            message = f"Chart name not found: {name}"
            logger.error(message)
            raise ValueError(message)

    if not with_table_data:
        return chart

    table_data = helpers.prepare_table_data(
        data, header_rows=header_rows, multi_index=multi_index
    )
    if isinstance(chart, list):
        return [*chart, *table_data]
    return [chart, *table_data]
