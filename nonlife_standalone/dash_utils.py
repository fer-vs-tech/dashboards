from dash.dash_table.Format import Format, Scheme, Sign


def set_column_names(
    columns, precision=0, show_negative_numbers=False, additional_header=None
):
    """
    Apply the column names for the table
    """
    default_sign = Sign.negative if show_negative_numbers else Sign.parantheses
    column_names = [
        {
            "name": [additional_header, column] if additional_header else column,
            "id": f"{additional_header}_{i}",
            "type": "numeric",
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


def set_parameterization_column_names(
    dataframe, precision=0, show_negative_numbers=False, additional_header=None
):
    """
    Apply the column names for the table
    """
    default_sign = Sign.negative if show_negative_numbers else Sign.parantheses
    dist_values = dataframe.iloc[:, 0].to_list()
    distribution_lrc = dataframe.iloc[:, 1].to_list()
    column_names = [
        {
            "name": [additional_header, dist_values[i], str(distribution_lrc[i])]
            if additional_header
            else column,
            "id": f"{additional_header}_{i}",
            "type": "numeric",
            "deletable": False,
            "format": Format(
                group=",", precision=precision, scheme=Scheme.fixed, sign=default_sign
            )
            if i != 0
            else Format(
                group=",", precision=precision, scheme=Scheme.fixed, sign=default_sign
            ),
        }
        for i, column in enumerate(dataframe.columns)
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
    # print(pivot)

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
