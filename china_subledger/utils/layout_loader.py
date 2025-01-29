import logging

logger = logging.getLogger(__name__)

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

import cm_dashboards.china_subledger.utils.helpers as helpers


def generate_layout(title):
    """
    Dashboard layout
    """

    return dbc.Container(
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
                    dcc.Input(id="wvr_path"),
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
                                children=[
                                    title,
                                    html.A(
                                        target="_blank",
                                        download="yes",
                                        children=[
                                            html.Button(
                                                "Bundle Reports",
                                                id={
                                                    "type": "export-data-button",
                                                    "index": "export-data-button",
                                                },
                                                className="export",
                                            ),
                                        ],
                                    ),
                                ],
                                style={"text-decoration": "none"},
                            ),
                        ],
                    ),
                    dcc.Loading(
                        id="main-loading",
                        type="dot",
                        color="#2741BC",
                        loading_state={
                            "is_loading": False,
                        },
                        children=[
                            html.Div(
                                children=[
                                    dbc.Accordion(
                                        id="controllers",
                                        start_collapsed=False,
                                        children=[
                                            dbc.AccordionItem(
                                                title="Controllers",
                                                children=[
                                                    html.Div(
                                                        children=[
                                                            dbc.Row(
                                                                children=[
                                                                    dbc.Col(
                                                                        children=[
                                                                            html.B(
                                                                                "Previous Report Date"
                                                                            ),
                                                                            dcc.Dropdown(
                                                                                id="previous-report-date-dropdown",
                                                                                disabled=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        children=[
                                                                            html.B(
                                                                                "Report Date"
                                                                            ),
                                                                            dcc.Dropdown(
                                                                                id="report-date-dropdown",
                                                                                disabled=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        children=[
                                                                            html.B(
                                                                                "Group ID"
                                                                            ),
                                                                            dcc.Dropdown(
                                                                                id="group-id-dropdown",
                                                                                placeholder="Select group ID ...",
                                                                                persistence=True,
                                                                                clearable=False,
                                                                                disabled=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        children=[
                                                                            dbc.Button(
                                                                                "Show Results",
                                                                                id="apply-button",
                                                                                className="me-2",
                                                                                n_clicks=0,
                                                                                disabled=True,
                                                                                style={
                                                                                    "height": "57%",
                                                                                    "width": "100%",
                                                                                    "margin-top": "24px",
                                                                                },
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    dcc.Store(id="model_results"),
                                    dcc.Store(id="assumptions"),
                                    dcc.Download(id="export-to-excel"),
                                    html.Div(
                                        className="body-content",
                                        style={"height": "57vh"},
                                        children=[
                                            html.Div(
                                                id="dashboards",
                                                children=[
                                                    html.Div(
                                                        style={
                                                            "display": "flex",
                                                            "justify-content": "center",
                                                            "align-items": "center",
                                                            "height": "50vh",
                                                        },
                                                        className="text-center",
                                                        children=[
                                                            "No data to display, please select any group ID and click 'Show Results' button to populate results",
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def render_dashboards(dashboard_results):
    """
    Render dashboards based on the results
    """
    table_style = {
        "overflowX": "auto",
        "minWidth": "100%",
        "maxWidth": "100%",
        "width": "100%",
        "maxHeight": "500px",
        "height": "300px",
    }
    dashboard_details = helpers.dashboards_list()
    results = []
    for i, (dash_id, dash_results) in enumerate(dashboard_results.items(), start=1):
        if dash_id in ["validation_table", "missing_mappings"]:
            continue

        label = dashboard_details[dash_id].get("label", f"Dashboard {i}")
        prepared_table_data = dash_results.get("table_data")
        if not prepared_table_data:
            logger.warning(f"Table data is missing for dashboard: {dash_id}")
            continue

        results.append(
            dbc.Tab(
                label=label,
                tab_class_name="unactive-tab",
                label_class_name="unactive-tab-label",
                active_tab_class_name="active-tab",
                active_label_class_name="active-tab-label",
                children=[
                    html.Div(
                        className="merged-header",
                        children=[
                            html.Label(id="main-label"),
                            html.Br(),
                            dash_table.DataTable(
                                id=f"{dash_id}-table",
                                data=prepared_table_data[0],
                                columns=prepared_table_data[1],
                                style_data_conditional=prepared_table_data[2],
                                style_table=table_style,
                                merge_duplicate_headers=True,
                                cell_selectable=False,
                                export_format="xlsx",
                            ),
                        ],
                    ),
                ],
            ),
        )

    layout = [
        dbc.Tabs(
            children=results,
            active_tab="tab-0",
        ),
    ]

    if dashboard_results["missing_mappings"]:
        error_toast = generate_toast_message(dashboard_results["missing_mappings"])
        layout.append(error_toast)

    return layout


def render_error(error_message):
    """
    Render message if error occurred
    """
    return [
        html.Div(
            className="one-half column mixed-table row",
            children=[
                html.Label(id="main-label"),
                html.Br(),
                html.Div(
                    className="alert alert-danger",
                    role="alert",
                    children=[
                        html.P(
                            children=[
                                html.B("Failed to load the data"),
                                html.Br(),
                                html.Span(error_message),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ]


def generate_toast_message(messages: list[str], icon: str = "danger") -> dbc.Toast:
    """
    Generate toast messages for error messages

    :param message: Message to display
    :param icon:  Class name (default: danger)
    :return: List of toast messages (dbc.Toast)
    """
    if not isinstance(messages, list):
        messages = [messages]

    children = [
        html.Div("The subledger mappings are not found in the variable mappings:"),
        html.Div(style={"margin-bottom": "8px"}),
    ]
    for i, message in enumerate(messages, start=1):
        child = html.Div(f"{i}) {message}")
        children.append(child)

    return dbc.Toast(
        children,
        header="Error occured",
        is_open=True,
        dismissable=True,
        duration=10000,
        icon=icon,
        style={
            "position": "fixed",
            "bottom": 120,
            "right": 30,
            "width": 350,
            "zIndex": 10000,
            "background": "#FFFFFF",
        },
    )
