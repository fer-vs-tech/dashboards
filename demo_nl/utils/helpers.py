import logging

logger = logging.getLogger(__name__)

import ast
import datetime
import math
import os
import statistics
from typing import Type

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import cm_dashboards.ifrs17_accounting.dash_utils as dash_utils
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.demo_nl.results.program_names import ChartNames
from cm_dashboards.demo_nl.utils.abstract_handler import GenericHandler

def dashboards_list():
    """
    Return list of dashboards
    """
    return {
        "dashboard_1": {
            "header": [0, 1, 2],
            "header_rows": [0, 1, 2],
            "label": "miau",
        },
    }



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


def pivot_df(df):
    """
    Helper function to rotate the df
    :param df: the df to rotate
    :param result: rotated result
    """
    # Rotate DF
    df = df.reset_index(drop=True).transpose()

    # Convert datetime object to string in column names
    df.rename(
        columns=lambda t: str(t),
        inplace=True,
    )

    # Reset index, rename 'index' column name
    df.reset_index(inplace=True)
    # df.rename(
    #     columns={"index": hader_name, 0: column_names[0], 1: column_names[1]},
    #     inplace=True,
    # )

    return df


def set_color_schema(chart_name):
    """
    Retrive color schema for chart type specified
    """
    color_schema = {
        ChartNames.ProjectedMarketRisk: ["#ADD5D7", "#9CB7A8"],
        ChartNames.CatastropheRisk: ["#AFCEE3"],
        ChartNames.ExpenseRisk: ["#D5DAFB"],
        ChartNames.LongevityRisk: ["#FFEFD7"],
        ChartNames.MorbidityRisk: ["#FFE6EA"],
        ChartNames.MortalityRisk: ["#E0F6F4"],
        ChartNames.LapseRisk: ["#F6ECED", "#E9CF8F", "#CEB8DE", "#6C7BC0"],
        ChartNames.EquityRisk: ["#C79ECF", "#C8E4FE", "#A5AEFF"],
        ChartNames.InterestRisk: ["#EAE7E7", "#FAB2AC", "#EDA1C1"],
        ChartNames.PropertyRisk: ["#AFCEE3"],
        ChartNames.CurrencyRisk: ["#EAE7E7", "#76B39D", "#155E63"],
        ChartNames.SpreadRisk: ["#F6ECED", "#E9CF8F", "#CEB8DE", "#6C7BC0"],
        ChartNames.ProjectedMarketRiskAgg: ["#A5BDFD"],
        ChartNames.ProjectedLifeInsuranceRiskAgg: ["#A5BDFD"],
        ChartNames.LifeInsuranceRiskAgg: ["#FFE5B9"],
        ChartNames.BalanceSheet: [
            "#A0B1F1",
            "#6E84FE",
            "#8698FB",
            "#D5DAFB",
            "#2741BC",
        ],
        ChartNames.RiskDistribution: [
            "#8AA5E5",
            "#F4F0FD",
            "#E5DAFB",
            "#CBB6F8",
            "#A88DEB",
            "#C0E5B7",
        ],
        ChartNames.MarketRiskDistribution: [
            "#C6F1FA",
            "#FFDDDC",
            "#DACCDD",
            "#E4EDEC",
            "#F8E297",
        ],
        ChartNames.LifeInsuranceRiskDistribution: [
            "#D1CDEE",
            "#F3F3F3",
            "#D1E4DE",
            "#B5D9E7",
            "#E4D8DC",
            "#C0E5B7",
            "#EABBC1",
        ],
        ChartNames.AssetMV: ["#D3DCFC", "#B1BAFD", "#8698FB", "#6E84FE"],
        ChartNames.MarketRiskProjection: ["#D5DAFB"],
        ChartNames.LifeInsuranceRiskProjection: ["#C6F1FA"],
        ChartNames.AssetPortfolio: ["#FFE5B9", "#B0D0F9", "#E6BFCE", "#FFC77F"],
    }

    return color_schema.get(chart_name, None)


def calc_ratio(x, y):
    result = f"{round((x - y) / y, 2) * 100}%"
    logger.info("Result: {}".format(result))
    return result


def create_grid_of_pie_charts(df, names, color_schema, rows=2, cols=3):
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
    # Create figure
    fig = go.Figure()

    # Add pie charts to figure
    column_names = [
        "2018-12-31",
        "2019-12-31",
        "2020-12-31",
        "2021-12-31",
        "2022-12-31",
        "2023-12-31",
    ]
    for i, column in enumerate(column_names):
        #  Select first and group columns only
        data = df[[names, column]]
        current_chart = go.Pie(
            labels=data[names],
            values=data[column],
            name=column,
            title=column,
            domain={"row": i // cols, "column": i % cols},
        )

        # Make some gap between title and chart
        current_chart.title.position = "bottom center"
        current_chart.title.font.size = 16
        current_chart.marker.colors = color_schema

        fig.add_trace(current_chart)

    # Update current chart title position
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(family="sans serif 'Nunito Sans'", size=13, color="#000000"),
        hovertemplate="<br>Percentage: %{percent}<extra></extra>",
    )

    # Update layout
    margin = dict(l=1, r=1, t=1, b=1, pad=70)
    fig.update_layout(
        grid={"rows": rows, "columns": cols},
        margin=margin,
        legend=dict(orientation="v", x=1.1, y=0.5),
    )

    # Apply white border to pie chart
    fig.update_traces(marker=dict(line=dict(color="#FFFFFF", width=1)), sort=False)
    return fig


def create_pie_chart(
    df, names: str, values: str, color_schema: dict, margin=None, text_size=15
):
    """
    Create pie chart object
    :param df: data to be used for chart creation
    :param names: Data names to be used for chart creation
    :param values: Data values to be used for chart creation
    :param title: Title of the chart
    :param color_schema: List of color values
    :param margin: Margin to be used to update the chart (optional)
    :param text_size: Text size for chart (optional)
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
        textinfo="percent+label",
        textfont=dict(
            family="sans serif 'Nunito Sans'", size=text_size, color="#000000"
        ),
        hovertemplate="<br>Percentage: %{percent}<extra></extra>",
    )
    # Apply white border to pie chart
    chart.update_traces(marker=dict(line=dict(color="#FFFFFF", width=1)), sort=False)

    # Update legend position
    chart.update_layout(
        margin=margin,
        legend=dict(orientation="v", x=1.2, y=0.5),
    )
    return chart


def create_bar_chart(
    df: pd.DataFrame,
    x: list[str] | str,
    y: list[str] | str,
    title: str,
    orientation: str = "v",
    barmode: str = "stack",
    color: str = None,
    color_schema: str = None,
    text_color: str = "#4F4F4F",
    pattern_shape: str = None,
    pattern_size: int = 10,
    hide_title: bool = False,
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
    :param pattern_shape: Pattern shape to be used for the last bar chart (optional) (default None)
        shapes: ['', '/', '\\', 'x', '-', '|', '+', '.']
    :param pattern_size: Pattern size (optional) (default 10)
    :return chart: chart object
    """
    legend_names = rename_lagends()

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
        labels={
            f"{x}": "",
            f"{y}": "",
            "variable": "",
            "value": "",
        },
    )

    # Rename legend names
    chart.for_each_trace(
        lambda trace: trace.update(name=legend_names.get(trace.name, trace.name)),
    )

    chart.update_layout(
        margin=dict(l=5, r=5, t=25, b=5),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        legend=dict(orientation="v", y=0.5),
        xaxis_tickmode="array",
        xaxis_tickangle=0,
        xaxis_tickvals=df[x],
        xaxis_tickformat="%Y",
        dragmode=False,
    )
    chart.update_traces(
        selector=dict(type="bar"),
        textfont=dict(family="sans serif 'Nunito Sans'", size=16, color=text_color),
        hovertemplate="%{x}: %{y:,.1f} <extra></extra>",
    )

    chart.update_xaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)
    chart.update_yaxes(
        showline=True,
        linewidth=1.2,
        linecolor="#E0E0E0",
        mirror=True,
    )

    # Make gap between bar charts bigger
    chart.update_layout(bargap=0.4)

    # Adjust chart parameters to fit, apply different ones depending on the orientation type
    if orientation == "v":
        chart.update_traces(
            texttemplate="%{y:,.2s}",
            textposition="none",
            textfont_size=12,
            insidetextanchor="middle",
        )

        # Set Y-axis range
        chart.update_yaxes(
            visible=True,
            showticklabels=True,
            showgrid=True,
            tickprefix="",
            tickformat=",.0f",
            ticksuffix="",
        )

    else:
        chart.update_traces(
            texttemplate="%{x:f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont_size=12,
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
                    y=1.07,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(family="Arial", size=12, color="#828282"),
                )
            ],
        )

        # Adjust bar gap to make it fit
        if pattern_shape is not None:
            chart.update_layout(bargap=0.5)
        else:
            chart.update_layout(bargap=0.525)

    else:
        # Add annotations
        chart.update_layout(
            margin=dict(t=30, b=0, r=10, l=10),
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

    # Apply pattern shape to the last bar chart on y-axis if needed
    if pattern_shape is not None:
        chart.data[len(y) - 1].update(
            marker=dict(
                pattern=dict(shape=pattern_shape, size=pattern_size, fgcolor="#FFFFFF"),
            )
        )

    # Remove white line from stacked bars
    chart.update_traces(marker_line_width=0, selector=dict(type="bar"))

    return chart


def get_template_df(journal_name, generate_header_rows=True, header=[0]):
    """
    Get DataFrame by reading template csv file
    :param journal_name: journal name (e.g. "AC")
    :return: DataFrame, list of header rows
    """
    # Get path to template csv file by journal name and make dataframe from it
    current_path = os.path.dirname(os.path.abspath(__file__))
    # go to parent directory
    current_path = os.path.dirname(current_path)

    # Get DataFrame with column
    df = pd.read_csv(
        f"{current_path}\\templates\\{journal_name}.csv",
        header=header,
        encoding="utf-8",
    )

    # Rename "Unnamed" columns to empty string
    if len(header) == 1:
        logger.info("Renaming columns for template: {}".format(journal_name))
        df.columns = [remove_substring(col) for col in df.columns]

    # # Replace NaN values with empty string
    # df = df.replace(np.nan, "N/A", regex=True)

    # Get header rows
    header_rows = []
    if generate_header_rows:
        for index, row in df.iterrows():  # Iterate over rows
            # Get first cell value
            first_cell_value = row[0]
            # Check if first cell value not starts with empty space
            if (
                isinstance(first_cell_value, str)
                and first_cell_value
                and not first_cell_value.startswith(" ")
            ):
                header_rows.append(index)
        # logger.info("Header rows for {}: {}".format(journal_name, header_rows))
    return df, header_rows


def replace_template_values(template, db_results):
    """
    Replace template values with actual values from DB
    :param template: template DataFrame
    :param db_results: DB results
    :return: DataFrame with replaced values
    """
    # Copy template DataFrame to avoid changing original one
    df = template.copy()
    report_dates = [
        "2018-12-31",
        "2019-12-31",
        "2020-12-31",
        "2021-12-31",
        "2022-12-31",
        "2023-12-31",
    ]

    # Iterate over each column and read values, skip first column
    for column in df.columns[1:]:
        current_key = column[1].lower()
        # Check if DB result exists for current result
        if current_key not in db_results:
            logger.info(
                "DB result does not exist for current key: {}".format(current_key)
            )
            continue
        logger.info("Current result: {}".format(current_key))

        # Get DB result for that key
        db_result = db_results[current_key]
        db_result_columns = db_result.columns.values.tolist()

        # Get column values and iterate over them with row index
        for row_index, cell_value in enumerate(df[column]):
            # logger.info(f"Row index: {row_index}, current cell value: {cell_value}")

            # Skip if cell value does not exist in DB result
            if cell_value not in db_result_columns:
                # logger.info(
                #     f"Skipping updating current cell as it does not exist in DB result: {cell_value}"
                # )
                continue

            # Read first column value for that current row
            current_report_date = df.iloc[row_index, 0]
            # logger.info(f"Current report date: {current_report_date}")
            if current_report_date not in report_dates:
                # logger.info("Skipping empty cell value")
                continue

            # Get actual result from DB result by applying needed filters
            try:
                # If row index is between 1 and 6, calculate difference between base and filtered value
                if row_index in range(1, 7):
                    base_data = db_results["base"]
                    base_row = base_data[
                        base_data["Report_Date"] == current_report_date
                    ]
                    filtered_row = db_result[
                        db_result["Report_Date"] == current_report_date
                    ]
                    actual_value = (
                        base_row[cell_value].values[0]
                        - filtered_row[cell_value].values[0]
                    )
                else:
                    filtered_row = db_result[
                        db_result["Report_Date"] == current_report_date
                    ]
                    actual_value = filtered_row[cell_value].values[0]
            except Exception as e:
                logger.error(
                    f"Error occurred while processing cell value: {cell_value}, error message: {str(e)}"
                )
                continue

            # logger.info(f"Actual value: {actual_value}")

            # Replace cell value with actual value, use row index and column name
            df.loc[row_index, column] = actual_value

    return df


def remove_substring(string):
    """
    Remove substring from string
    :param string: string
    :return: string
    """
    if "." in string:
        string = string.split(".")[0]
    if "Unnamed" in string:
        string = ""
    return string


def get_percentage_variables():
    """
    Retrive percentage variables
    :return: list of percentage variables (list)
    """
    results = [
        "RiskPropotion_1",
        "RiskPropotion_2",
        "RiskPropotion_3",
        "RiskPropotion_4",
        "RiskPropotion_5",
        "RiskPropotion_6",
        "MarketProportion_1",
        "MarketProportion_2",
        "MarketProportion_3",
        "MarketProportion_4",
        "MarketProportion_5",
        "LifeInsProportion_1",
        "LifeInsProportion_2",
        "LifeInsProportion_3",
        "LifeInsProportion_4",
        "LifeInsProportion_5",
        "LifeInsProportion_6",
        "LifeInsProportion_7",
    ]
    return results


def convert_to_percentage(value, round_to=2, perform_abs=True):
    """
    Convert value to percentage
    :param value: value to be converted
    :return: value in percentage
    """
    result = value * 100
    # Round to 2 decimal places
    result = round(result, round_to)
    # Convert to positive number
    if perform_abs:
        result = abs(result)
    # Cast to string, add left padding with 0
    result = f"{result:.2f}%"
    return result


def calculate_avg_value(template_df, result_df):
    """
    Calculate average value for each column
    :param df: DataFrame
    :return: DataFrame
    """
    report_dates = [
        "2018-12-31",
        "2019-12-31",
        "2020-12-31",
        "2021-12-31",
        "2022-12-31",
        "2023-12-31",
    ]

    # logger.info("Result df: {}".format(result_df))
    # Iterate over columns, except first column
    for column in template_df.columns[1:]:
        # Get column name
        report_date = column
        # logger.info(f"COLUMN NAME: {report_date}")
        # Get column values
        column_values = template_df[report_date].values
        # Iterate over column values
        for variable_name in column_values:
            # Check if value is not empty
            if variable_name:
                # Calculate average value for cell
                # logger.info(
                #     "Calculating average value for cell: {}".format(variable_name)
                # )
                # Skip if value is empty, nan or null
                if (
                    pd.isna(variable_name)
                    or pd.isnull(variable_name)
                    or variable_name == ""
                    or report_date not in report_dates
                ):
                    continue

                # Get previous year value from report_dates if not first item
                try:
                    # Get all values from result_df for report date and calculate average on the cell value
                    # logger.info("Report date: {}".format(report_date))
                    avg_value = result_df[result_df["ReportDate"] == report_date][
                        variable_name
                    ].mean(axis=0)
                    logger.info(f"Average {variable_name} value: {avg_value}")

                    # # Replace value in template DataFrame
                    template_df[report_date] = template_df[report_date].replace(
                        variable_name, avg_value
                    )
                except Exception as e:
                    logger.error(
                        "Error while calculating average value for cell: {}".format(
                            variable_name
                        )
                    )
                    logger.error(e)
                    continue

    return template_df


def add_sum_row(df):
    """
    Add sum row to DataFrame
    :param df: DataFrame
    :return: DataFrame
    """
    df.iloc[4, 1:] = df.iloc[:4, 1:].sum(axis=0)
    return df


def calculate_ratios(result):
    """
    Calculate ratios between some rows
    """
    first_part = result.iloc[4, 1:]
    second_part = result.iloc[6, 1:]
    third_part = result.iloc[5, 1:]

    # Calculate ratio between needed rows
    ratio_1 = first_part / second_part
    ratio_1 = ratio_1.map(lambda x: f"{round((x-1) * 100 , 2)}%")
    result.iloc[7, 1:] = ratio_1

    ratio_2 = first_part / third_part
    ratio_2 = ratio_2.map(lambda x: f"{round((x) * 100 , 2)}%")
    result.iloc[8, 1:] = ratio_2

    return result


def calc_ratio(col):
    """
    Calculate DF column ratio
    """
    if isinstance(col[0], str):
        return col
    return col / col.sum()


def downscale_value(col, divisor=100000):
    """
    Downscale value in DF column by divisor
    """
    if isinstance(col[0], str):
        return col
    return col / divisor


def pivot_df(df, index_name, convert_to_datetime=None):
    """
    Helper function to rotate the df
    :param df: the df to rotate
    :param result: rotated result
    """
    df = df.reset_index(drop=True).transpose()
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df = df.reset_index(drop=False)
    df = df.rename(columns={"index": index_name})

    # Convert string representation of date to datetime object
    if convert_to_datetime is not None:
        # Add 00:00:00 to the end of the date string
        df[convert_to_datetime] = df[convert_to_datetime] + " 00:00:00"
        df[convert_to_datetime] = pd.to_datetime(
            df[convert_to_datetime], format="%Y-%m-%d %H:%M:%S", exact=True
        )
    return df


def get_db_connection(wvr_path, model_name):
    """
    Get database connection (initalize connection for boost further processing)
    :param wvr_path: WVR path (str)
    :param model_name: Model name (str)
    :return: Database connection (pyodbc connection object)
    """
    connection = None
    try:
        connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model_name)
        logger.info("Connect string: {}".format(connect_string))
        connection = wvr_functions.get_connection(connect_string)
    except Exception as e:
        logger.error(f"Error while establishing connection: {e}")
    return connection


def get_partial_data(df, start_row, end_row, keep_first_level=True):
    """
    Get partial data from DataFrame
    :param df: DataFrame
    :param start_row: Start row index
    :param end_row: End row index
    :return: DataFrame
    """
    df_copy = df.copy()
    if keep_first_level:
        # Remove first column level
        df_copy.columns = df_copy.columns.droplevel(0)
        df_copy = df_copy.drop("Base", axis=1)
        df_copy.columns = [remove_substring(col) for col in df_copy.columns]
        df_copy = df_copy.rename(columns={"": "Report_Date"})

    return df_copy.iloc[start_row:end_row]


def convert_df(df, to_dict=True):
    """
    Convert a multi-level DataFrame to a dictionary and back to a multi-level DataFrame.
    :param df: Multi-level DataFrame to convert (pd.DataFrame)
    :param to_dict: If True, convert to dictionary. If False, convert from dictionary. (bool)
    :return: Converted DataFrame or dictionary (pd.DataFrame or dict)
    """
    if to_dict:
        # Convert column names to tuples
        df.columns = [str(col) for col in df.columns]
        # Convert the DataFrame to a dictionary
        data_dict = df.to_dict(orient="split")
        return data_dict

    # Convert the dictionary back to a DataFrame
    df = pd.DataFrame(df["data"], columns=df["columns"])
    try:
        df.columns = pd.MultiIndex.from_tuples(
            [ast.literal_eval(col) for col in df.columns]
        )
    except Exception as e:
        logger.error(f"Error while normalizing column names: {e}")

    return df


def perform_calculations(df):
    """
    Perform special calculations for the DataFrame to get needed values
    :param df: DataFrame to perform calculations on
    :return: DataFrame with calculated values
    """
    # Add special column by performing some calculations
    special_columns = {
        "Lapse": ["Lapse_Down", "Lapse_Mass", "Lapse_Up"],
        "Equity": ["Equity_Type_1_General", "Equity_Type_2_General"],
        "Interest": ["Interest_Down", "Interest_Up"],
        "Spread": [
            "Spread_Bond_Infra_Corp",
            "Spread_Bond_Infra_Invest",
            "Spread_Bond_No_Infra",
        ],
        "Fx": ["Fx_Down", "Fx_Up"],
        "Market_Risk": {
            "names": ["Equity", "Interest", "Property", "Spread", "Fx"],
            "matrix": np.array(
                [
                    [1, 0.5, 0.75, 0.75, 0.25],
                    [0.5, 1, 0.5, 0.5, 0.25],
                    [0.75, 0.5, 1, 0.5, 0.25],
                    [0.75, 0.5, 0.5, 1, 0.25],
                    [0.25, 0.25, 0.25, 0.25, 1],
                ]
            ),
        },
        "Life_Insurance_Risk": {
            "names": [
                "Catastrophe",
                "Expense",
                "Lapse",
                "Longevity",
                "Morbidity",
                "Mortality",
            ],
            "matrix": np.array(
                [
                    [1, 0.25, 0.25, 0, 0.25, 0.25],
                    [0.25, 1, 0.5, 0.25, 0.5, 0.25],
                    [0.25, 0.5, 1, 0.25, 0, 0],
                    [0, 0.25, 0.25, 1, 0, -0.25],
                    [0.25, 0.5, 0, 0, 1, 0.25],
                    [0.25, 0.25, 0, -0.25, 0.25, 1],
                ]
            ),
        },
    }

    # Loop over special columns and calculate logic
    for column, wanted_columns in special_columns.items():
        try:
            # Calculate square root of x and y columns with additional logic
            if column == "Equity":
                x_column = wanted_columns[0]
                y_column = wanted_columns[1]
                calc_values = df.apply(
                    lambda row: math.sqrt(
                        row[x_column] ** 2
                        + row[y_column] ** 2
                        + 2 * 0.75 * row[x_column] * row[y_column]
                    ),
                    axis=1,
                )

            # Calculate square root of matrix multiplication
            elif column == "Market_Risk" or column == "Life_Insurance_Risk":
                # Get only needed columns
                filtered_df = df[wanted_columns["names"]]

                # Apply max on each cell
                if column == "Life_Insurance_Risk":
                    filtered_df = filtered_df.apply(
                        lambda cell: cell.map(lambda x: 0 if x < 0 else x), axis=0
                    )

                # Perform matrix multiplication
                calc_values = filtered_df.apply(
                    lambda row: calculate_row_sqrt(wanted_columns["matrix"], row),
                    axis=1,
                )

            # Calculate sum of wanted columns and take max value from them
            else:
                calc_values = df[wanted_columns].max(axis=1)
                # Check if values are negative, if so, take 0 instead
                calc_values = calc_values.map(lambda x: 0 if x < 0 else x)

            df[column] = calc_values
        except Exception as e:
            logger.error(f"Error while performing calculations for {column}: {e}")
            continue

    return df


def calculate_row_sqrt(matrix, row):
    """
    Calculate square root of matrix multiplication
    :param matrix: Matrix to multiply
    :param row_vector: Row vector to multiply
    :return: Square root of matrix multiplication
    """
    # Calculate matrix multiplication
    row_vector = np.array(row)
    result = np.matmul(row_vector, np.matmul(matrix, row_vector.T))

    # Calculate square root of calculated matrix multiplication
    sqrt_result = np.sqrt(result)
    logger.info("Square root result: {}".format(sqrt_result))

    return sqrt_result


def rename_lagends(legends_dict=None):
    """
    Helper function to rename legends to match the ones in the template
    """

    default = {
        "Dev_Period_Position": "Dev Period",
        "Origin_Period_Position": "Origin Period",
        "returnValue": "Value"
    }

    # Get kwargs
    if legends_dict is None:
        return default

    return {**default, **legends_dict}


def replace_template_values_ordinary(
    template_df,
    lookup_df,
):
    """
    Replace template values by checking
    """
    df = template_df.copy()
    lookup_dict = lookup_df.to_dict(orient="records")[0]
    # Use applymap to replace values if there is no formula in the template
    df = df.applymap(lambda x: apply_formatting(x, lookup_dict))
    return df


def apply_formatting(cell_value, lookup_dict, perform_abs=False):
    """
    Apply formatting to cell value
    :param cell_value: cell value
    :param lookup_dict: lookup dictionary
    :return: formatted cell value with replacement value if applicable
    """
    if (
        pd.isna(cell_value)
        or pd.isnull(cell_value)
        or cell_value == ""
        or isinstance(cell_value, int)
    ):
        if str(cell_value).lower() == "true":
            return str(cell_value).upper()
        return cell_value

    # Remove substring from cell value if possible
    try:
        new_value = lookup_dict.get(cell_value, cell_value)
    except Exception as e:
        logger.info("Error occurred: {}".format(e))
        new_value = cell_value

    # Cast cell value to float if possible
    if not isinstance(new_value, (int, float, datetime.date)) and new_value.isdigit():
        new_value = float(new_value)

    percentage_variables = get_percentage_variables()
    # Check if cell value is percentage
    if cell_value in percentage_variables:
        new_value = convert_to_percentage(
            new_value, perform_abs=perform_abs, round_to=1
        )

    # logger.info("Cell value: {}, new value: {}".format(cell_value, new_value))
    return new_value


def remove_substring(string):
    """
    Remove substring from string
    :param string: string
    :return: string
    """
    if "." in string:
        string = string.split(".")[0]
    if "Unnamed" in string:
        string = ""
    return string


def get_percentage_variables():
    """
    Retrive percentage variables
    :return: list of percentage variables (list)
    """
    results = [
        "RiskPropotion_1",
        "RiskPropotion_2",
        "RiskPropotion_3",
        "RiskPropotion_4",
        "RiskPropotion_5",
        "RiskPropotion_6",
        "MarketProportion_1",
        "MarketProportion_2",
        "MarketProportion_3",
        "MarketProportion_4",
        "MarketProportion_5",
        "LifeInsProportion_1",
        "LifeInsProportion_2",
        "LifeInsProportion_3",
        "LifeInsProportion_4",
        "LifeInsProportion_5",
        "LifeInsProportion_6",
        "LifeInsProportion_7",
    ]
    return results


def convert_to_percentage(value, round_to=2, perform_abs=True):
    """
    Convert value to percentage
    :param value: value to be converted
    :return: value in percentage
    """
    result = value * 100
    # Round to 2 decimal places
    result = round(result, round_to)
    # Convert to positive number
    if perform_abs:
        result = abs(result)
    # Cast to string, add left padding with 0
    result = f"{result:.2f}%"
    return result

def convert_df_to_triangle (df, triangle_indexes, triangle_columns, triangle_values, force=None):
    """
    Convert dataframe data returned by wvr to a triangle table representation
    :param value: df raw
    :return: df triangle
    """
    if force is not None:
        dev = int(force[0]) + 1
        orig = int(force[1])

        for i in range(1,dev):
            df.loc[(df['Dev_Period_Position'] == i) & (df['Origin_Period_Position'] > orig), 'returnValue'] = None
            orig = orig - 1

    out_df = pd.DataFrame(df.pivot(index=triangle_indexes, columns=triangle_columns, values=triangle_values))
    #out_df = df.pivot(index=triangle_indexes, columns=triangle_columns, values=triangle_values)
    #out = df.pivot(index='Origin_Period_Position', columns='Dev_Period_Position', values='returnValue')

    return out_df

def set_wvr_nl_paths(wvr_paths):
    # List of needed mapper names
    mappers = [
        "NL_Data_Prep",
        "NL_LIC_Model",
        "NL_LRC_Fit",
        "NL_LRC_Eval"
    ]
    try:
        test = wvr_functions.identify_models(wvr_paths, mappers)
        mapped_results = dict()
        common_mappers = list()
        for mapper in mappers:
            # Find WVR path based on mapper name pattern
            patter_name = f"{mapper}.wvr"
            filtered_wvr_paths = list(filter(lambda x: x.endswith(patter_name), wvr_paths))

            # Store the relevant WVR path if found
            if len(filtered_wvr_paths) == 0:
                logger.info(f"No path found for {mapper}, skipping ...")
                continue
                # raise Exception(f"No path found for {mapper}, aborting ...")

            # Log warning if multiple paths are found
            if len(filtered_wvr_paths) > 1:
                logger.info(f"Multiple paths found for {mapper}, selecting first one: {filtered_wvr_paths[0]}")
            else:
                logger.info(f"Path found for {mapper}: {filtered_wvr_paths[0]}")

            mapped_results[mapper.lower()] = filtered_wvr_paths[0]
            common_mappers.append(filtered_wvr_paths[0])

        if len(mapped_results) == 0:
            mapped_results = wvr_functions.identify_models(wvr_paths, mappers)

        # # Raise exception if not all WVR paths are set
        # logger.info("Same model-named NL Std.Code WVR paths: {}".format(mapped_results))
        #
        # # Set unique WVR path for "Aggregation_std" mapper as it's the only one that not found in common_mappers
        # common_mappers = set(common_mappers)
        # wvr_paths = set(wvr_paths)
        # unique_wvr_paths = list(wvr_paths - common_mappers)
        # logger.info("Unique ORSA WVR paths: {}".format(unique_wvr_paths))
        #
        # #mapped_results["aggregation_std"] = found_models.get("SII_Aggregation_Std_Formula_Group")
        #
        # logger.info("Final ORSA WVR paths: {}".format(mapped_results))
        mapped_results = {k.lower(): v for k, v in mapped_results.items()}
        return mapped_results

    except Exception as e:
        raise e
    return mapped_results



def create_line_chart(
    df: pd.DataFrame,
    x: list[str] | str,
    y: list[str] | str,
    title: str,
    orientation: str = "v",
    barmode: str = "stack",
    color: str = None,
    color_schema: str = None,
    text_color: str = "#4F4F4F",
    pattern_shape: str = None,
    pattern_size: int = 10,
    hide_title: bool = False,
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
    :param pattern_shape: Pattern shape to be used for the last bar chart (optional) (default None)
        shapes: ['', '/', '\\', 'x', '-', '|', '+', '.']
    :param pattern_size: Pattern size (optional) (default 10)
    :return chart: chart object
    """

    legend_names = rename_lagends()

    chart2 = px.line(
        data_frame=df,
        x=x,
        y=y,
        color=color,
        markers=True,
        orientation="h"
    )

    # Rename legend names
    chart2.for_each_trace(
        lambda trace: trace.update(name=legend_names.get(trace.name, trace.name)),
    )


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
        labels={
            f"{x}": "",
            f"{y}": "",
            "variable": "",
            "value": "",
        },
    )

    # Rename legend names
    chart.for_each_trace(
        lambda trace: trace.update(name=legend_names.get(trace.name, trace.name)),
    )

    chart.update_layout(
        margin=dict(l=5, r=5, t=25, b=5),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        legend=dict(orientation="v", y=0.5),
        xaxis_tickmode="array",
        xaxis_tickangle=0,
        xaxis_tickvals=df[x],
        xaxis_tickformat="%Y",
        dragmode=False,
    )
    chart.update_traces(
        selector=dict(type="bar"),
        textfont=dict(family="sans serif 'Nunito Sans'", size=16, color=text_color),
        hovertemplate="%{x}: %{y:,.1f} <extra></extra>",
    )

    chart.update_xaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)
    chart.update_yaxes(
        showline=True,
        linewidth=1.2,
        linecolor="#E0E0E0",
        mirror=True,
    )

    # Make gap between bar charts bigger
    chart.update_layout(bargap=0.4)

    # Adjust chart parameters to fit, apply different ones depending on the orientation type
    if orientation == "v":
        chart.update_traces(
            texttemplate="%{y:,.2s}",
            textposition="none",
            textfont_size=12,
            insidetextanchor="middle",
        )

        # Set Y-axis range
        chart.update_yaxes(
            visible=True,
            showticklabels=True,
            showgrid=True,
            tickprefix="",
            tickformat=",.0f",
            ticksuffix="",
        )

    else:
        chart.update_traces(
            texttemplate="%{x:f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont_size=12,
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
                    y=1.07,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(family="Arial", size=12, color="#828282"),
                )
            ],
        )

        # Adjust bar gap to make it fit
        if pattern_shape is not None:
            chart.update_layout(bargap=0.5)
        else:
            chart.update_layout(bargap=0.525)

    else:
        # Add annotations
        chart.update_layout(
            margin=dict(t=30, b=0, r=10, l=10),
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

    # Apply pattern shape to the last bar chart on y-axis if needed
    if pattern_shape is not None:
        chart.data[len(y) - 1].update(
            marker=dict(
                pattern=dict(shape=pattern_shape, size=pattern_size, fgcolor="#FFFFFF"),
            )
        )

    # Remove white line from stacked bars
    chart.update_traces(marker_line_width=0, selector=dict(type="bar"))

    return chart2



def create_line_chart_ATA(
    df: pd.DataFrame,
    x: list[str] | str,
    y: list[str] | str,
    title: str,
    orientation: str = "v",
    barmode: str = "stack",
    color: str = None,
    color_schema: str = None,
    text_color: str = "#4F4F4F",
    pattern_shape: str = None,
    pattern_size: int = 10,
    hide_title: bool = False,
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
    :param pattern_shape: Pattern shape to be used for the last bar chart (optional) (default None)
        shapes: ['', '/', '\\', 'x', '-', '|', '+', '.']
    :param pattern_size: Pattern size (optional) (default 10)
    :return chart: chart object
    """

    legend_names = rename_lagends()

    chart2 = px.line(
        data_frame=df,
        x=x,
        y=y,
        color=color,
        markers=True,
        #orientation="h"
    )

    # trace1 = px.line(dfATAFigure, x='Dev_Period_Position', y='ATA', color='Orig_New',
    #                  markers=True,
    #                  category_orders={"Orig_New": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]})

    # Rename legend names
    chart2.for_each_trace(
        lambda trace: trace.update(name=legend_names.get(trace.name, trace.name)),
    )


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
        labels={
            f"{x}": "",
            f"{y}": "",
            "variable": "",
            "value": "",
        },
    )

    # Rename legend names
    chart.for_each_trace(
        lambda trace: trace.update(name=legend_names.get(trace.name, trace.name)),
    )

    chart.update_layout(
        margin=dict(l=5, r=5, t=25, b=5),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        legend=dict(orientation="v", y=0.5),
        xaxis_tickmode="array",
        xaxis_tickangle=0,
        xaxis_tickvals=df[x],
        xaxis_tickformat="%Y",
        dragmode=False,
    )
    chart.update_traces(
        selector=dict(type="bar"),
        textfont=dict(family="sans serif 'Nunito Sans'", size=16, color=text_color),
        hovertemplate="%{x}: %{y:,.1f} <extra></extra>",
    )

    chart.update_xaxes(showline=True, linewidth=1.2, linecolor="#E0E0E0", mirror=True)
    chart.update_yaxes(
        showline=True,
        linewidth=1.2,
        linecolor="#E0E0E0",
        mirror=True,
    )

    # Make gap between bar charts bigger
    chart.update_layout(bargap=0.4)

    # Adjust chart parameters to fit, apply different ones depending on the orientation type
    if orientation == "v":
        chart.update_traces(
            texttemplate="%{y:,.2s}",
            textposition="none",
            textfont_size=12,
            insidetextanchor="middle",
        )

        # Set Y-axis range
        chart.update_yaxes(
            visible=True,
            showticklabels=True,
            showgrid=True,
            tickprefix="",
            tickformat=",.0f",
            ticksuffix="",
        )

    else:
        chart.update_traces(
            texttemplate="%{x:f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont_size=12,
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
                    y=1.07,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(family="Arial", size=12, color="#828282"),
                )
            ],
        )

        # Adjust bar gap to make it fit
        if pattern_shape is not None:
            chart.update_layout(bargap=0.5)
        else:
            chart.update_layout(bargap=0.525)

    else:
        # Add annotations
        chart.update_layout(
            margin=dict(t=30, b=0, r=10, l=10),
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

    # Apply pattern shape to the last bar chart on y-axis if needed
    if pattern_shape is not None:
        chart.data[len(y) - 1].update(
            marker=dict(
                pattern=dict(shape=pattern_shape, size=pattern_size, fgcolor="#FFFFFF"),
            )
        )

    # Remove white line from stacked bars
    chart.update_traces(marker_line_width=0, selector=dict(type="bar"))

    return chart2