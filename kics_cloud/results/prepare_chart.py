import logging

logger = logging.getLogger(__name__)

import pandas as pd

import cm_dashboards.kics_cloud.helpers as helpers
import cm_dashboards.kics_cloud.results.prepare_data as prepare_data
from cm_dashboards.kics_cloud.results.program_names import (
    ChartNames,
    ColorSchema,
    ProgramNames,
)


def generate(wvr_path, name):
    """
    Helper function to generate bar charts
    :param wvr_path: the path to wvr file(s) (string or kwargs)
    :param name:
    """
    match name:
        case ChartNames.CompanyRisk:
            # Get individual data as they depend on different models
            data_1 = prepare_data.get_data(
                wvr_path, ProgramNames.CompanyLevelLifeRiskTotal
            )
            data_2 = prepare_data.get_data(wvr_path, ProgramNames.CompanyLevelAssetRisk)
            data_3 = prepare_data.get_data(wvr_path, ProgramNames.OperationRiskTotal)

            # Merge results as one dict
            results_as_dict = {
                **data_1.to_dict("list"),
                **data_2.to_dict("list"),
                **data_3.to_dict("list"),
            }

            # Create data frame as desired
            columns = helpers.get_data_structure(name.value)
            df = helpers.set_value(results_as_dict, columns)
            df_rotate = helpers.pivot_df(df, name.value)
            df_rotate.rename(columns={"CompanyRisk": "Risk"}, inplace=True)

            # Create chart and table data
            values, names = ("Data", "Risk")
            color_schema = helpers.set_color_schema(1)
            margin = dict(l=12, r=4, t=44, b=44)
            chart = helpers.create_pie_chart(
                df_rotate,
                values=values,
                names=names,
                color_schema=color_schema,
                margin=margin,
            )
            data, column, style = helpers.prepare_table_data(df_rotate)

            return chart, data, column, style

        case ChartNames.AssetInfo:
            df = prepare_data.get_data(wvr_path, ProgramNames.AssetInfo)
            df.rename(
                columns={"Market_Value": "Market Value", "Asset_Group": "Asset Group"},
                inplace=True,
            )

            # Create chart and table data
            values, names = ("Market Value", "Asset Group")
            color_schema = helpers.set_color_schema(2)
            margin = dict(l=1, r=1, t=42, b=44)
            chart = helpers.create_pie_chart(
                df,
                values=values,
                names=names,
                color_schema=color_schema,
                margin=margin,
            )
            data, column, style = helpers.prepare_table_data(df)

            return chart, data, column, style

        case ChartNames.MarketRisk:
            data = prepare_data.get_data(wvr_path, ProgramNames.MarketRisk)
            results_as_dict = data.to_dict("list")

            # Create data frame as desired
            columns = helpers.get_data_structure(name.value)
            df = helpers.set_value(results_as_dict, columns)
            df_rotate = helpers.pivot_df(df, name.value)
            df_rotate.rename(columns={"MarketRisk": "Market Risk"}, inplace=True)

            # Create chart and table data
            values, names = ("Data", "Market Risk")
            color_schema = helpers.set_color_schema(3)
            chart = helpers.create_pie_chart(
                df_rotate,
                values=values,
                names=names,
                color_schema=color_schema,
            )
            data, column, style = helpers.prepare_table_data(df_rotate)

            return chart, data, column, style

        case ChartNames.LiabilityInfo:
            # Get individual data as they depend on different models
            data_1 = prepare_data.get_data(wvr_path, ProgramNames.ProductLevelLifeRisk)
            data_2 = prepare_data.get_data(
                wvr_path, ProgramNames.ProductLevelLifeRiskTotal
            )

            # Merge results into one dict
            results_as_dict = {
                **data_1.to_dict("list"),
                **data_2.to_dict("list"),
            }

            # Create data frame as desired
            columns = helpers.get_data_structure(name.value)
            df = helpers.set_value(results_as_dict, columns)
            df = df[["Product", "BEL", "Risk_Margin"]]
            df = pd.melt(
                df,
                id_vars=["Product"],
                value_vars=["BEL", "Risk_Margin"],
                var_name="LiabilityInfo",
                value_name="Data",
            )
            # Sort the data and remove duplicates from "Product" column
            df.sort_values("Product", ascending=True, inplace=True)
            df.rename(columns={"Product": "Liability info"}, inplace=True)
            df_plot = df.copy()
            df_plot.loc[df_plot["Liability info"].duplicated(), "Liability info"] = ""

            # Create table data
            data, column, style = helpers.prepare_table_data(df_plot)

            # Adjust data as needed to plot
            df = helpers.calculate_ratio(df)
            df["Liabilities"] = df[["Liability info", "LiabilityInfo"]].apply(
                lambda x: " ".join(x), axis=1
            )
            df["Liability"] = ""

            # Create chart
            title = "Liability Info"
            x = "Data"
            y = "Liability"
            color = "Liabilities"
            color_schema = helpers.set_color_schema(4)
            chart = helpers.create_bar_chart(
                df,
                y=y,
                x=x,
                title=title,
                orientation="h",
                color=color,
                color_schema=color_schema,
                text_color="white",
            )

            return chart, data, column, style

        case ChartNames.ProductInfo:
            # Get individual data as they depend on different models
            data_1 = prepare_data.get_data(
                wvr_path, ProgramNames.ProductLevelLifeRiskTotal
            )
            data_2 = prepare_data.get_data(wvr_path, ProgramNames.ProductLevelAssetRisk)

            # Merge results into one dict
            results_as_dict = {
                **data_1.to_dict("list"),
                **data_2.to_dict("list"),
            }

            # Create data frame as desired
            program_name = name.value
            columns = helpers.get_data_structure(program_name)
            df = helpers.set_value(results_as_dict, columns)
            rename_columns = ["Trad", "UL"]
            df_rotate = helpers.pivot_df(df, program_name, rename_columns)
            df_rotate = df_rotate[df_rotate["ProductInfo"] != "Product"]
            df_rotate.rename(columns={"ProductInfo": ""}, inplace=True)

            # Create table data
            data, column, style = helpers.prepare_table_data(df_rotate)

            # Risk chart
            risk_df = df[["Product", "Credit_Risk", "Market_Risk", "Insurance_Risk"]]
            risk_df = helpers.calculate_ratio(risk_df, axis=1)
            risk_title = "Risk"
            risk_y = ["Insurance_Risk", "Market_Risk", "Credit_Risk"]
            risk_x = "Product"
            color_schema = helpers.set_color_schema(5)
            risk_chart = helpers.create_bar_chart(
                risk_df,
                y=risk_y,
                x=risk_x,
                title=risk_title,
                color_schema=color_schema,
            )

            # Insurance risk chart
            insurance_risk_df = df[
                ["Product", "Expense", "Lapse", "Longevity", "Morbidity", "Mortality"]
            ]
            insurance_risk_df = helpers.calculate_ratio(insurance_risk_df, axis=1)

            insurance_risk_title = "Insurance Risk"
            insurance_risk_y = [
                "Expense",
                "Lapse",
                "Longevity",
                "Morbidity",
                "Mortality",
            ]
            insurance_risk_x = "Product"
            color_schema = helpers.set_color_schema(6)[::-1]
            insurance_risk_chart = helpers.create_bar_chart(
                insurance_risk_df,
                y=insurance_risk_y,
                x=insurance_risk_x,
                title=insurance_risk_title,
                color_schema=color_schema,
                text_color="white",
            )

            # Market risk chart
            market_risk_df = df[
                [
                    "Product",
                    "Interest_Risk",
                    "Equity_Risk",
                    "Concentration_Risk",
                    "Property_Risk",
                    "Forex_Risk",
                ]
            ]
            market_risk_df = helpers.calculate_ratio(market_risk_df, axis=1)

            market_risk_title = "Market Risk"
            market_risk_y = [
                "Interest_Risk",
                "Equity_Risk",
                "Concentration_Risk",
                "Property_Risk",
                "Forex_Risk",
            ]
            market_risk_x = "Product"
            color_schema = helpers.set_color_schema(7)[::-1]
            market_risk_chart = helpers.create_bar_chart(
                market_risk_df,
                y=market_risk_y,
                x=market_risk_x,
                title=market_risk_title,
                color_schema=color_schema,
            )

            return (
                risk_chart,
                insurance_risk_chart,
                market_risk_chart,
                data,
                column,
                style,
            )

        case ChartNames.LiabilityMovement:
            df = prepare_data.get_data(wvr_path, ProgramNames.LiabilityMovement)
            df = df.astype(int, errors="ignore")
            data, column, style = helpers.prepare_table_data(
                df, filter_column_style=["Δ BEL", "Δ RM"]
            )

            # Bel movement chart
            df["Text"] = df["Δ BEL"].apply(lambda x: f"{round(x):,}")
            color_schema = ColorSchema(
                current="#AFCEE3",
                increase="#AFCEE3",
                decrease="#F6D794",
                total="#AFCEE3",
            )
            logger.info("ColorSchema: {}".format(color_schema.current))
            bel_chart = helpers.create_waterfall_chart(
                df,
                x="Name",
                y="Δ BEL",
                text="Text",
                title="BEL Movement",
                color_schema=color_schema,
                dtick=20000,
            )

            # Risk margin movement
            df["Text"] = df["Δ RM"].apply(lambda x: f"{round(x):,}")
            color_schema = ColorSchema(
                current="#AFCEE3",
                increase="#AFCEE3",
                decrease="#F6D794",
                total="#AFCEE3",
            )
            risk_chart = helpers.create_waterfall_chart(
                df,
                x="Name",
                y="Δ RM",
                text="Text",
                title="Risk Margin Movement",
                color_schema=color_schema,
                dtick=500,
            )

            return bel_chart, risk_chart, data, column, style

        case ChartNames.AssetMovement:
            df = prepare_data.get_data(wvr_path, ProgramNames.AssetMovement)
            df = df.astype(int, errors="ignore")
            data, column, style = helpers.prepare_table_data(
                df, filter_column_style=["Δ Asset"]
            )

            # Bel movement chart
            df["Text"] = df["Δ Asset"].apply(lambda x: f"{round(x):,}")
            color_schema = ColorSchema(
                current="#F4D7D0",
                increase="#F4D7D0",
                decrease="#EA8686",
                total="#F4D7D0",
            )
            chart = helpers.create_waterfall_chart(
                df,
                x="Name",
                y="Δ Asset",
                text="Text",
                title="Asset Movement",
                dtick=50000,
                color_schema=color_schema,
            )
            chart.update_yaxes(range=[0, 250000])

            return chart, data, column, style

        case ChartNames.CapitalAndIndividualRisksMovement:
            df = prepare_data.get_data(
                wvr_path, ProgramNames.CapitalAndIndividualRisksMovement
            )
            data_1, column_1, style_1 = helpers.prepare_table_data(
                df[
                    [
                        "Name",
                        "Market_Risk",
                        "Credit_Risk",
                        "Operation_Risk",
                        "Required_Capital",
                    ]
                ]
            )
            data_2, column_2, style_2 = helpers.prepare_table_data(
                df[
                    [
                        "Name",
                        "Interest_Risk",
                        "Equity_Risk",
                        "Concentration_Risk",
                        "Property_Risk",
                        "Forex_Risk",
                    ]
                ]
            )
            data_3, column_3, style_3 = helpers.prepare_table_data(
                df[
                    [
                        "Name",
                        "Expense",
                        "Lapse",
                        "Longevity",
                        "Morbidity",
                        "Mortality",
                    ]
                ]
            )

            # Required Capital
            required_capital_df = df[
                [
                    "Name",
                    "Market_Risk",
                    "Insurance_Risk",
                    "Credit_Risk",
                    "Operation_Risk",
                    "Required_Capital",
                ]
            ]
            title = "Required Capital"
            y = [
                "Operation_Risk",
                "Credit_Risk",
                "Insurance_Risk",
                "Market_Risk",
            ]
            x = "Name"
            line_chart_y = "Required_Capital"
            color_schema = helpers.set_color_schema(8)
            required_capital_chart = helpers.create_mixed_bar_chart(
                required_capital_df,
                y=y,
                x=x,
                title=title,
                line_chart_y=line_chart_y,
                color_schema=color_schema,
                line_color="#99897E",
                dtick=5000,
            )

            required_capital_chart.update_layout(
                margin=dict(l=265, r=265, t=100, b=5),
                legend=dict(orientation="v", x=1.02, y=0.5),
            )

            # Market Risk
            market_risk_df = df[
                [
                    "Name",
                    "Interest_Risk",
                    "Equity_Risk",
                    "Concentration_Risk",
                    "Property_Risk",
                    "Forex_Risk",
                    "Market_Risk",
                ]
            ]
            title = "Market Risk"
            y = [
                "Property_Risk",
                "Interest_Risk",
                "Equity_Risk",
                "Concentration_Risk",
                "Forex_Risk",
            ]
            x = "Name"
            line_chart_y = "Market_Risk"
            color_schema = helpers.set_color_schema(9)
            market_risk_chart = helpers.create_mixed_bar_chart(
                market_risk_df,
                y=y,
                x=x,
                title=title,
                line_chart_y=line_chart_y,
                color_schema=color_schema,
                line_color="rgba(145, 167, 223, 1)",
                dtick=5000,
            )
            market_risk_chart.update_layout(
                title_font=dict(size=14),
                title_x=0.3,
            )

            # Insurance Risk
            insurance_risk_df = df[
                [
                    "Name",
                    "Expense",
                    "Lapse",
                    "Longevity",
                    "Morbidity",
                    "Mortality",
                    "Insurance_Risk",
                ]
            ]
            title = "Insurance Risk"
            y = [
                "Expense",
                "Lapse",
                "Longevity",
                "Morbidity",
                "Mortality",
            ]
            x = "Name"
            line_chart_y = "Insurance_Risk"
            color_schema = helpers.set_color_schema(10)
            insurance_risk_chart = helpers.create_mixed_bar_chart(
                insurance_risk_df,
                y=y,
                x=x,
                title=title,
                line_chart_y=line_chart_y,
                color_schema=color_schema,
                line_color="rgba(39, 65, 188, 1)",
                dtick=2000,
            )
            insurance_risk_chart.update_layout(
                title_font=dict(size=14),
                title_x=0.3,
            )

            return (
                required_capital_chart,
                data_1,
                column_1,
                style_1,
                market_risk_chart,
                data_2,
                column_2,
                style_2,
                insurance_risk_chart,
                data_3,
                column_3,
                style_3,
            )

        case ChartNames.InterestRateSensitivity:
            df = prepare_data.get_data(wvr_path, ProgramNames.InterestRateSensitivity)
            data, column, style = helpers.prepare_table_data(df)

            return data, column, style

        case ChartNames.InsuranceAndMarketRisk:
            # Get DF and generate table data
            df = prepare_data.get_data(wvr_path, ProgramNames.InsuranceAndMarketRisk)
            df = df.astype(int, errors="ignore")
            data, column, style = helpers.prepare_table_data(
                df, filter_column_style=["Δ Insurance_Risk", "Δ Market_Risk"]
            )

            # Color schema for chart
            color_schema = ColorSchema(
                current="#F4D7D0",
                increase="#F4D7D0",
                decrease="#EA8686",
                total="#F4D7D0",
            )

            # Create waterfall chart
            df["Text"] = df["Δ Insurance_Risk"].apply(lambda x: f"{round(x,2):,}")
            insurance_risk_chart = helpers.create_waterfall_chart(
                df,
                x="Name",
                y="Δ Insurance_Risk",
                text="Text",
                title="Insurance Risk Movement",
                color_schema=color_schema,
                dtick=2000,
            )

            df["Text"] = df["Δ Market_Risk"].apply(lambda x: f"{round(x,2):,}")
            market_risk_chart = helpers.create_waterfall_chart(
                df,
                x="Name",
                y="Δ Market_Risk",
                text="Text",
                title="Market Risk Movement",
                color_schema=color_schema,
                dtick=5000,
            )

            return insurance_risk_chart, market_risk_chart, data, column, style

        case ChartNames.RatioMovement:
            df = prepare_data.get_data(wvr_path, ProgramNames.RatioMovement)
            df = df.astype(int, errors="ignore")
            df["KICS_Ratio"] = df["KICS_Ratio"].apply(lambda x: f"{x}%")
            data, column, style = helpers.prepare_table_data(
                df[["Name", "Available_Capital", "Required_Capital", "KICS_Ratio"]]
            )

            # Chart
            df["K-ICS_Ration"] = df["Available_Capital"] + df["Required_Capital"]
            title = "K-ICS Ratio Movement"
            y = [
                "Available_Capital",
                "Required_Capital",
            ]
            x = "Name"
            text = df["KICS_Ratio"]
            line_chart_y = "K-ICS_Ration"
            color_schema = helpers.set_color_schema(11)
            chart = helpers.create_mixed_bar_chart(
                df,
                y=y,
                x=x,
                text=text,
                title=title,
                line_chart_y=line_chart_y,
                color_schema=color_schema,
                line_color="rgba(67, 100, 247, 1)",
                dtick=20000,
                bar_width=0.51,
                y_axis_range=[0, 120000],
                ticksuffix="M",
            )
            # Add custom text on the bar chart
            chart.update_layout(
                margin=dict(l=10, r=30, t=60, b=50),
                legend=dict(
                    orientation="h", y=-0.3, xanchor="center", yanchor="bottom", x=0.5
                ),
                yaxis=dict(
                    title="( 단위: 백만원%)",
                    titlefont_size=10,
                    tickfont_size=12,
                ),
            )
            chart.update_xaxes(tickangle=0, tickfont_size=10.5)

            return chart, data, column, style

        case ChartNames.AvailableCapital:
            df = prepare_data.get_data(wvr_path, ProgramNames.AvailableCapital)
            df = df.astype(int, errors="ignore")
            data, column, style = helpers.prepare_table_data(df)

            df = df[["Name", "Tier_1", "Tier_2"]]
            title = "Available Capital"
            y = [
                "Tier_1",
                "Tier_2",
            ]
            x = "Name"
            color_schema = helpers.set_color_schema(12)
            chart = helpers.create_bar_chart(
                df,
                y=y,
                x=x,
                title=title,
                color_schema=color_schema,
            )

            # Customize chart
            chart.update_layout(
                font_color="#4F4F4F",
                yaxis=dict(
                    title="( 단위: 백만원)",
                    titlefont_size=10,
                    tickfont_size=12,
                    tickfont_color="#333333",
                    ticksuffix="M",
                    exponentformat="none",
                    separatethousands=True,
                    range=[0, 70000],
                    dtick=10000,
                ),
                xaxis=dict(
                    titlefont_size=10,
                    tickfont_size=12,
                    tickfont_color="#333333",
                ),
                margin=dict(l=10, r=30, t=60, b=50),
                legend=dict(
                    orientation="h", y=-0.3, xanchor="center", yanchor="bottom", x=0.5
                ),
            )

            # Hide text on the bar chart
            chart.update_traces(width=0.22, textposition="none")

            return chart, data, column, style

        case ChartNames.TierOne:
            df = prepare_data.get_data(wvr_path, ProgramNames.TierOne)
            df = df.astype(int, errors="ignore")
            data, column, style = helpers.prepare_table_data(
                df, filter_column_style=["Tier_1"]
            )

            # Color schema for chart
            color_schema = ColorSchema(
                current="#B4C1ED",
                increase="#B4C1ED",
                decrease="#F6D794",
                total="#B4C1ED",
            )

            # Create waterfall chart
            df["Text"] = df["Tier_1"].apply(lambda x: f"{round(x,1):,}")
            measure = ["relative", "relative", "relative", "total"]
            chart = helpers.create_waterfall_chart(
                df,
                x="Name",
                y="Tier_1",
                text="Text",
                title="Tier 1",
                color_schema=color_schema,
                dtick=10000,
                measure=measure,
            )

            chart.update_traces(width=0.425)

            return chart, data, column, style

        case ChartNames.TierTwo:
            df = prepare_data.get_data(wvr_path, ProgramNames.TierTwo)
            df_table = df.copy()
            df_table = df_table.rename(columns={"Δ Tier_2": " "})

            data, column, style = helpers.prepare_table_data(
                df_table, filter_column_style=[""]
            )

            # Color schema for chart
            color_schema = ColorSchema(
                current="#B4C1ED",
                increase="#B4C1ED",
                decrease="#F6D794",
                total="#B4C1ED",
            )

            # Create waterfall chart
            df["Text"] = df["Δ Tier_2"].apply(lambda x: f"{round(x,1):,}")
            measure = ["relative", "relative", "relative", "total"]
            chart = helpers.create_waterfall_chart(
                df,
                x="Name",
                y="Δ Tier_2",
                text="Text",
                title="Tier 2",
                color_schema=color_schema,
                dtick=500,
                measure=measure,
            )

            chart.update_traces(width=0.425)

            return chart, data, column, style

        case _:
            return
