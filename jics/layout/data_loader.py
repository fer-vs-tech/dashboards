"""
Author: Kamoliddin Usmonov
Date: 2023-04-17
Description: Dashboard data loader module for JICS project
"""

import logging

logger = logging.getLogger(__name__)

import cm_dashboards.jics.results.data_generator as data_generator


def get_dashboard_list():
    """
    Define dashboard data (id, label, dashboard count, handler, child dashboards, merge duplicate headers)
    :return: Dashboard data (dict)
    """

    # Define the dashboard data for each dashboard
    dashboards = {
        "tab_1": {
            "id": "dashboards-1",
            "label": "結果の要約",
            "merge_duplicate_headers": True,
            "sheet_width": 7,
            "sheet_color": "#FF0000",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T3": {
                    "merge_duplicate_headers": True,
                },
                "T4": {
                    "merge_duplicate_headers": True,
                },
                "T5": {
                    "merge_duplicate_headers": True,
                },
                "T6": {
                    "merge_duplicate_headers": True,
                },
                "T7": {
                    "merge_duplicate_headers": True,
                },
                "T8": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
        "tab_2": {
            "id": "dashboards-2",
            "label": "バランスシート",
            "merge_duplicate_headers": True,
            "sheet_width": 13,
            "sheet_color": "#3366FF",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T9": {
                    "merge_duplicate_headers": True,
                },
                "T9-2": {
                    "merge_duplicate_headers": True,
                },
                "T9-3": {
                    "merge_duplicate_headers": True,
                },
                "T9-4": {
                    "merge_duplicate_headers": True,
                },
                "T10": {
                    "merge_duplicate_headers": True,
                },
                "T11": {
                    "merge_duplicate_headers": True,
                },
                "T12": {
                    "merge_duplicate_headers": True,
                },
                "T13": {
                    "merge_duplicate_headers": True,
                },
                "T14": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
        "tab_3": {
            "id": "dashboards-3",
            "label": "MOCE",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#3366FF",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T25": {
                    "merge_duplicate_headers": True,
                },
                "T26": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
        "tab_4": {
            "id": "dashboards-4",
            "label": "将来所要資本",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#3366FF",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T27": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
        "tab_5": {
            "id": "dashboards-5",
            "label": "ランオフパターン",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#3366FF",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T28": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
        "tab_6": {
            "id": "dashboards-6",
            "label": "所要資本",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#3366FF",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T29": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
        "tab_7": {
            "id": "dashboards-7",
            "label": "生命保険リスク",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#3366FF",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T30": {
                    "merge_duplicate_headers": True,
                    "footer": "死亡リスク",
                },
                "T31": {
                    "merge_duplicate_headers": True,
                    "footer": "長寿リスク",
                },
                "T32": {
                    "merge_duplicate_headers": True,
                    "footer": "罹患・障害リスク",
                },
                "T33": {
                    "merge_duplicate_headers": True,
                },
                "T34": {
                    "merge_duplicate_headers": True,
                },
                "T35": {
                    "merge_duplicate_headers": True,
                },
                "T36": {
                    "merge_duplicate_headers": True,
                },
                "T37": {
                    "merge_duplicate_headers": True,
                },
                "T38": {
                    "merge_duplicate_headers": True,
                },
                "T39": {
                    "merge_duplicate_headers": True,
                    "footer": "解約・失効リスク",
                },
                "T40": {
                    "merge_duplicate_headers": True,
                    "footer": "経費リスク",
                },
                "T41": {
                    "merge_duplicate_headers": True,
                    "footer": "損害保険リスク",
                },
            },
        },
        "tab_8": {
            "id": "dashboards-8",
            "label": "損害保険リスク",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#339966",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T42": {
                    "merge_duplicate_headers": True,
                },
                "T43": {
                    "merge_duplicate_headers": True,
                    "footer": "巨大災害リスク",
                },
            },
        },
        "tab_9": {
            "id": "dashboards-9",
            "label": "巨大災害リスク",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#339966",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T44": {
                    "merge_duplicate_headers": True,
                },
                "T45": {
                    "merge_duplicate_headers": True,
                },
                "T46": {
                    "merge_duplicate_headers": True,
                },
                "T47": {
                    "merge_duplicate_headers": True,
                },
            },
        },
        "tab_10": {
            "id": "dashboards-10",
            "label": "市場リスク",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#339966",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T48": {
                    "merge_duplicate_headers": True,
                    "footer": "金利リスク",
                },
                "T49": {
                    "merge_duplicate_headers": True,
                },
                "T50": {
                    "merge_duplicate_headers": True,
                },
                "T51": {
                    "merge_duplicate_headers": True,
                },
                "T52": {
                    "merge_duplicate_headers": True,
                },
                "T53": {
                    "merge_duplicate_headers": True,
                },
                "T54": {
                    "merge_duplicate_headers": True,
                },
                "T55": {
                    "merge_duplicate_headers": True,
                },
                "T56": {
                    "merge_duplicate_headers": True,
                    "footer": "スプレッドリスク",
                },
                "T57": {
                    "merge_duplicate_headers": True,
                },
                "T58": {
                    "merge_duplicate_headers": True,
                    "footer": "株式リスク",
                },
                "T59": {
                    "merge_duplicate_headers": True,
                },
                "T60": {
                    "merge_duplicate_headers": True,
                    "footer": "不動産リスク",
                },
                "T61": {
                    "merge_duplicate_headers": True,
                    "footer": "為替リスク",
                },
                "T62": {
                    "merge_duplicate_headers": True,
                },
                "T63": {
                    "merge_duplicate_headers": True,
                    "footer": "資産集中リスク",
                },
                "T64": {
                    "merge_duplicate_headers": True,
                },
                "T65": {
                    "merge_duplicate_headers": True,
                    "footer": "信用リスク",
                },
                "T66": {
                    "merge_duplicate_headers": True,
                },
            },
        },
        "tab_11": {
            "id": "dashboards-11",
            "label": "信用リスク",
            "merge_duplicate_headers": True,
            "sheet_color": "#339966",
            "sheet_width": 24,
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T67": {
                    "merge_duplicate_headers": True,
                },
                "T68": {
                    "merge_duplicate_headers": True,
                },
                "T69": {
                    "merge_duplicate_headers": True,
                },
                "T70": {
                    "merge_duplicate_headers": True,
                },
                "T71": {
                    "merge_duplicate_headers": True,
                },
                "T72": {
                    "merge_duplicate_headers": True,
                },
                "T73": {
                    "merge_duplicate_headers": True,
                },
                "T74": {
                    "merge_duplicate_headers": True,
                },
                "T75": {
                    "merge_duplicate_headers": True,
                },
                "T76": {
                    "merge_duplicate_headers": True,
                },
                "T77": {
                    "merge_duplicate_headers": True,
                },
                "T78": {
                    "merge_duplicate_headers": True,
                },
                "T79": {
                    "merge_duplicate_headers": True,
                },
                "T80": {
                    "merge_duplicate_headers": True,
                },
                "T81": {
                    "merge_duplicate_headers": True,
                },
                "T82": {
                    "merge_duplicate_headers": True,
                },
                "T83": {
                    "merge_duplicate_headers": True,
                    "footer": "オペレーショナルリスク",
                },
                "T84": {
                    "merge_duplicate_headers": True,
                },
                "T85": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
        "tab_12": {
            "id": "dashboards-12",
            "label": "オペレーショナルリスク",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#339966",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T86": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
                "T87": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
        "tab_13": {
            "id": "dashboards-13",
            "label": "非保険事業",
            "merge_duplicate_headers": True,
            "sheet_width": 33,
            "sheet_color": "#339966",
            "child_dashboards": {
                "HEADER": {
                    "merge_duplicate_headers": True,
                },
                "T88": {
                    "merge_duplicate_headers": True,
                    "footer": "#",
                },
            },
        },
    }

    return dashboards


def get_dashboard_info(tab_id):
    """
    Define dashboard data (id, label, dashboard count, handler, child dashboards, merge duplicate headers)
    :param tab_id: Tab id
    :return: Dashboard data (dict)
    """
    data = get_dashboard_list()
    return data.get(tab_id)
