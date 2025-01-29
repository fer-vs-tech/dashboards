import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

import cm_dashboards.china_paa.utils.helpers as helpers


def generate_layout(title):
    """
    Dashboard layout
    """
    # Define reusable styles
    toast_style = {
        "position": "fixed",
        "bottom": 120,
        "right": 5,
        "width": 300,
        "zIndex": 10000,
    }

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
                    dcc.Input(
                        id="wvr_path",
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
                                                disabled=True,
                                            ),
                                        ],
                                    ),
                                ],
                                style={"text-decoration": "none"},
                            ),
                            dcc.Store(
                                id="calculated-results",
                                storage_type="memory",
                            ),
                            dcc.Store(
                                id="controllers-data",
                                storage_type="memory",
                            ),
                            dcc.Download(id="export-to-excel"),
                        ],
                    ),
                    html.Div(
                        children=[
                            dbc.Toast(
                                id="error-toast",
                                header="Error occurred",
                                is_open=False,
                                dismissable=True,
                                icon="danger",
                                style=toast_style,
                            ),
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
                                                                        "Opening Date"
                                                                    ),
                                                                    dcc.Loading(
                                                                        type="dot",
                                                                        color="#2741BC",
                                                                        children=[
                                                                            dcc.Dropdown(
                                                                                id="open-date-dropdown",
                                                                                placeholder="Select opening date ...",
                                                                                persistence=True,
                                                                                clearable=False,
                                                                                disabled=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            dbc.Col(
                                                                children=[
                                                                    html.B(
                                                                        "Reporting Date"
                                                                    ),
                                                                    dcc.Loading(
                                                                        type="dot",
                                                                        color="#2741BC",
                                                                        children=[
                                                                            dcc.Dropdown(
                                                                                id="report-date-dropdown",
                                                                                placeholder="Select reporting date ...",
                                                                                persistence=True,
                                                                                clearable=False,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            dbc.Col(
                                                                children=[
                                                                    html.B("Portfolio"),
                                                                    dcc.Loading(
                                                                        type="dot",
                                                                        color="#2741BC",
                                                                        children=[
                                                                            dcc.Dropdown(
                                                                                id="portfolio-dropdown",
                                                                                placeholder="Select portfolio ...",
                                                                                persistence=True,
                                                                                clearable=False,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            dbc.Col(
                                                                children=[
                                                                    html.B("Risk Type"),
                                                                    dcc.Loading(
                                                                        type="dot",
                                                                        color="#2741BC",
                                                                        children=[
                                                                            dcc.Dropdown(
                                                                                id="risk-type-dropdown",
                                                                                placeholder="Select risk type ...",
                                                                                persistence=True,
                                                                                clearable=False,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    dbc.Row(
                                                        children=[
                                                            dbc.Col(
                                                                children=[
                                                                    html.B("Grp Type"),
                                                                    dcc.Loading(
                                                                        type="dot",
                                                                        color="#2741BC",
                                                                        children=[
                                                                            dcc.Dropdown(
                                                                                id="grp-type-dropdown",
                                                                                placeholder="Select grp type ...",
                                                                                persistence=True,
                                                                                clearable=False,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            dbc.Col(
                                                                children=[
                                                                    html.B(
                                                                        "Inception Year"
                                                                    ),
                                                                    dcc.Loading(
                                                                        type="dot",
                                                                        color="#2741BC",
                                                                        children=[
                                                                            dcc.Dropdown(
                                                                                id="inception-year-dropdown",
                                                                                placeholder="Select inception year ...",
                                                                                persistence=True,
                                                                                clearable=False,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            dbc.Col(
                                                                children=[
                                                                    html.B("Model"),
                                                                    dcc.Loading(
                                                                        type="dot",
                                                                        color="#2741BC",
                                                                        children=[
                                                                            dcc.Dropdown(
                                                                                id="model-dropdown",
                                                                                placeholder="Select model ...",
                                                                                persistence=True,
                                                                                clearable=False,
                                                                            ),
                                                                        ],
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
                            dcc.Loading(
                                id="main-loading",
                                type="dot",
                                color="#2741BC",
                                loading_state={
                                    "is_loading": False,
                                },
                                children=[
                                    html.Div(
                                        className="body-content",
                                        style={"height": "57vh"},
                                        children=[
                                            html.Div(
                                                id="dashboards",
                                                children=[
                                                    html.Div(
                                                        className="text-center",
                                                        style={
                                                            "display": "flex",
                                                            "justify-content": "center",
                                                            "align-items": "center",
                                                            "height": "50vh",
                                                        },
                                                        children="No data to display. Please select the reporting date and group ID.",
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

def render_custom_triangle(dashboard_results):
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


    # Loop through the results and generate dashboard layout
    results = []

    label = f"Dashboard fer"
    results.append(
                        dash_table.DataTable(
                            id=f"tri-table",
                            data=dashboard_results[0],
                            columns=dashboard_results[1],
                            style_data_conditional=dashboard_results[2],
                            style_table=table_style,
                            merge_duplicate_headers=True,
                            cell_selectable=False,
                        )
                )

    layout = results

    return layout


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
    # Loop through the results and generate dashboard layout
    results = []
    for i, (dash_id, dash_results) in enumerate(dashboard_results.items(), start=1):
        label = dashboard_details[dash_id].get("label", f"Dashboard {i}")
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
                                data=dash_results[0],
                                columns=dash_results[1],
                                style_data_conditional=dash_results[2],
                                style_table=table_style,
                                merge_duplicate_headers=True,
                                cell_selectable=False,
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

    return layout


def render_error(error_message):
    """
    Render message if error occurred
    """
    return html.Div(
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
