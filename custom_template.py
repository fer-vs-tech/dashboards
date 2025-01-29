# Author: Kamoliddin Usmonov
# Date: 2022-06-20
# Custome template for CM Dashboards

custom_template = {
    "data": {
        "bar": [
            {
                "error_x": {"color": "#2a3f5f"},
                "error_y": {"color": "#2a3f5f"},
                "marker": {
                    "line": {"color": "white", "width": 0},
                    "pattern": {
                        "shape": "",
                        "fillmode": "overlay",
                        "fgopacity": 0.7,
                        "size": 5,
                        "solidity": 0.2,
                    },
                },
                "hoverlabel": {"bordercolor": "white"},
                "type": "bar",
            }
        ],
        "barpolar": [
            {
                "marker": {
                    "line": {"color": "white", "width": 0.5},
                    "pattern": {"fillmode": "overlay", "size": 10, "solidity": 0.2},
                },
                "type": "barpolar",
            }
        ],
        "carpet": [
            {
                "aaxis": {
                    "endlinecolor": "#2a3f5f",
                    "gridcolor": "#C8D4E3",
                    "linecolor": "#C8D4E3",
                    "minorgridcolor": "#C8D4E3",
                    "startlinecolor": "#2a3f5f",
                },
                "baxis": {
                    "endlinecolor": "#2a3f5f",
                    "gridcolor": "#C8D4E3",
                    "linecolor": "#C8D4E3",
                    "minorgridcolor": "#C8D4E3",
                    "startlinecolor": "#2a3f5f",
                },
                "type": "carpet",
            }
        ],
        "choropleth": [
            {"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}
        ],
        "contour": [
            {
                "colorbar": {"outlinewidth": 0, "ticks": ""},
                "colorscale": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "type": "contour",
            }
        ],
        "contourcarpet": [
            {"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}
        ],
        "heatmap": [
            {
                "colorbar": {"outlinewidth": 0, "ticks": ""},
                "colorscale": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "type": "heatmap",
            }
        ],
        "heatmapgl": [
            {
                "colorbar": {"outlinewidth": 0, "ticks": ""},
                "colorscale": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "type": "heatmapgl",
            }
        ],
        "histogram": [
            {
                "marker": {
                    "pattern": {"fillmode": "overlay", "size": 10, "solidity": 0.2}
                },
                "type": "histogram",
            }
        ],
        "histogram2d": [
            {
                "colorbar": {"outlinewidth": 0, "ticks": ""},
                "colorscale": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "type": "histogram2d",
            }
        ],
        "histogram2dcontour": [
            {
                "colorbar": {"outlinewidth": 0, "ticks": ""},
                "colorscale": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "type": "histogram2dcontour",
            }
        ],
        "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}],
        "parcoords": [
            {
                "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "parcoords",
            }
        ],
        "pie": [{"automargin": True, "type": "pie"}],
        "scatter": [
            {
                "fillpattern": {"fillmode": "overlay", "size": 10, "solidity": 0.2},
                "type": "scatter",
            }
        ],
        "scatter3d": [
            {
                "line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "scatter3d",
            }
        ],
        "scattercarpet": [
            {
                "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "scattercarpet",
            }
        ],
        "scattergeo": [
            {
                "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "scattergeo",
            }
        ],
        "scattergl": [
            {
                "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "scattergl",
            }
        ],
        "scattermapbox": [
            {
                "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "scattermapbox",
            }
        ],
        "scatterpolar": [
            {
                "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "scatterpolar",
            }
        ],
        "scatterpolargl": [
            {
                "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "scatterpolargl",
            }
        ],
        "scatterternary": [
            {
                "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                "type": "scatterternary",
            }
        ],
        "surface": [
            {
                "colorbar": {"outlinewidth": 0, "ticks": ""},
                "colorscale": [
                    [0.0, "#0d0887"],
                    [0.1111111111111111, "#46039f"],
                    [0.2222222222222222, "#7201a8"],
                    [0.3333333333333333, "#9c179e"],
                    [0.4444444444444444, "#bd3786"],
                    [0.5555555555555556, "#d8576b"],
                    [0.6666666666666666, "#ed7953"],
                    [0.7777777777777778, "#fb9f3a"],
                    [0.8888888888888888, "#fdca26"],
                    [1.0, "#f0f921"],
                ],
                "type": "surface",
            }
        ],
        "table": [
            {
                "cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}},
                "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}},
                "type": "table",
            }
        ],
    },
    "layout": {
        "annotationdefaults": {
            "arrowcolor": "#2a3f5f",
            "arrowhead": 0,
            "arrowwidth": 1,
        },
        "autotypenumbers": "strict",
        "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
        "colorscale": {
            "diverging": [
                [0, "#8e0152"],
                [0.1, "#c51b7d"],
                [0.2, "#de77ae"],
                [0.3, "#f1b6da"],
                [0.4, "#fde0ef"],
                [0.5, "#f7f7f7"],
                [0.6, "#e6f5d0"],
                [0.7, "#b8e186"],
                [0.8, "#7fbc41"],
                [0.9, "#4d9221"],
                [1, "#276419"],
            ],
            "sequential": [
                [0.0, "#0d0887"],
                [0.1111111111111111, "#46039f"],
                [0.2222222222222222, "#7201a8"],
                [0.3333333333333333, "#9c179e"],
                [0.4444444444444444, "#bd3786"],
                [0.5555555555555556, "#d8576b"],
                [0.6666666666666666, "#ed7953"],
                [0.7777777777777778, "#fb9f3a"],
                [0.8888888888888888, "#fdca26"],
                [1.0, "#f0f921"],
            ],
            "sequentialminus": [
                [0.0, "#0d0887"],
                [0.1111111111111111, "#46039f"],
                [0.2222222222222222, "#7201a8"],
                [0.3333333333333333, "#9c179e"],
                [0.4444444444444444, "#bd3786"],
                [0.5555555555555556, "#d8576b"],
                [0.6666666666666666, "#ed7953"],
                [0.7777777777777778, "#fb9f3a"],
                [0.8888888888888888, "#fdca26"],
                [1.0, "#f0f921"],
            ],
        },
        "colorway": [
            "#636efa",
            "#EF553B",
            "#00cc96",
            "#ab63fa",
            "#FFA15A",
            "#19d3f3",
            "#FF6692",
            "#B6E880",
            "#FF97FF",
            "#FECB52",
        ],
        "font": {"color": "#828282", "family": "Arial", "size": 12},
        "geo": {
            "bgcolor": "white",
            "lakecolor": "white",
            "landcolor": "white",
            "showlakes": True,
            "showland": True,
            "subunitcolor": "#C8D4E3",
        },
        "hoverlabel": {
            "align": "auto",
            "font": {"color": "white"},
            "bordercolor": "white",
        },
        "hovermode": "closest",  # x unified, x
        "mapbox": {"style": "light"},
        "paper_bgcolor": "#FFFFFF",
        "plot_bgcolor": "#E5ECF6",
        "polar": {
            "angularaxis": {
                "gridcolor": "#EBF0F8",
                "linecolor": "#EBF0F8",
                "ticks": "",
            },
            "bgcolor": "black",
            "radialaxis": {"gridcolor": "#EBF0F8", "linecolor": "#EBF0F8", "ticks": ""},
        },
        "scene": {
            "xaxis": {
                "backgroundcolor": "white",
                "gridcolor": "#DFE8F3",
                "gridwidth": 2,
                "linecolor": "#EBF0F8",
                "showbackground": True,
                "ticks": "",
                "zerolinecolor": "#EBF0F8",
            },
            "yaxis": {
                "backgroundcolor": "white",
                "gridcolor": "#DFE8F3",
                "gridwidth": 2,
                "linecolor": "#EBF0F8",
                "showbackground": True,
                "ticks": "",
                "zerolinecolor": "#EBF0F8",
            },
            "zaxis": {
                "backgroundcolor": "white",
                "gridcolor": "#DFE8F3",
                "gridwidth": 2,
                "linecolor": "#EBF0F8",
                "showbackground": True,
                "ticks": "",
                "zerolinecolor": "#EBF0F8",
            },
        },
        "shapedefaults": {"line": {"color": "#2a3f5f"}},
        "ternary": {
            "aaxis": {"gridcolor": "#DFE8F3", "linecolor": "#A2B1C6", "ticks": ""},
            "baxis": {"gridcolor": "#DFE8F3", "linecolor": "#A2B1C6", "ticks": ""},
            "bgcolor": "white",
            "caxis": {"gridcolor": "#DFE8F3", "linecolor": "#A2B1C6", "ticks": ""},
        },
        "title": {"x": 0, "font": {"size": 16, "color": "#2741BC"}},
        "xaxis": {
            "automargin": True,
            "color": "#828282",
            "gridcolor": "#F6F6F6",
            "linecolor": "#EBF0F8",
            "title": {
                "standoff": 30,
                "font": {"color": "#91A7DF", "family": "Arial", "size": 14},
            },
            "zerolinecolor": "#EBF0F8",
            "zerolinewidth": 2,
            # "spikesnap": "cursor",
            "spikemode": "toaxis+across+marker",
            "spikedash": "dot",
            # "spikecolor": "gray",
            "spikethickness": 2,
            # "tickangle": 45,
            "ticklabelposition": "outside",
            "tickcolor": "#828282",
            "ticklabelmode": "period",
            "ticks": "outside",
            "tickwidth": 1,
            "zeroline": True,
        },
        "yaxis": {
            "automargin": True,
            "color": "#828282",
            "gridcolor": "#F6F6F6",
            "linecolor": "#EBF0F8",
            "title": {
                "standoff": 30,
                "font": {"color": "#91A7DF", "family": "Arial", "size": 14},
            },
            "zerolinecolor": "#EBF0F8",
            "zerolinewidth": 2,
            # "spikesnap": "cursor",
            "spikemode": "toaxis+across+marker",
            "spikedash": "dot",
            # "spikecolor": "gray",
            "spikethickness": 2,
            # "tickangle": -45,
            "tickcolor": "#828282",
            "ticklabelmode": "period",
            "ticklabelposition": "outside",
            "ticks": "outside",
            "tickwidth": 1,
        },
        # "spikedistance": 0,
        # "hoverdistance": -1,
        "legend": {
            "itemclick": "toggle",
            "itemdoubleclick": "toggleothers",
            "orientation": "v",
            "title": {
                "font": {"color": "#828282", "family": "Arial", "size": 14},
                "side": "top",
            },
            # "tracegroupgap": 0,
            "orientation": "v",
            "valign": "middle",
            "x": 1.025,
            "y": 0.75,
            # "xanchor": "auto",
            # "yanchor": "top",
        },
        "autosize": False,
        "modebar": {
            # "bgcolor": "#F6F6F6",
            "activecolor": "#91A7DF",
            "color": "#E9EDF9",
            "add": [
                "togglehover",
                "togglespikelines",
                "v1hovermode",
                "hoverclosest",
                "hovercompare",
                "togglehover",
                "togglespikelines",
                "drawline",
                "drawopenpath",
                "drawclosedpath",
                "drawcircle",
                "drawrect",
                "eraseshape",
            ],
            "remove": ["pan2d", "reset3d"],
        },
        "uniformtext": {"minsize": 8, "mode": "hide"},
        "colorway": [
            "#7992FF",
            "#39C0BE",
            "#4364F7",
            "#F8981D",
            "#FA7F7F",
            "#FB78C9",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ],
    },
}
