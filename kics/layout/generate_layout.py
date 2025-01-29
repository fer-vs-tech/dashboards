"""
This module contains functions for generating the layout for dashboards
:author: Kamoliddin Usmonov
:date: 2023-06-02
"""

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html


def generate_dashboard_layout(dashboard_data, results):
    """
    Generate layout for dashboard
    :param dashboard_data: Dashboard data (label, dashboard count, handler)
    :param results: Dashboard results (data, columns, style_data_conditional)
    :return: Layout for dashboard
    """
    # Get default layout elements
    (
        class_name,
        style_table,
        style_cell,
        merge_duplicate_headers,
    ) = get_default_layout_elements()

    # Check if there is only one dashboard
    if dashboard_data.get("dashboard_count", 0) == 1:
        # Generate layout without inner dashboards
        layout = get_layout_without_inner_dashboards(
            dashboard_data,
            results,
            class_name,
            style_table,
            style_cell,
            merge_duplicate_headers,
        )
    else:
        # Generate layout with inner dashboards
        layout = get_layout_with_inner_dashboards(
            dashboard_data, results, class_name, style_table, style_cell
        )

    return layout


def get_default_layout_elements():
    """
    Get default layout elements
    :return: Default class name, table style, cell style, and merge_duplicate_headers value
    """
    class_name = "one-half column mixed-table"
    style_table = {
        "overflowX": "auto",
        "minWidth": "100%",
    }
    style_cell = {"textAlign": "left"}
    merge_duplicate_headers = False
    return class_name, style_table, style_cell, merge_duplicate_headers


def get_layout_without_inner_dashboards(
    dashboard_data,
    results,
    class_name,
    style_table,
    style_cell,
    merge_duplicate_headers,
):
    """
    Generate layout for dashboard without inner dashboards
    :param dashboard_data: Dashboard data (label, dashboard count, handler)
    :param results: Dashboard results (data, columns, style_data_conditional)
    :param class_name: Class name for the dashboard
    :param style_table: Table style for the dashboard
    :param style_cell: Cell style for the dashboard
    :param merge_duplicate_headers: Whether to merge duplicate headers
    :return: Layout for dashboard without inner dashboards
    """
    # Check if we should merge duplicate headers
    if dashboard_data.get("merge_duplicate_headers", False):
        merge_duplicate_headers = True
        class_name += " merged-header"
        style_table["maxHeight"] = "350px"
        style_cell = {
            "minWidth": "150px",
            "width": "150px",
            "textAlign": "left",
        }

    # Check if we should merge duplicate cells
    if dashboard_data.get("merge_duplicate_cells", False):
        class_name += " merged-cell"

    # Get results data, columns, and style
    data, columns, style = results

    # Generate layout
    layout = (
        html.Div(
            className=class_name,
            children=[
                html.Label(dashboard_data["label"]),
                dash_table.DataTable(
                    id="dashboard-table",
                    export_format="xlsx",
                    is_focused=False,
                    merge_duplicate_headers=merge_duplicate_headers,
                    page_size=400,
                    data=data,
                    columns=columns,
                    style_data_conditional=style,
                    style_table=style_table,
                    style_cell=style_cell,
                ),
            ],
        ),
    )
    return layout


def get_layout_with_inner_dashboards(
    dashboard_data, results, class_name, style_table, style_cell
):
    """
    Generate layout for dashboard with inner dashboards
    :param dashboard_data: Dashboard data (label, dashboard count, handler)
    :param results: Dashboard results (data, columns, style_data_conditional)
    :param class_name: Class name for the dashboard
    :param style_table: Table style for the dashboard
    :param style_cell: Cell style for the dashboard
    :return: Layout for dashboard with inner dashboards
    """
    # Get child dashboard names and results
    child_dashboard_names = list(dashboard_data.get("child_dashboards").keys())
    dashboard_layouts = []
    class_name_inner = ""

    # Loop through child dashboard results
    for i, result in enumerate(results):
        child_dashboard_id = child_dashboard_names[i]
        data, columns, style = result
        child_dashboard = dashboard_data["child_dashboards"].get(child_dashboard_id)

        # Check if we should merge duplicate headers and cells
        if child_dashboard is None:
            merge_duplicate_headers = dashboard_data.get(
                "merge_duplicate_headers", False
            )
            merge_duplicate_cells = dashboard_data.get("merge_duplicate_cells", False)

        else:
            merge_duplicate_headers = child_dashboard.get(
                "merge_duplicate_headers", False
            )
            merge_duplicate_cells = child_dashboard.get("merge_duplicate_cells", False)

        # Check if we should merge duplicate headers
        if merge_duplicate_headers:
            class_name_inner = "merged-header"
            style_table["maxHeight"] = "350px"
            style_cell = {
                "minWidth": "130px",
                "width": "180px",
                "textAlign": "left",
            }

        # Check if we should merge duplicate cells
        if merge_duplicate_cells:
            class_name_inner += " merged-cell"

        # Generate layout for child dashboard
        item = html.Div(
            className=class_name_inner,
            children=[
                html.Label(child_dashboard_id),
                dash_table.DataTable(
                    id=f"dashboard-{child_dashboard_id}-table",
                    export_format="xlsx",
                    merge_duplicate_headers=merge_duplicate_headers,
                    page_size=400,
                    data=data,
                    columns=columns,
                    style_data_conditional=style,
                    style_table=style_table,
                    style_cell=style_cell,
                ),
            ],
        )
        dashboard_layouts.append(item)

    # Generate layout for dashboard with inner dashboards
    layout = (
        html.Div(
            className=class_name,
            children=[
                html.Label(dashboard_data.get("label")),
                html.Div(
                    children=dashboard_layouts,
                ),
            ],
        ),
    )
    return layout


def generate_tabs(dashboard_data):
    """
    Generates the tabs for the main layout based on the dashboard data.
    """
    # Loop through the dashboard data and create a tab for each one
    tabs = list()
    for id, data in dashboard_data.items():
        label = data.get("id")
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


def generate_main_layout(dashboard_data):
    """
    Generates the main layout for the KICS dashboards.
    """
    # Main layout
    layout = dbc.Container(
        fluid="md",
        className="dbc",
        children=[
            dcc.Location(id="url", refresh=True),
            html.Div(
                className="logo-container",
                children=[
                    html.Img(src="/dash/static/assets/wm_logo.svg"),
                ],
            ),
            html.Div(
                style={"display": "none"},
                children=[
                    dcc.Input(
                        id="kics-name",
                        value="",
                        placeholder="",
                    ),
                    dcc.Input(
                        id="kics-path",
                        value="",
                        placeholder="",
                    ),
                    dcc.Input(
                        id="transition-path",
                        value="",
                        placeholder="",
                    ),
                    dcc.Input(
                        id="sensitivity-path",
                        value="",
                        placeholder="",
                    ),
                    dcc.Input(
                        id="kics-model-name",
                        value="",
                        placeholder="",
                    ),
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
                                children="K-ICS QIS reporting dashboards",
                                style={"text-decoration": "none"},
                            ),
                        ],
                    ),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="report-date-dropdown",
                                placeholder="Select report date",
                                persistence=True,
                                clearable=True,
                            ),
                            html.Br(),
                            dbc.Tabs(
                                id="tabs",
                                active_tab="tab-0",
                                children=generate_tabs(dashboard_data),
                            ),
                            dcc.Loading(
                                id="dashboard-loading",
                                type="default",
                                color="#2741BC",
                                children=[
                                    html.Div(
                                        className="body-content",
                                        style={"height": "57vh"},
                                        id="dashboard-data",
                                    ),
                                ],
                            ),
                            html.Div(id="blank-output"),
                        ],
                    ),
                ],
            ),
        ],
    )

    return layout
