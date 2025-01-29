"""
Author: Kamoliddin Usmonov
Date: 2022-12-29
Description: Helper functions for KICS dashboards
"""

import logging

logger = logging.getLogger(__name__)

import datetime
from typing import Type

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import cm_dashboards.ifrs17_accounting.dash_utils as dash_utils
from cm_dashboards.kics_cloud.abstract_handler import GenericHandler
from cm_dashboards.kics_cloud.results.program_names import ChartNames, ColorSchema


def get_df(handler: GenericHandler, wvr_path: str, model_name: str) -> pd.DataFrame:
    """
    Get table data from wvr
    :param handler: DB handler
    :param wvr_path: path to wvr file
    :return: DataFrame
    """
    df = handler.get_wvr_data(wvr_path, model_name)
    return df


def prepare_table_data(
    df: pd.DataFrame,
    header_rows: list[int] = [],
    hidden_columns: list[str] = [],
    filter_column_style: list | str = None,
    additional_header: list[str] = [],
    replace_zero: str = None,
    multi_index: bool = False,
    show_negative_numbers: bool = True,
) -> tuple:
    """
    Prepare table data
    :param df: DataFrame
    :param header_rows: list of header rows
    :param hidden_columns: list of hidden columns
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Check if replacement is needed
    if replace_zero is not None:
        df = df.replace({0: replace_zero})

    # Set multiindex table data, column if needed
    if multi_index:
        table_data, columns = dash_utils.set_multi_index_column_names(
            df, show_negative_numbers=show_negative_numbers
        )
    else:
        table_data = df.to_dict("records")
        table_columns = df.columns
        columns = dash_utils.set_column_names(
            table_columns,
            precision=0,
            hidden_columns=hidden_columns,
            show_negative_numbers=show_negative_numbers,
            additional_header=additional_header,
        )
    conditional_style = dash_utils.set_table_style_kics(
        columns, show_negative_numbers=show_negative_numbers
    )
    row_style = dash_utils.set_row_style(header_rows)
    style = conditional_style + row_style

    # Add conditional style for filter column
    if filter_column_style is not None:
        result = dash_utils.set_conditional_style_by_filtering(
            column=filter_column_style
        )
        style = style + result

    return table_data, columns, style


def calculate_ratio(df: pd.DataFrame, axis: int = 0) -> pd.DataFrame:
    """
    Helper function to calculate proportaion ratio
    """
    details = {key: list() for key in df.columns.values.tolist()}
    total_sum = df.sum(numeric_only=True, axis=axis).to_dict()
    # logger.info("Total sum: {}".format(total_sum))

    # Loop throught each row and calculate proportion ration per column
    for index, row in df.iterrows():
        row_as_dict = row.to_dict()
        for column, value in row_as_dict.items():
            # Do not calculate ratio if value is 0
            if isinstance(value, str) or value == 0:
                details[column].append(value)
                continue

            # Calculate proportion ratio
            column_or_index = column if axis == 0 else index
            ratio = round(value / total_sum[column_or_index], 2) * 100
            details[column].append(ratio)

    result = pd.DataFrame(details)
    return result


def get_data_structure(figure_name: str) -> list[str]:
    """
    Return predefined data structure per figure name to create desired data
    """
    structures = {
        ChartNames.CompanyRisk.value: [
            "Insurance_Risk",
            "Market_Risk",
            "Credit_Risk",
            "Operation_Risk",
        ],
        ChartNames.MarketRisk.value: [
            "Interest_Risk",
            "Equity_Risk",
            "Concentration_Risk",
            "Property_Risk",
            "Forex_Risk",
        ],
        ChartNames.LiabilityInfo.value: ["BEL", "Risk_Margin", "Product"],
        ChartNames.ProductInfo.value: [
            "Insurance_Risk",
            "Expense",
            "Lapse",
            "Longevity",
            "Morbidity",
            "Mortality",
            "Market_Risk",
            "Interest_Risk",
            "Equity_Risk",
            "Concentration_Risk",
            "Property_Risk",
            "Forex_Risk",
            "Credit_Risk",
            "Product",
        ],
        ChartNames.LiabilityMovement.value: [
            "Previous",
            "Voulme Update",
            "Actuarial Assumption Update",
            "Economic Assumption Update",
            "Current",
        ],
        ChartNames.AssetMovement.value: [
            "Previous",
            "Voulme Update",
            "Actuarial Assumption Update",
            "Economic Assumption Update",
            "Current",
        ],
        ChartNames.InsuranceAndMarketRisk.value: [
            "Previous",
            "Voulme Update",
            "Actuarial Assumption Update",
            "Economic Assumption Update",
            "Current",
        ],
        ChartNames.RatioMovement.value: [
            "Previous",
            "Voulme Update",
            "Actuarial Assumption Update",
            "Economic Assumption Update",
            "Current",
        ],
        ChartNames.CapitalAndIndividualRisksMovement.value: [
            "Previous",
            "Current",
        ],
        ChartNames.AvailableCapital.value: [
            "Previous",
            "Current",
        ],
        ChartNames.TierTwo.value: [
            "Previous",
            "Issue & Deduction",
            "Economic Assumption update",
            "Current",
        ],
        ChartNames.TierOne.value: [
            "Previous",
            "BS adjustment",
            "Capital adjustment",
            "Current",
        ],
    }

    return structures.get(figure_name)


def set_value(result_dict: dict, fields: list) -> pd.DataFrame:
    """
    Loop up value from results dict and set value if exits
    """
    result = dict()
    for field in fields:
        value = result_dict.get(field, "")
        # Save the value
        logger.info("{} value: {}".format(field, value))
        result[field] = value

    # logger.info("Final result: {}".format(result))
    df = pd.DataFrame(result)

    # # Check if more than one row
    # if len(df.index) > 1:
    #     df.index.names = ["Product"]

    return df


def pivot_df(
    df: pd.DataFrame, hader_name: str, column_names: list = ["Data", "Data_2"]
) -> pd.DataFrame:
    """
    Helper function to rotate the df
    :param df: the df to rotate
    :param result: rotated result
    """
    # Rotate DF
    df = df.reset_index(drop=True).transpose()

    # # Make the first row as header row
    # df.columns = df.iloc[0]
    # df = df[1:]

    # Convert datetime object to string in column names
    df.rename(
        columns=lambda t: t.strftime("%Y-%m-%d") if isinstance(t, datetime.date) else t,
        inplace=True,
    )

    # Reset index, rename 'index' column name
    df.reset_index(inplace=True)
    df.rename(
        columns={"index": hader_name, 0: column_names[0], 1: column_names[1]},
        inplace=True,
    )

    return df


def set_color_schema(unit_number: int) -> list:
    """
    Retrive color schema for chart type specified
    """
    color_schema = {
        1: ["#D5DAFB", "#B1BAFD", "#6E84FE", "#8698FB"],
        2: ["#ADD5D7", "#9CB7A8"],
        3: ["#F6D794", "#F6B1C3", "#A47DA0", "#E5F0F6", "#ADD5D7", "#E5F0F6"],
        4: ["#D3DCFC", "#6E84FE", "#8698FB", "#B1BAFD"],
        5: ["#F8AA7C", "#ADD5D7", "#F6D794"],
        6: ["#D5DAFB", "#B1BAFD", "#8698FB", "#56CCF2", "#6E84FE"],
        7: ["#F6D794", "#D5DAFB", "#A47DA0", "#ADD5D7", "#F8AA7C"],
        8: ["#C89D8D", "#EAB8B1", "#8698FB", "#F6D794"],
        9: ["#2D9CDB", "#EAB8B1", "#F6D794", "#E0E0E0", "#C89D8D"],
        10: ["#6E84FE", "#2741BC", "#8698FB", "#B1BAFD", "#D5DAFB"],
        11: ["#AFCEE3", "#F6D794"],
        12: ["#B4C1ED", "#F6D794"],
    }

    return color_schema.get(unit_number, None)


def add_column(
    df: pd.DataFrame, values: list, column_name: str = "Name", index: int = 0
) -> pd.DataFrame:
    """
    Add name column
    :param df: DataFrame to add column (DataFrame)
    :param values: List of column values (list of strings)
    :param column_name: Name of column (str) (optional)
    :param index: Index of column to insert (int) (optional)
    :return df: result of add column operation (DataFrame)
    """
    df.insert(index, column_name, values)
    return df


def calculate_difference(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the difference between rows per column as requested
    """
    columns = df.columns.values.tolist()
    # Get the column names

    # Iterate over each row and calculate the operation
    for index, current_row in df.iterrows():
        for i, column in enumerate(columns):
            try:
                # Skip calculation for the first and last rows
                if index == 0 or index == (len(df.index) - 1):
                    difference = current_row[column]
                else:
                    # Calculate the difference between current and previous row
                    previous_row = df.loc[index - 1]
                    difference = current_row[column] - previous_row[column]

                # Append the result
                new_column = f"Δ {column}"
                df.loc[index, new_column] = difference
            except Exception as e:
                print(f"Error: {e}")

    return df


def join_dfs(dfs_list: list[pd.DataFrame], axis: int = 0) -> pd.DataFrame:
    """
    Join a list of DF and make as unified
    """
    result = pd.concat(dfs_list, axis=axis)
    result.reset_index(inplace=True, drop=True)
    return result


def calc_ratio(x, y):
    result = f"{round((x - y) / y, 2) * 100}%"
    logger.info("Result: {}".format(result))
    return result


def create_mixed_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: list[str] | str,
    title: str,
    line_chart_y: str,
    text: str = None,
    orientation: str = "v",
    barmode: str = "stack",
    color: str = None,
    color_schema: str = None,
    line_color: str = "blue",
    dtick: int = 1000,
    bar_width: float = 0.43,
    bar_text_color: str = "rgba(255,255,255,0)",
    y_axis_range: list[int] = None,
    ticksuffix: str = None,
) -> go.Figure:
    """
    Create bar chart object
    :param df: data to be used for chart creation
    :param x: X-axis data
    :param y: Y-axis data
    :param title: Title of the chart
    :param orientation: Orientation of the chart "h" or "v" (horizontal or vertical) (optional)
    :param color: Color of the chart (optional)
    :param color_schema: List of colors for the chart (optional)
    :param line_color: Color of the line chart (optional)
    :return chart: chart object
    """
    # Create chart object
    chart = px.bar(
        data_frame=df,
        x=x,
        y=y,
        title=title,
        color=color,
        text_auto=True,
        orientation=orientation,
        barmode=barmode,
        color_discrete_sequence=color_schema,
        labels=dict(
            value="", variable="", Product="", Data="", Liabilities="", Name=""
        ),
    )

    # Update the chart margin, title, and legend positioning
    chart.update_layout(
        margin=dict(l=0, r=0, t=80, b=0),
        title_text=title,
        title_x=0.5,
        title_font_size=14,
        legend=dict(orientation="v", x=1.02, y=0.5),
    )

    # Add border line to the paper
    chart.update_xaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)
    chart.update_yaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)

    # Update font size, hover template, marker sizez
    chart.update_traces(
        width=bar_width,
        textposition="inside",
        textfont_size=12,
        insidetextanchor="middle",
        marker_line_width=0,
        selector=dict(type="bar"),
        textfont=dict(family="sans serif 'Nunito Sans'", size=14, color=bar_text_color),
        hovertemplate="%{x}: %{y}",
    )

    # Update y-axis labels
    chart.update_yaxes(
        showline=True,
        exponentformat="none",
        separatethousands=True,
        dtick=dtick,
        ticksuffix=ticksuffix,
    )

    # Update y-axis range
    if y_axis_range is not None:
        chart.update_yaxes(
            range=y_axis_range,
        )

    # Add line chart trace with given data and color
    line_chart_trace = px.line(
        df,
        x=x,
        y=line_chart_y,
        color_discrete_sequence=[line_color],
        markers=True,
    ).data[0]

    # Update line chart trace, marker, mode, text, textfont, textposition, showlegend, and name
    # line_chart_trace["marker"]["symbol"] = ["circle", "circle-open"]
    line_chart_trace["mode"] = "lines+markers+text"
    line_chart_trace["text"] = text
    line_chart_trace["textfont"] = dict(size=10, color="#000000")
    line_chart_trace["textposition"] = "top center"
    line_chart_trace["showlegend"] = True
    line_chart_trace["name"] = line_chart_y
    chart.add_trace(line_chart_trace)
    chart.update_layout(legend=dict(itemsizing="trace", itemwidth=30))

    return chart


def create_waterfall_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    text: str,
    title: str,
    color_schema: Type[ColorSchema],
    dtick: int = 20000,
    measure: list[str] = ["relative", "relative", "relative", "relative", "total"],
) -> go.Figure:
    """
    Create a waterfall chart
    :param df: DataFrame to plot
    :param x: X-axis data point
    :param y: Y-axis data point
    :text: List of text to plot as label
    :dtick: Y-axis range to draw the ticks (optional)
    :param color_schema: Defined color scheme to use (ColorSchema)
    """
    max_y = df[y].max()
    y_axis_range = [0, max_y + dtick]
    chart = go.Figure()
    chart.add_trace(
        go.Waterfall(
            x=df[x],
            y=df[y],
            text=df[text],
            measure=measure,
            textposition="outside",
            connector=dict(
                mode="between",
                line=dict(width=1, color=color_schema.connector, dash="dot"),
            ),
            decreasing=dict(
                marker=dict(
                    color=color_schema.decrease,
                    line=dict(width=2, color=color_schema.decrease),
                ),
            ),
            increasing=dict(marker=dict(color=color_schema.increase)),
            totals=dict(marker=dict(color=color_schema.total)),
        )
    )
    chart.update_xaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)
    chart.update_yaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)

    chart.update_layout(
        margin=dict(l=30, r=30, t=60, b=60),
        font_color="#4F4F4F",
        title_text=title,
        title_x=0.5,
        title_font_size=14,
        title_font_family="Arial",
        yaxis=dict(
            title="( 단위: 백만원)",
            titlefont_size=10,
            tickfont_size=12,
        ),
    )

    chart.update_traces(
        width=0.54,
        textposition="outside",
        textfont_size=12,
    )
    chart.update_yaxes(
        visible=True,
        showticklabels=True,
        showgrid=True,
        ticksuffix="M",
        exponentformat="none",
        separatethousands=True,
        range=y_axis_range,
        dtick=dtick,
    )
    chart.update_xaxes(tickangle=0, tickfont_size=10.5)

    return chart


def create_pie_chart(df, names: str, values: str, color_schema: dict, margin=None):
    """
    Create pie chart object
    :param df: data to be used for chart creation
    :param names: Data names to be used for chart creation
    :param values: Data values to be used for chart creation
    :param title: Title of the chart
    :param color_schema: List of color values
    :param margin: Margin to be used to update the chart (optional)
    :return chart: chart object
    """
    # Default margin
    if margin is None:
        margin = dict(l=1, r=1, t=1, b=1)

    chart = px.pie(
        data_frame=df,
        names=names,
        values=values,
        color_discrete_sequence=color_schema,
    )
    chart.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(family="sans serif 'Nunito Sans'", size=13, color="white"),
        hovertemplate="%{label} <br>Percentage: %{percent} </br>Value: %{value:,}",
    )

    # Update legend position
    chart.update_layout(margin=margin, legend=dict(orientation="v", x=1.2, y=0.5))
    return chart


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: list[str] | str,
    title: str,
    orientation: str = "v",
    barmode: str = "stack",
    color: str = None,
    color_schema: str = None,
    text_color: str = "#4F4F4F",
) -> go.Figure:
    """
    Create bar chart object
    :param df: data to be used for chart creation
    :param x: X-axis data
    :param y: Y-axis data
    :param title: Title of the chart
    :param orientation: Orientation of the chart "h" or "v" (horizontal or vertical) (optional)
    :param barmode: Barmode of the chart (default "stack") (optional)
    :param color: Color of the chart (optional)
    :param color_schema: List of colors for the chart (optional)
    :param text_color: Annotation text color (optional)
    :return chart: chart object
    """
    # Create chart object
    chart = px.bar(
        data_frame=df,
        x=x,
        y=y,
        color=color,
        text_auto=True,
        orientation=orientation,
        barmode=barmode,
        color_discrete_sequence=color_schema,
        labels=dict(
            value="",
            variable="",
            Product="",
            Data="",
            Liabilities="",
            Liability="",
            Name="",
        ),
    )

    chart.update_layout(
        bargap=0,
        bargroupgap=0,
        margin=dict(l=5, r=5, t=25, b=5),
    )
    chart.update_traces(
        marker_line_width=0,
        selector=dict(type="bar"),
        textfont=dict(family="sans serif 'Nunito Sans'", size=16, color=text_color),
        hovertemplate="%{x}: %{y}",
    )
    chart.update_xaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)
    chart.update_yaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)

    # Hide text if its size is smaller
    chart.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")

    # Adjust chart parameters to fit, apply different ones depending on the orientation type
    if orientation == "v":
        chart.update_traces(
            width=0.35,
            texttemplate="%{y:f}%",
            textposition="inside",
            textfont_size=12,
            insidetextanchor="middle",
        )

        # Update legend position
        chart.update_layout(
            yaxis_ticksuffix="%",
            title_text=title,
            title_x=0.5,
            legend=dict(
                orientation="v", y=-0.6, xanchor="center", yanchor="bottom", x=0.2
            ),
        )  # yanchor="bottom" y=-1.1, xanchor="left", x=0

        # Set Y-axis range
        chart.update_yaxes(
            visible=True,
            showticklabels=True,
            showgrid=True,
            range=[0, 100],
            tickmode="linear",
            dtick=10,
        )

    else:
        chart.update_traces(
            width=0.55,
            texttemplate="%{x:f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont_size=12,
        )
        chart.update_layout(
            xaxis_ticksuffix="%", legend=dict(orientation="v", x=1.2, y=0.5)
        )

        # Set Y-axis range
        chart.update_xaxes(
            showgrid=True,
            range=[0, 100],
            tickmode="linear",
            dtick=20,
        )

    return chart
