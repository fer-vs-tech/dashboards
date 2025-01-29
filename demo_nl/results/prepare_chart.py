import logging

logger = logging.getLogger(__name__)

import pandas as pd
import plotly.graph_objects as go

import cm_dashboards.orsa.utils.helpers as helpers
from cm_dashboards.orsa.results.prepare_data import get_data
from cm_dashboards.orsa.results.program_names import ChartNames, ProgramNames


def generate(
    wvr_files, name, prepared_data=None, with_table_data=False, hide_title=False
):
    """
    Helper function to generate bar charts
    :param wvr_files: dict of WVR paths
    :param name: chart name (Enum)
    :param prepared_data: dict of prepared data
    """
    color_schema = helpers.set_color_schema(name)

    match name:
        case ChartNames.Schema:
            table_data = get_data(
                wvr_files, ProgramNames.Schema, return_table_data=True
            )
            return table_data

        case ChartNames.FutureBSProjection:
            header_rows = [0, 7, 14, 21, 28, 35, 42, 49]
            prepared_data = helpers.convert_df(prepared_data, to_dict=False)
            table_data = helpers.prepare_table_data(
                prepared_data, multi_index=True, header_rows=header_rows
            )
            return table_data

        case ChartNames.CatastropheRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Catastrophe Risk",
                x="Report_Date",
                y="Catastrophe",
                color_schema=color_schema,
            )
            return chart

        case ChartNames.ExpenseRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Expense Risk",
                x="Report_Date",
                y="Expense",
                color_schema=color_schema,
            )
            return chart

        case ChartNames.LongevityRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Longevity Risk",
                x="Report_Date",
                y="Longevity",
                color_schema=color_schema,
            )
            return chart

        case ChartNames.MorbidityRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Morbidity Risk",
                x="Report_Date",
                y="Morbidity",
                color_schema=color_schema,
            )
            return chart

        case ChartNames.MortalityRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Mortality Risk",
                x="Report_Date",
                y="Mortality",
                color_schema=color_schema,
            )
            return chart

        case ChartNames.LapseRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Lapse Risk",
                x="Report_Date",
                y=["Lapse_Up", "Lapse_Down", "Lapse_Mass", "Lapse"],
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

            return chart

        case ChartNames.EquityRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Equity Risk",
                x="Report_Date",
                y=["Equity_Type_1_General", "Equity_Type_2_General", "Equity"],
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

            return chart

        case ChartNames.InterestRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Interest Risk",
                x="Report_Date",
                y=["Interest_Up", "Interest_Down", "Interest"],
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

            return chart

        case ChartNames.PropertyRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Property Risk",
                x="Report_Date",
                y="Property",
                color_schema=color_schema,
            )

            return chart

        case ChartNames.CurrencyRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Currency Risk",
                x="Report_Date",
                y=["Fx_Up", "Fx_Down", "Fx"],
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

            return chart

        case ChartNames.SpreadRisk:
            chart = helpers.create_bar_chart(
                prepared_data,
                title="Spread Risk",
                x="Report_Date",
                y=[
                    "Spread_Bond_Infra_Corp",
                    "Spread_Bond_Infra_Invest",
                    "Spread_Bond_No_Infra",
                    "Spread",
                ],
                color_schema=color_schema,
                barmode="group",
                pattern_shape="x",
            )

            return chart

        case ChartNames.ProjectedLifeInsuranceRiskAgg:
            # Prepare table data
            needed_columns = [
                "Report_Date",
                "Equity",
                "Interest",
                "Property",
                "Spread",
                "Fx",
                "Market_Risk",
            ]
            filtered_df = prepared_data[needed_columns]
            table_data = helpers.prepare_table_data(filtered_df, multi_index=False)

            # Create chart
            chart = helpers.create_bar_chart(
                filtered_df,
                title="Market Risk (Projected)",
                x="Report_Date",
                y="Market_Risk",
                color_schema=color_schema,
            )

            return chart, *table_data

        case ChartNames.LifeInsuranceRiskAgg:
            # Prepare table data
            needed_columns = [
                "Report_Date",
                "Mortality",
                "Morbidity",
                "Longevity",
                "Lapse",
                "Expense",
                "Catastrophe",
                "Life_Insurance_Risk",
            ]
            filtered_df = prepared_data[needed_columns]
            filtered_df = filtered_df.apply(
                lambda cell: cell.map(
                    lambda x: 0 if (isinstance(x, (int, float)) and x < 0) else x
                ),
                axis=0,
            )
            table_data = helpers.prepare_table_data(filtered_df, multi_index=False)

            # Create chart
            chart = helpers.create_bar_chart(
                filtered_df,
                title="Life Insurance Risk (Projected)",
                x="Report_Date",
                y="Life_Insurance_Risk",
                color_schema=color_schema,
            )

            return chart, *table_data

        case ChartNames.BalanceSheet:
            df = get_data(wvr_files, ProgramNames.BalanceSheet)
            title = "Balance Sheet"
            y = [
                "Assets",
                "BE Liabilities",
                "Risk_Margin",
                "MCR",
                "SCR (in excess of MCR)",
            ]
            x = ""
            chart = helpers.create_bar_chart(
                df,
                y=y,
                x=x,
                title=title,
                color_schema=color_schema,
                hide_title=hide_title,
            )

            # Update width of trace
            width = 0.4
            if with_table_data:
                width = 0.25
            chart.update_traces(width=width)
            chart.update_layout(bargap=0, width=500)

            if with_table_data:
                table_data = helpers.prepare_table_data(df)
                return chart, *table_data
            return chart

        case ChartNames.RiskDistribution:
            df = get_data(wvr_files, ProgramNames.RiskDistribution)

            # Create chart and table data
            values, names = ("Risk amount", "Contents")
            chart = helpers.create_pie_chart(
                df,
                values=values,
                names=names,
                color_schema=color_schema,
                text_size=13.5,
            )

            if hide_title:
                chart.update_layout(
                    legend=dict(orientation="v", x=1.1, y=0.5),
                )

            if with_table_data:
                table_data = helpers.prepare_table_data(df)
                return chart, *table_data
            return chart

        case ChartNames.MarketRiskDistribution:
            df = get_data(wvr_files, ProgramNames.MarketRiskDistribution)

            # Create chart and table data
            values, names = ("Risk amount", "Contents")
            chart = helpers.create_pie_chart(
                df,
                values=values,
                names=names,
                color_schema=color_schema,
            )

            if hide_title:
                chart.update_layout(
                    legend=dict(orientation="v", x=1.08, y=0.5),
                )

            if with_table_data:
                table_data = helpers.prepare_table_data(df)
                return chart, *table_data
            return chart

        case ChartNames.LifeInsuranceRiskDistribution:
            df = get_data(wvr_files, ProgramNames.LifeInsuranceRiskDistribution)

            # Create chart and table data
            values, names = ("Risk amount", "Contents")
            chart = helpers.create_pie_chart(
                df,
                values=values,
                names=names,
                color_schema=color_schema,
            )

            if hide_title:
                chart.update_layout(
                    legend=dict(orientation="v", x=1.08, y=0.5),
                )

            if with_table_data:
                table_data = helpers.prepare_table_data(df)
                return chart, *table_data
            return chart

        case ChartNames.AssetPortfolio:
            df = get_data(wvr_files, ProgramNames.AssetMV)

            # FIlter out unwanted rows
            df = df[df["Assets_Total"].isin(["Bond", "Cash", "Equity", "Property"])]

            # Create chart and table data
            names = "Assets_Total"
            chart = helpers.create_grid_of_pie_charts(
                df,
                names,
                color_schema,
            )

            if with_table_data:
                table_data = helpers.prepare_table_data(df)
                return chart, *table_data
            return chart

        case ChartNames.AssetMV:
            # Get prepared data and generate table data
            df = get_data(wvr_files, ProgramNames.AssetMV)
            if with_table_data:
                table_data = helpers.prepare_table_data(df)

            # Filter out unwanted rows and do needed transformations
            df = df[df["Assets_Total"].isin(["Bond", "Cash", "Equity", "Property"])]
            df_ratios = df.apply(helpers.calc_ratio)

            # Pivot data for chart creation
            df = helpers.pivot_df(df, "Assets_Total", "Assets_Total")
            df_ratios = helpers.pivot_df(df_ratios, "Assets_Total", "Assets_Total")

            # Create chart
            title = "Asset MV"
            text_size = 9.4
            if with_table_data:
                text_size = 11
            chart = go.Figure(
                data=[
                    go.Bar(
                        name="Property",
                        x=df["Assets_Total"],
                        y=df["Property"],
                        text=df_ratios["Property"],
                        marker_color=color_schema[3],
                    ),
                    go.Bar(
                        name="Equity",
                        x=df["Assets_Total"],
                        y=df["Equity"],
                        text=df_ratios["Equity"],
                        marker_color=color_schema[2],
                    ),
                    go.Bar(
                        name="Cash",
                        x=df["Assets_Total"],
                        y=df["Cash"],
                        text=df_ratios["Cash"],
                        marker_color=color_schema[1],
                    ),
                    go.Bar(
                        name="Bond",
                        x=df["Assets_Total"],
                        y=df["Bond"],
                        text=df_ratios["Bond"],
                        marker_color=color_schema[0],
                    ),
                ]
            )

            chart.update_traces(
                textfont=dict(size=text_size, color="#000000"),
                texttemplate="%{text:.2%}",
                textposition="inside",
                insidetextanchor="middle",
                hovertemplate="<br>Value: %{y}<br>Percentage: %{text:.2%}<extra></extra>",
                selector=dict(type="bar"),
            )
            chart.update_xaxes(
                showline=True,
                linewidth=1.2,
                linecolor="#E0E0E0",
                mirror=True,
            )
            chart.update_yaxes(
                showline=True,
                linewidth=1.2,
                linecolor="#E0E0E0",
                mirror=True,
                visible=True,
                showticklabels=True,
                showgrid=True,
                tickprefix="",
                tickformat=",.0f",
                ticksuffix="",
            )

            # Hide text if its size is smaller
            chart.update_layout(
                margin=dict(l=5, r=5, t=25, b=5),
                barmode="stack",
                bargap=0.45,
                legend=dict(orientation="v", y=0.5),
                xaxis_tickmode="array",
                xaxis_tickangle=0,
                xaxis_tickvals=df["Assets_Total"],
                xaxis_tickformat="%Y",
                dragmode=False,
            )

            # Hide title if needed
            if not hide_title:
                chart.update_layout(
                    title=dict(
                        text=title,
                        font=dict(family="Arial", size=16, color="#4F4F4F"),
                        x=0.5,
                        y=0.99,
                    ),
                )

                # Add annotations
                chart.update_layout(
                    margin=dict(t=60, r=30, b=30, l=30),
                    annotations=[
                        dict(
                            text="(2018-12-31 기준, 단위 : 10만원)",
                            x=1,
                            y=1.08,
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(family="Arial", size=12, color="#828282"),
                        )
                    ],
                )
            else:
                # Add annotations
                chart.update_layout(
                    margin=dict(t=30, b=43, r=10, l=10),
                    annotations=[
                        dict(
                            text="(2018-12-31 기준, 단위 : 10만원)",
                            x=1,
                            y=1.08,
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(family="Arial", size=12, color="#828282"),
                        )
                    ],
                )

            # Remove white line from stacked bars
            chart.update_traces(marker_line_width=0, selector=dict(type="bar"))

            if with_table_data:
                return chart, *table_data
            return chart

        case ChartNames.MarketRiskProjection:
            needed_columns = [
                "Report_Date",
                "Equity",
                "Interest",
                "Property",
                "Spread",
                "Fx",
                "Market_Risk",
            ]
            filtered_df = prepared_data[needed_columns]

            # Create chart
            chart = helpers.create_bar_chart(
                filtered_df,
                title="Market Risk (Projected)",
                x="Report_Date",
                y="Market_Risk",
                color_schema=color_schema,
                hide_title=hide_title,
            )

            return chart

        case ChartNames.LifeInsuranceRiskProjection:
            needed_columns = [
                "Report_Date",
                "Mortality",
                "Morbidity",
                "Longevity",
                "Lapse",
                "Expense",
                "Catastrophe",
                "Life_Insurance_Risk",
            ]
            filtered_df = prepared_data[needed_columns]
            filtered_df = filtered_df.apply(
                lambda cell: cell.map(
                    lambda x: 0 if (isinstance(x, (int, float)) and x < 0) else x
                ),
                axis=0,
            )

            # Create chart
            chart = helpers.create_bar_chart(
                filtered_df,
                title="Life Insurance Risk (Projected)",
                x="Report_Date",
                y="Life_Insurance_Risk",
                color_schema=color_schema,
                hide_title=hide_title,
            )

            return chart

        case ChartNames.SolvencyResults:
            result = get_data(
                wvr_files, ProgramNames.SolvencyResults, return_table_data=True
            )
            return result

        case _:
            logger.error(f"Chart name {name} not found")
            raise ValueError(f"Chart name {name} not found")



def get_chart(wvr_path, title):
    """
    Generic line chart using supplied model field name
    """
    handler = db_helper.ClaimCostsResults()
    chart_data_df = handler.get_wvr_data(wvr_path, "NL_LIC_Model")
    # print(chart_data_df)

    try:
        chart = init_chart(title, chart_data_df, "Claim_Paid_By_Origin")
    except:
        # A dash initialisation bug requires this double init
        chart = init_chart(title, chart_data_df, "Claim_Paid_By_Origin")
    for bar in chart.data:
        bar.width = 0.5

    # Add sum of rows
    chart_data_df.loc[:, "Total"] = chart_data_df.drop("Origin_Period_Position", 1).sum(
        numeric_only=True, axis=1
    )
    chart_data_df.loc["Total"] = chart_data_df.set_index("Origin_Period_Position").sum(
        numeric_only=True, axis=0
    )
    chart_data_df.iloc[
        -1, chart_data_df.columns.get_loc("Origin_Period_Position")
    ] = "Total"

    table_data = chart_data_df.to_dict("records")
    columns = dash_utils.set_column_names(chart_data_df.columns, precision=0)
    conditional_style = dash_utils.set_conditional_style(columns)

    return chart, table_data, columns, conditional_style