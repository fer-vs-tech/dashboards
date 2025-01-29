#layout_loader IFRS17

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

from dash import Dash, dcc, html, Input, Output, State, callback, Patch, clientside_callback
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import dash_ag_grid as dag

df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()

# stylesheet with the .dbc class to style  dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

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

    color_mode_switch = html.Span(
        [
            dbc.Label(className="fa fa-moon", html_for="switch"),
            dbc.Switch(id="switch", value=True, className="d-inline-block ms-1", persistence=True),
            dbc.Label(className="fa fa-sun", html_for="switch"),
        ]
    )

    # The ThemeChangerAIO loads all 52  Bootstrap themed figure templates to plotly.io
    theme_controls = html.Div(
        [ThemeChangerAIO(aio_id="theme"), color_mode_switch],
        className="hstack gap-3 mt-2"
    )

    header = html.H4(
        "Theme Explorer Sample App", className="bg-primary text-white p-2 mb-2 text-center"
    )

    grid = dag.AgGrid(
        id="grid",
        columnDefs=[{"field": i} for i in df.columns],
        rowData=df.to_dict("records"),
        defaultColDef={"flex": 1, "minWidth": 120, "sortable": True, "resizable": True, "filter": True},
        dashGridOptions={"rowSelection": "multiple"},
    )

    dropdown = html.Div(
        [
            dbc.Label("Select indicator (y-axis)"),
            dcc.Dropdown(
                ["gdpPercap", "lifeExp", "pop"],
                "pop",
                id="indicator",
                clearable=False,
            ),
        ],
        className="mb-4",
    )

    checklist = html.Div(
        [
            dbc.Label("Select Continents"),
            dbc.Checklist(
                id="continents",
                options=continents,
                value=continents,
                inline=True,
            ),
        ],
        className="mb-4",
    )

    slider = html.Div(
        [
            dbc.Label("Select Years"),
            dcc.RangeSlider(
                years[0],
                years[-1],
                5,
                id="years",
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                value=[years[2], years[-2]],
                className="p-0",
            ),
        ],
        className="mb-4",
    )
    theme_colors = [
        "primary",
        "secondary",
        "success",
        "warning",
        "danger",
        "info",
        "light",
        "dark",
        "link",
    ]
    colors = html.Div(
        [dbc.Button(f"{color}", color=f"{color}", size="sm") for color in theme_colors]
    )
    colors = html.Div(["Theme Colors:", colors], className="mt-2")

    controls = dbc.Card(
        [dropdown, checklist, slider],
        body=True,
    )

    tab1 = dbc.Tab([dcc.Graph(id="line-chart", figure=px.line(template="bootstrap"))], label="Line Chart")
    tab2 = dbc.Tab([dcc.Graph(id="scatter-chart", figure=px.scatter(template="bootstrap"))], label="Scatter Chart")
    tab3 = dbc.Tab([grid], label="Grid", className="p-4")
    tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))

    main_layout = dbc.Container(
    [
        header,
        dbc.Row([
            dbc.Col([
                controls,
                # ************************************
                # Uncomment line below when running locally!
                # ************************************
                # theme_controls
            ],  width=4),
            dbc.Col([tabs, colors], width=8),
        ]),
    ],
    fluid=True,
    className="dbc dbc-ag-grid",
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
