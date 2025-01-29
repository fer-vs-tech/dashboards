from dash.dash_table.Format import Format, Scheme


def set_column_names(columns):
    """
    Apply the column names for the table
    """
    column_names = [
        {
            "name": i,
            "id": i,
            "type": "numeric",
            "deletable": False,
            "format": Format(group=",", precision=0, scheme=Scheme.fixed),
        }
        for i in columns
    ]
    return column_names


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
    return pivot


def string_to_int(s):
    s = s.strip()
    return int(s) if s else 0
