from dash.dash_table.Format import Format, Scheme, Sign


def set_multi_index_column_names(
    df,
    flatten_char="_",
    precision=0,
    show_negative_numbers=False,
    hidden_columns=[],
):
    """
    Set multi index to DataFrame
    :param df: DataFrame
    :param flatten_char: flatten character (str)
    :return: table data (dict), column names (list)
    """
    df = df.copy()
    table_columns = []
    default_sign = Sign.negative if show_negative_numbers else Sign.parantheses

    # Check if there are multi index columns
    levels = df.columns.nlevels
    if levels == 1:
        for column in df.columns:
            table_columns.append({"name": column, "id": column})
    else:
        updated_columns = []
        for i, column in enumerate(df.columns):
            # Replace "Unnamed" with empty string
            column = [remove_substring(x) for x in list(column)]
            column = tuple(column)
            column_id = flatten_char.join(column)
            table_columns.append(
                {
                    "name": column,
                    "id": column_id,
                    "type": "numeric",
                    "presentation": "input",
                    "hideable": True if column in hidden_columns else False,
                    "deletable": False,
                    "format": Format(
                        group=",",
                        precision=precision,
                        scheme=Scheme.fixed,
                        sign=default_sign,
                    )
                    if i != 0
                    else Format(
                        group=",", precision=0, scheme=Scheme.fixed, sign=default_sign
                    ),
                }
            )
            updated_columns.append(column_id)
        df.columns = updated_columns

    table_data = df.to_dict("records")
    return table_data, table_columns


def set_column_names(
    columns,
    precision=0,
    show_negative_numbers=False,
    hidden_columns=[],
    additional_header=[],
):
    """
    Apply the column names for the table
    """
    default_sign = Sign.negative if show_negative_numbers else Sign.parantheses
    linkable_columns = ["Download", "Journal"]
    column_names = [
        {
            "name": [additional_header[i], column] if additional_header else column,
            "id": column,
            "type": "text" if column in linkable_columns else "numeric",
            "presentation": "markdown" if column in linkable_columns else "input",
            "hideable": True if column in hidden_columns else False,
            "deletable": False,
            "format": Format(
                group=",", precision=precision, scheme=Scheme.fixed, sign=default_sign
            )
            if i != 0
            else Format(group=",", precision=0, scheme=Scheme.fixed, sign=default_sign),
        }
        for i, column in enumerate(columns)
    ]
    return column_names


def set_table_data(data, id):
    """
    Set the table data with unique ID
    """
    result = {f"{id}_{i}": value for i, value in enumerate(data)}
    return result


def pivot_data(results, x, y, model_field):
    """
    Rotate data in suitable orientation for table display
    """
    pivot = results.set_index([y, x]).unstack(x)
    pivot = pivot.reset_index()
    # Remove multi-index
    pivot = pivot.rename(columns={model_field: "", y: ""})
    pivot.columns = [f"{i}{j}" for i, j in pivot.columns]
    pivot = pivot.rename(columns={"": y})

    # Add sum of rows and columns
    pivot.loc[:, "Total"] = pivot.drop("Origin_Period_Position", 1).sum(
        numeric_only=True, axis=1
    )
    pivot.loc["Total"] = pivot.set_index("Origin_Period_Position").sum(
        numeric_only=True, axis=0
    )
    pivot.iloc[-1, pivot.columns.get_loc("Origin_Period_Position")] = "Total"
    return pivot


# Define custom colors for the graphs
def get_color_plate(graph_name):
    """
    Get the color plate for the graph
    """
    colors = [
        "#7990FF",
        "#39C0BE",
        "#3C62F1",
        "#F8981D",
        "#FA7F7F",
        "#EC008C",
        "#9B51E0",
        "#EB5757",
        "#F7E11E",
        "#1693A5",
    ]
    colors_two = ["#1B238C", "#2741BC", "#4364F7", "#7992FF", "A0B1F1"]
    color_plate = {
        "line": colors,
        "bar": colors_two,
        "pie": colors,
    }

    return color_plate.get(graph_name)


def set_tooltip_for_header(columns):
    """
    Set the tooltip for the header in table
    """
    tooltip = {i: i for i in columns}
    return tooltip


def set_tooltip_for_table(df):
    """
    Set the tooltip for the whole table
    """
    tooltip_data = [
        {
            column: {"value": str(value), "type": "markdown"}
            for column, value in row.items()
        }
        for row in df
    ]
    return tooltip_data


def set_conditional_style(columns):
    """
    Set the conditional style for certain columns
    """
    conditional_style = []
    for column in columns:
        if len(column["name"]) >= 20:
            condition = {
                "if": {"column_id": str(column["name"])},
                "width": "260px",
            }
            conditional_style.append(condition)
            continue
        elif len(column["name"]) >= 16:
            condition = {
                "if": {"column_id": str(column["name"])},
                "width": "220px",
            }
            conditional_style.append(condition)
            continue
        elif len(column["name"]) >= 12:
            condition = {
                "if": {"column_id": str(column["name"])},
                "width": "200px",
            }
            conditional_style.append(condition)
            continue
        else:
            condition = {
                "if": {"column_id": str(column["name"])},
                "width": "90px",
            }
            conditional_style.append(condition)
            continue
    return conditional_style


def set_table_style(columns, show_negative_numbers=False):
    """
    Set the table style
    """
    conditional_style = []
    for column in columns:
        if column["name"] == "Description":
            condition = {
                "if": {"column_id": str(column["name"])},
                "textAlign": "left",
                "width": "350px",
            }
            conditional_style.append(condition)
        else:
            condition = {
                "if": {"column_id": str(column["name"])},
                "textAlign": "right",
                "width": "120px",
            }
            conditional_style.append(condition)

        # Set red color for negative numbers
        if show_negative_numbers:
            condition = {
                "if": {
                    "filter_query": f"{{{column['id']}}} < 0",
                    "column_id": column["id"],
                },
                "backgroundColor": "#f8e6ec",
                "textAlign": "right",
            }
    return conditional_style


def set_table_style_kics(columns, show_negative_numbers=False):
    """
    Set the table style for K-ICS QIS reporting templates
    """
    conditional_style = []
    for column in columns:
        # Bypass pontential error for empty column names
        if len(column["id"]) == 0:
            continue

        # Set red color for negative numbers
        if show_negative_numbers:
            condition = {
                "if": {
                    "filter_query": f"{{{column['id']}}} < 0",
                    "column_id": column["id"],
                },
                "backgroundColor": "#f8e6ec",
                "textAlign": "right",
            }
            conditional_style.append(condition)

        # Align numbers to right (e.g. 100)
        condition = {
            "if": {
                "column_id": column["id"],
                "filter_query": f"{{{column['id']}}} >= 0",
            },
            "textAlign": "right",
        }

        conditional_style.append(condition)

        # Align percentage values to right (e.g. 100%)
        condition = {
            "if": {
                "column_id": column["id"],
                "filter_query": f"{{{column['id']}}} contains '%' && {{{column['id']}}} not contains ')'",
            },
            "textAlign": "right",
        }

        # Align values include "%" and parentheses to left (e.g. Text (100%))
        condition = {
            "if": {
                "column_id": column["id"],
                "filter_query": f"{{{column['id']}}} contains ')' || {{{column['id']}}} contains ')'",
            },
            "textAlign": "left",
        }

        conditional_style.append(condition)
    return conditional_style


def set_row_style(row_ids):
    """
    Set the row style
    """
    row_style = []
    for row_id in row_ids:
        condition = {
            "if": {"row_index": row_id},
            "backgroundColor": "#F4F6FC",
            "fontWeight": "bold",
        }
        row_style.append(condition)
    return row_style


def set_conditional_style_by_filtering(column, filter_value=0):
    """
    Set the conditional style for certain columns
    :param column: column name to be filtered by value (str)
    :param filter_value: value to be filtered out (int) (default: 0)
    :return: conditional style (list)
    """
    conditional_style = []
    condition = {
        "if": {
            "filter_query": f"{{{column}}} < '{filter_value}'",
            "column_id": column,
        },
        "backgroundColor": "#f8e6ec",
        # "color": "#f8e6ec",
        # "fontWeight": "bold",
    }
    conditional_style.append(condition)
    return conditional_style


def remove_substring(string):
    """
    Remove substring from string
    :param string: string
    :return: string
    """
    if "." in string and "~" not in string:
        string = string.split(".")[0]
    if "Unnamed" in string:
        string = ""
    return string
