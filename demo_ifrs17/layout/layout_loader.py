#layout_loader IFRS17

import dash_bootstrap_components as dbc
from dash import dcc, html
import cm_dashboards.demo_ifrs17.layout.component_styles as styles
import cm_dashboards.demo_ifrs17.layout.modal_filters as modal_filters
import cm_dashboards.demo_ifrs17.layout.main_menu as main_menu



accordion_menu_reins = html.Div(
    dbc.Accordion(id="acc-reins",
                children="",
                start_collapsed=True,
                always_open=True,
                flush=True,
    ),style={"overflow": "auto","max-height": "600px"}
)



def generate_layout(title):
    """
    Generates the main layout for the dashboard.
    :param title: The title of the dashboard
    :param dashboard_data: The dashboard data
    :return: The main layout
    """
    FIGURE_CONFIG = {
        "displaylogo": False,
        "displayModeBar": False,
    }

    FIGURE_STYLE = {
        "height": "500px",
    }

    PIE_CHART_STYLE = {
        "height": "200px",
        "width": "100%",
    }

    BAR_CHART_STYLE = {
        "height": "304px",
        "width": "90%",
    }

    LONGER_BAR_CHART_STYLE = {
        "height": "383px",
        "width": "90%",
    }

    # Table styles
    style_table = dict(overflowX="auto", minWidth="100", maxHeight="380px")
    style_cell = dict(minWidth="130px", width="180px", textAlign="left")

    main_layout = dbc.Container(
        className="dbc",
        children=[
            html.Div(
                className="logo",
                children=[
                    dcc.Location(id="url", refresh=True),
                      dcc.Store(
                        id="wvr_files",
                        storage_type="session",
                    ),
                    dcc.Store(
                        id="variables_key_value",
                        storage_type="session",
                    ),
                     dcc.Store(
                        id="breakdowns_key_value",
                        storage_type="session",
                    ),
                    dcc.Store(
                        id="disclosures_key_value",
                        storage_type="session",
                    ),
                    html.Img(src="/dash/static/assets/wm_logo.svg"),
                    html.Div(
                        className="logo-text", children=title
                    ),
                ],
            ),
            dcc.Location(id="url", refresh=True),
            html.Div(
                style={"padding":"10px"},
                className="body-container",
                id="body-container",
                children=[
                    modal_filters.filters,
                    dcc.Loading(
                        type="dot",
                        color="#2741BC",
                        children=[
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    html.B(
                                        "BBA Model",
                                        style=styles.label_style,
                                    ),
                                    dcc.Dropdown(
                                        id="bba-model-dropdown",
                                        placeholder="Select BBA Model ...",
                                        persistence=True,
                                        clearable=False,
                                        # disabled=True,
                                        style={
                                            "width": 300,
                                            #"height": "2px",
                                            "font-size": 12,
                                            "fontWeight": "normal",
                                        }
                                    ),
                                ],
                                width=3,
                            ),
                            dbc.Col(
                                children=[
                                    html.B(
                                        "PAA Model",
                                        style = styles.label_style,
                                    ),
                                    dcc.Dropdown(
                                        id="paa-model-dropdown",
                                        placeholder="Select PAA ...",
                                        persistence=True,
                                        clearable=False,
                                        # disabled=True,
                                        style={
                                            "width": 300,
                                            #"height": "2px",
                                            "font-size": 12,
                                            "fontWeight": "normal",
                                        }
                                    ),
                                ],
                                width=3,
                            ),
                            dbc.Col(
                                children=[
                                    html.B(
                                        "Reporting Date",
                                        style=styles.label_style,
                                    ),
                                    dcc.Dropdown(
                                        id="steps-dropdown",
                                        placeholder="Select Date ...",
                                        persistence=True,
                                        clearable=False,
                                        style={
                                            "width": 200,
                                            #"height": "2px",
                                            "font-size": 12,
                                            "fontWeight": "normal",
                                        }
                                        # disabled=True,
                                    ),
                                    ],
                                width=2,
                            ),
                            dbc.Col(
                                children=[
                                    dbc.Button(
                                        [
                                        "Filters ",
                                        dbc.Badge(id="filter-count", children="0", color="primary", text_color="light"),
                                        ],
                                        id="btn-filters",
                                        color="primary",
                                        outline=True,
                                        n_clicks=0,
                                        style={
                                            "height": "70%",
                                            "width": 125,
                                            # "width": "100%",
                                            "margin-top": "12px",
                                        },
                                    )
                                ],
                                width=2,
                                align="end",
                            ),
                            dbc.Col(
                                children=[
                                    dbc.Button(
                                        "Show Results",
                                        id="apply-button",
                                        #className="sm-2",
                                        class_name="chulo-btn",
                                        n_clicks=0,
                                        style={
                                            "height": "70%",
                                            "width": 200,
                                            #"width": "100%",
                                            "margin-top": "12px",
                                        },
                                    ),
                                ],
                                width=2,
                                align="end",
                            ),
                        ],
                    ),
                            #html.Hr(),
                            html.Div(id='row-filters-div',children=[dbc.Stack(id='row-filters',
                                                                              direction="horizontal",
                                                                              gap=2)],style={'padding-left':'10px',
                                                                                             'padding-top':'15px',
                                                                                             'display':'inline-block'}
                    )
                        ], #loading
            ),
                    html.Hr(),
                    dcc.Loading(
                        type="dot",
                        color="#2741BC",
                        children=[
                            main_menu.main
                    ],
            ),
            dbc.Toast(
                id="error-toast",
                header="Error occurred",
                is_open=False,
                dismissable=True,
                icon="danger",
                style={
                    "position": "fixed",
                    "top": 84,
                    "right": 10,
                    "width": 290,
                },
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
