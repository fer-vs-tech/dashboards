import logging

logger = logging.getLogger(__name__)

import ast
import datetime
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import cm_dashboards.ifrs17_accounting.dash_utils as dash_utils
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.flaor.results.program_names import ChartNames
from cm_dashboards.flaor.utils.abstract_handler import GenericHandler


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


def pivot_dataframe(df):
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

    # Make the first row as header row
    df.columns = df.iloc[0]
    # Drop the first row
    df = df.drop(df.index[0])
    # Map through each column and convert to string
    df.columns = df.columns.map(str)

    return df


def set_color_schema(chart_name):
    """
    Retrive color schema for chart type specified
    """
    color_schema = {
        ChartNames.ASSET_PORTFOLIO: [
            "#2741BC",
            "#6E84FE",
            "#8698FB",
            "#A0B1F1",
            "#D5DAFB",
        ],
        ChartNames.REQUIRED_CAPITAL: [
            "#8AA5E5",
            "#F4F0FD",
            "#E5DAFB",
            "#CBB6F8",
            "#A88DEB",
            "#C0E5B7",
        ],
        ChartNames.PROJECTED_RISK_REGULATORY: [
            "#C6F1FA",
            "#FFDDDC",
            "#DACCDD",
            "#E4EDEC",
            "#F8E297",
        ],
        ChartNames.AVAILABLE_CAPITAL: [
            "#D1CDEE",
            "#F3F3F3",
            "#D1E4DE",
            "#B5D9E7",
            "#E4D8DC",
            "#C0E5B7",
            "#EABBC1",
        ],
        ChartNames.LIFE_AND_HEALTH_RISK_OVERALL: [
            "#FFC77F",
            "#B0D0F9",
            "#E6BFCE",
            "#C6F1FA",
            "#F4F0FD",
            "#FFE5B9",
            "#E5DAFB",
        ],
        ChartNames.SOLVENCY_OVERALL: [
            "#C79ECF",
            "#C8E4FE",
            "#A5AEFF",
        ],
        ChartNames.MORBITITY_RISK: [
            "#EAE7E7",
            "#FAB2AC",
            "#EDA1C1",
        ],
        ChartNames.LAPSE_RISK: [
            "#F6ECED",
            "#E9CF8F",
            "#CEB8DE",
            "#6C7BC0",
        ],
        ChartNames.MARKET_RISK_OVERALL: [
            "#F6ECED",
            "#E9CF8F",
            "#CEB8DE",
            "#6C7BC0",
            "#AFCEE3",
            "#FFE5B9",
        ],
        ChartNames.INTEREST_RISK: [
            "#D3DCFC",
            "#B1BAFD",
            "#8698FB",
            "#6E84FE",
            "#2741BC",
            "#A0B1F1",
        ],
        ChartNames.EQUITY_RISK: [
            "#EAE7E7",
            "#76B39D",
            "#155E63",
            "#FAB2AC",
            "#EDA1C1",
            "#C6F1FA",
            "#FFE5B9",
        ],
        ChartNames.FOREX_RISK: [
            "#ADD5D7",
            "#9CB7A8",
            "#C6F1FA",
            "#FFE5B9",
        ],
        ChartNames.CONCENTRATION_RISK: [
            "#D5DAFB",
            "#FFE5B9",
            "#C6F1FA",
        ],
        ChartNames.LIFE_AND_HEALTH_INSURANCE_RISK: ["#AFCEE3"],
        ChartNames.MORTALITY_RISK: ["#D5DAFB"],
        ChartNames.LONGEVITY_RISK: ["#FFEFD7"],
        ChartNames.EXPENSE_RISK: ["#C6F1FA"],
        ChartNames.CATASTROPHE_RISK: ["#AFCEE3"],
        ChartNames.MARKET_RISK: ["#FFE5B9"],
        ChartNames.PROPERTY_RISK: ["#FFE6EA"],
        ChartNames.CREDIT_RISK: px.colors.qualitative.Light24,
    }

    return color_schema.get(chart_name, None)


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
    add_annotations: bool = False,
    secondary_y: str = None,
    facet_col: str = None,
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
        facet_col=facet_col,
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

        # Adjust bar gap to make it fit
        if pattern_shape is not None:
            chart.update_layout(bargap=0.5)
        else:
            chart.update_layout(bargap=0.525)

    # Add annotations
    if add_annotations:
        chart.update_layout(
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

    # Apply margin
    chart.update_layout(margin=dict(t=30, b=0, r=10, l=10))

    # Apply pattern shape to the last bar chart on y-axis if needed
    if pattern_shape is not None:
        if facet_col is None:
            chart.data[0].update(
                marker=dict(
                    pattern=dict(
                        shape=pattern_shape, size=pattern_size, fgcolor="#FFFFFF"
                    ),
                )
            )
        else:
            # Only apply pattern shape to the Required_Capital trace
            for trace in chart.data:
                if trace.name in ["Required_Capital", "Credit Risk"]:
                    trace.update(
                        marker=dict(
                            pattern=dict(
                                shape=pattern_shape,
                                size=pattern_size,
                                fgcolor="#FFFFFF",
                            ),
                        )
                    )

    # Add secondary y-axis if needed
    if secondary_y is not None:
        chart.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                showgrid=False,
                zeroline=True,
                showline=False,
                ticksuffix="%",
                range=[0, df[secondary_y].max() + (df[secondary_y].max() * 0.18)],
            )
        )
        chart.add_trace(
            go.Scatter(
                x=df[x],
                y=df[secondary_y],
                yaxis="y2",
                mode="lines",
                line=dict(color=color_schema[-1]),
                name="KICS_Ratio",
            )
        )

    # Remove white line from stacked bars
    chart.update_traces(marker_line_width=0, selector=dict(type="bar"))

    if facet_col is not None:
        # Show yaxis ticks for only first column
        chart.update_yaxes(showticklabels=False)
        chart.update_yaxes(showticklabels=True, col=1)

        # Show annotations at the bottom of the chart
        for annotation in chart.layout.annotations:
            text = annotation.text.split("=")[1]
            annotation.update(yref="paper", y=-0.1, text=text[0:4])

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


def rename_lagends(legends_dict=None):
    """
    Helper function to rename legends to match the ones in the template
    """

    default = {
        "Lapse_Down": "Lapse Down",
        "Lapse_Mass": "Lapse Mass",
        "Lapse_Up": "Lapse Up",
        "Equity_Type_1_General": "Equity Type 1",
        "Equity_Type_2_General": "Equity Type 2",
        "Interest_Down": "Interest Down",
        "Interest_Up": "Interest Up",
        "Spread_Bond_Infra_Corp": "Bond: Infra Corp",
        "Spread_Bond_Infra_Invest": "Bond: Infra Invest",
        "Spread_Bond_No_Infra": "Bond: No Infra",
        "Fx_Down": "Fx Down",
        "Fx_Up": "Fx Up",
    }

    # Get kwargs
    if legends_dict is None:
        return default

    return {**default, **legends_dict}


def replace_template_values(
    template_df,
    lookup_df,
    replace_nan=False,
):
    """
    Replace template values by checking
    """
    df = template_df.copy()
    start_row = 0
    for _, row in lookup_df.iterrows():
        df.iloc[start_row : start_row + 3, :] = df.iloc[
            start_row : start_row + 3, :
        ].applymap(lambda x: apply_formatting(x, row.to_dict()))
        start_row += 3

    if replace_nan:
        df = df.fillna(0)
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


def get_percentage_variables():
    """
    Retrive percentage variables
    :return: list of percentage variables (list)
    """
    results = ["KICS_Ratio"]
    return results


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


def convert_to_percentage(value, round_to=2, perform_abs=True):
    """
    Convert value to percentage
    :param value: value to be converted
    :return: value in percentage
    """
    result = value * 100
    result = round(result, round_to)
    if perform_abs:
        result = abs(result)
    result = f"{result:.1f}%"
    return result


def add_group_data(df, df_group):
    """
    Add group data by calculating needed values
    """
    try:
        logger.info("Calculating group data")
        last_seen_date = None
        column_names = [
            "Asset_CFs",
            "Liability_CFs",
            "Liquidity_Gap",
            "New_business",
            "Avg_of_Return_on_Asset_Management",
            "Avg_of_Crediting_Rate",
        ]
        results = {column_name: [] for column_name in column_names}

        for order_num, report_date in enumerate(df.Report_Date):
            logger.info(f"Current report date: {report_date}, index {order_num}")

            if last_seen_date is None:
                filtered_df = df_group[df_group["Report_Date"] == report_date]
            else:
                filtered_df = df_group[
                    (df_group["Report_Date"] > last_seen_date)
                    & (df_group["Report_Date"] <= report_date)
                ]

            for column_name in column_names:
                if column_name in [
                    "Avg_of_Return_on_Asset_Management",
                    "Avg_of_Crediting_Rate",
                ]:
                    value = filtered_df[column_name].mean()
                    if pd.isna(value):
                        value = 0
                    value = convert_to_percentage(value, round_to=3)
                else:
                    value = filtered_df[column_name].sum()
                results[column_name].append(value)

            last_seen_date = report_date

        for column_name in column_names:
            df[column_name] = results[column_name]

        assets_total = df.Liabs_WO_TVOG.tolist()
        liabs_total = df.New_business.tolist()
        df["In-force"] = [x - y for x, y in zip(assets_total, liabs_total)]

        df.reset_index(drop=True, inplace=True)
        column_names = [
            "Report_Date",
            "Asset_CFs",
            "Liability_CFs",
            "Liquidity_Gap",
            "Net_Asset_Value",
            "Assets",
            "Bond",
            "Loan",
            "Cash",
            "Equity",
            "Property",
            "Bond_Percent",
            "Loan_Percent",
            "Cash_Percent",
            "Equity_Percent",
            "Property_Percent",
            "Liabs_WO_TVOG",
            "In-force",
            "New_business",
            "Avg_of_Return_on_Asset_Management",
            "Avg_of_Crediting_Rate",
        ]
        df = df.reindex(columns=column_names)
        logger.info("Completed calculating group data")
    except Exception as e:
        logger.error(f"Error while calculating group data: {e}")
    return df


def update_unique_data(result, result_unique):
    """
    Update existing result with unique data
    """
    logger.info("Updating existing result with unique data")
    result_unique = result_unique.to_dict("records")[0]
    result.iloc[0, 3:8] = list(result_unique.values())

    base_value = result.iloc[0, 2]
    ratios = [(x / base_value * 100) for x in list(result_unique.values())]
    result.iloc[0, 8:13] = ratios

    result.iloc[:, 8:13] = result.iloc[:, 8:13].applymap(lambda x: f"{round(x, 1)}%")
    logger.info("Completed updating existing result with unique data")
    return result


def duplicate_rows(df, columns, divider_column, divider_values):
    """
    Duplicate each row, manipulate rows data and add divider column
    :param df: DataFrame
    :param divider_column: column to be used as divider
    :param divider_values: list of divider values
    :return df: Updated DataFrame
    """
    df = df.loc[df.index.repeat(2)].reset_index(drop=True)
    odd_indices = np.arange(1, len(df), 2)
    even_indices = np.arange(0, len(df), 2)

    df.loc[even_indices, columns[1:]] = 0
    df.loc[odd_indices, columns[0]] = 0
    df[divider_column] = np.where(
        np.arange(len(df)) % 2 == 0, divider_values[0], divider_values[1]
    )

    return df
