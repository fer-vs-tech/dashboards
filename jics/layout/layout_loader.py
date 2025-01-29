import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html


def generate_tabs(dashboard_data):
    """
    Generates the tabs for the main layout based on the dashboard data.
    :param dashboard_data: The dashboard data
    :return tabs: List of tabs for the main layout
    """
    # Loop through the dashboard data and create a tab for each one
    tabs = list()
    for id, data in dashboard_data.items():
        label = data.get("label")
        tab = dbc.Tab(
            id=id,
            tab_id=id,
            label=label,
            tab_class_name="unactive-tab",
            label_class_name="unactive-tab-label",
            active_tab_class_name="active-tab",
            active_label_class_name="active-tab-label",
        )
        tabs.append(tab)

    return tabs


def generate_main_layout(title, dashboard_data):
    """
    Generates the main layout for the dashboard.
    :param title: The title of the dashboard
    :param dashboard_data: The dashboard data
    :return: The main layout
    """
    main_layout = dbc.Container(
        fluid="md",
        className="dbc",
        children=[
            html.Div(
                className="logo-container",
                children=[
                    html.Img(src="/dash/static/assets/wm_logo.svg"),
                ],
            ),
            html.Div(
                style={"display": "none"},
                children=[
                    dcc.Location(id="url", refresh=True),
                    dcc.Input(
                        id="wvr-path",
                        value="",
                        placeholder="",
                    ),
                    dcc.Input(
                        id="model-name",
                        value="",
                        placeholder="",
                    ),
                    dcc.Store(id="results-store"),
                    dcc.Download(id="export-to-excel"),
                ],
            ),
            html.Div(
                className="body-container",
                children=[
                    html.Div(
                        className="title-container",
                        children=[
                            html.Div(
                                id="journal-title",
                                children=title,
                                style={"text-decoration": "none"},
                            ),
                        ],
                    ),
                    dcc.Loading(
                        id="app-loading-state",
                        type="default",
                        color="#2741BC",
                        fullscreen=False,
                        children=[
                            html.Div(
                                children=[
                                    dbc.Toast(
                                        id="error-toast",
                                        header="Error occurred",
                                        is_open=False,
                                        dismissable=True,
                                        icon="danger",
                                        style={
                                            "position": "fixed",
                                            "bottom": 120,
                                            "right": 5,
                                            "width": 300,
                                            "zIndex": 10000,
                                        },
                                    ),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                children=[
                                                    dcc.Dropdown(
                                                        id="report-date-dropdown",
                                                        placeholder="Select report date",
                                                        persistence=True,
                                                        clearable=True,
                                                    ),
                                                ],
                                                width=3,
                                            ),
                                            dbc.Col(
                                                children=[
                                                    html.Div(
                                                        children=[
                                                            html.A(
                                                                id="export-link",
                                                                target="_blank",
                                                                children=[
                                                                    html.Button(
                                                                        "Bundle Reports",
                                                                        id="export-link-button",
                                                                        className="export",
                                                                        disabled=True,
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                        className="export-button-container",
                                                        style={
                                                            "margin-bottom": "4px !important",
                                                            "padding": "0px",
                                                        },
                                                    ),
                                                ],
                                            ),
                                        ],
                                        style={"margin-bottom": "30px"},
                                    ),
                                    dbc.Tabs(
                                        id="tabs",
                                        active_tab="tab_1",
                                        children=generate_tabs(dashboard_data),
                                    ),
                                    html.Div(
                                        className="body-content",
                                        style={"height": "52vh"},
                                        id="dashboard-data",
                                    ),
                                    html.Div(id="blank-output"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    return main_layout


def generate_toast_message(
    messages: list[str], icon: str = "danger"
) -> list[dbc.Toast]:
    """
    Generate toast messages for error messages

    :param message: Message to display
    :param icon:  Class name (default: danger)
    :return: List of toast messages (dbc.Toast)
    """
    toast_messages: list[dbc.Toast] = list()

    # Check if messages is a list
    if not isinstance(messages, list):
        messages = [messages]

    # Generate toast messages for each message with different duration
    for i, (header, message) in enumerate(messages, start=1):
        duration = 8000
        toast_messages.append(
            dbc.Toast(
                message,
                header=header,
                is_open=True,
                dismissable=True,
                duration=duration * i,
                icon=icon,
                style={
                    "position": "fixed",
                    "bottom": 120,
                    "right": 5,
                    "width": 300,
                    "zIndex": 10000,
                },
            )
        )

    return toast_messages


def generate_ordinary_dashboard(dashboard_data, results):
    """
    Generate layout for dashboard table
    :param dashboard_data: Dashboard data (label, dashboard count, handler)
    :param results: Dashboard results (data, columns, style_data_conditional)
    :return: Layout for dashboard table
    """
    # Get default style properties
    style_table, style_cell = get_default_style()

    data, columns, style = results
    merge_duplicate_headers = dashboard_data.get("merge_duplicate_headers", False)
    merge_duplicate_cells = dashboard_data.get("merge_duplicate_cells", False)

    # Check if table has multi-level columns
    class_name = "jics one-half column mixed-table"
    if merge_duplicate_headers:
        class_name += " merged-header"
        style_table["maxHeight"] = "350px"
        style_cell = dict(minWidth="150px", width="150px", textAlign="left")

    # Check if table has merged cells
    if merge_duplicate_cells:
        class_name += " merged-cell"

    dashboard_id = dashboard_data.get("id")
    layout = html.Div(
        className=class_name,
        children=[
            html.Label(dashboard_id),
            dash_table.DataTable(
                id=f"dashboard-{dashboard_id}-table",
                export_format="xlsx",
                merge_duplicate_headers=merge_duplicate_headers,
                page_size=400,
                data=data,
                columns=columns,
                style_data_conditional=style,
                style_table=style_table,
                style_cell=style_cell,
                cell_selectable=False,
            ),
        ],
    )

    return layout


def generate_child_dashboard(dashboard_id, dashboard_data, result):
    """
    Generate layout for dashboard
    :param dashboard_id: Dashboard ID
    :param dashboard_data: Dashboard data (label, dashboard count, handler)
    :param result: Dashboard result (data, columns, style_data_conditional)
    :return: Layout for dashboard
    """
    data, columns, style = result
    merge_duplicate_headers = dashboard_data.get("merge_duplicate_headers", False)
    merge_duplicate_cells = dashboard_data.get("merge_duplicate_cells", False)

    # Get default style properties
    style_table, style_cell = get_default_style()

    # Detect if table has multi-level columns
    class_name = "jics"
    if merge_duplicate_headers:
        class_name += " merged-header"
        style_table["maxHeight"] = "350px"
        style_cell = dict(minWidth="130px", width="180px", textAlign="left")

    # Add classname to detect in JS for merging cells
    if merge_duplicate_cells:
        class_name += " merged-cell"

    layout = html.Div(
        className=class_name,
        children=[
            (
                html.Label(dashboard_id)
                if dashboard_id != "HEADER" and "-" not in dashboard_id
                else None
            ),
            dash_table.DataTable(
                id=f"dashboard-{dashboard_id}-table",
                export_format="xlsx",
                merge_duplicate_headers=merge_duplicate_headers,
                page_size=400,
                data=data,
                columns=columns,
                style_data_conditional=style,
                style_table=style_table,
                style_cell=style_cell,
                cell_selectable=False,
            ),
            html.Br(),
        ],
    )

    return layout


def get_default_style():
    """
    Get default style properties for dashboard.
    :return: Default style properties for dashboard (style_table, style_cell)
    """
    # Define default style properties
    style_table = dict(overflowX="auto", minWidth="100")
    style_cell = dict(textAlign="left")
    return style_table, style_cell


def generate_dashboard_layout(dashboard_data, results, error_messages):
    """
    Generate layout for dashboard
    :param dashboard_data: Dashboard data (label, dashboard count, handler)
    :param results: Dashboard results (data, columns, style_data_conditional)
    :param error_messages: List of error messages
    :return: Layout for dashboard
    """
    toast_messages = generate_toast_message(error_messages)

    # Return layout without inner dashboards (ordinary)
    if dashboard_data.get("child_dashboards") is None:
        layout = generate_ordinary_dashboard(dashboard_data, results)

    # Generate layout with inner dashboards (dynamic)
    else:
        child_dashboards = dashboard_data.get("child_dashboards")
        dashboard_layouts = []

        for dashboard_id, result in results:
            child_dashboard = child_dashboards.get(dashboard_id)
            layout = generate_child_dashboard(dashboard_id, child_dashboard, result)
            dashboard_layouts.append(layout)

        layout = html.Div(
            className="one-half column mixed-table",
            children=[
                html.Div(toast_messages),
                html.Div(
                    children=dashboard_layouts,
                ),
            ],
        )

    return layout
