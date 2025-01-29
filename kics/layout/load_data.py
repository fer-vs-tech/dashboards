"""
Author: Kamoliddin Usmonov
Date: 2022-12-29
Description: Helper functions for dashboard blueprint definition and customizations
"""
import logging

logger = logging.getLogger(__name__)

import cm_dashboards.kics.results.dashboard_1_1 as dashboard_1_1
import cm_dashboards.kics.results.dashboard_1_13 as dashboard_1_13
import cm_dashboards.kics.results.dashboard_2_1 as dashboard_2_1
import cm_dashboards.kics.results.dashboard_2_2 as dashboard_2_2
import cm_dashboards.kics.results.dashboard_2_3 as dashboard_2_3
import cm_dashboards.kics.results.dashboard_2_4 as dashboard_2_4
import cm_dashboards.kics.results.dashboard_2_5 as dashboard_2_5
import cm_dashboards.kics.results.dashboard_2_6 as dashboard_2_6
import cm_dashboards.kics.results.dashboard_3_2 as dashboard_3_2
import cm_dashboards.kics.results.dashboard_5_1 as dashboard_5_1
import cm_dashboards.kics.results.dashboard_5_2 as dashboard_5_2
import cm_dashboards.kics.results.dashboard_5_3 as dashboard_5_3
import cm_dashboards.kics.results.dashboard_5_4 as dashboard_5_4
import cm_dashboards.kics.results.dashboard_5_5 as dashboard_5_5
import cm_dashboards.kics.results.dashboard_5_6 as dashboard_5_6
import cm_dashboards.kics.results.dashboard_6_1 as dashboard_6_1
import cm_dashboards.kics.results.dashboard_6_2 as dashboard_6_2
import cm_dashboards.kics.results.dashboard_6_3 as dashboard_6_3
import cm_dashboards.kics.results.dashboard_6_4 as dashboard_6_4
import cm_dashboards.kics.results.dashboard_6_5 as dashboard_6_5
import cm_dashboards.kics.results.dashboard_7 as dashboard_7
import cm_dashboards.kics.results.dashboard_9_9 as dashboard_9_9
import cm_dashboards.kics.results.dashboard_9_11 as dashboard_9_11
import cm_dashboards.kics.results.dashboard_9_12 as dashboard_9_12
import cm_dashboards.kics.results.dashboard_9_12_2 as dashboard_9_12_2
import cm_dashboards.kics.results.dashboard_10_1 as dashboard_10_1
import cm_dashboards.kics.results.dashboard_10_2 as dashboard_10_2


def get_dashboards_data(kics_name=None):
    """
    All dashboards data (id, label, dashboard count, handler, child dashboards, merge duplicate headers)
    :param company_name: Company name (default: DBG)
    :return: Dashboard data (dict)
    """
    dashboards = {
        "tab-0": {
            "id": "1-1",
            "label": "K-ICS 건전성감독기준 재무상태표",
            "dashboard_count": 1,
            "merge_duplicate_headers": False,
            "handler": dashboard_1_1,
        },
        "tab-1": {
            "id": "1-13",
            "label": "K-ICS 건전성감독기준 재무상태표",
            "merge_duplicate_headers": False,
            "dashboard_count": 1,
            "handler": dashboard_1_13,
        },
        "tab-2": {
            "id": "2-1",
            "label": "K-ICS 지급여력비율 (총괄) (AH717, AI717)",
            "merge_duplicate_headers": False,
            "dashboard_count": 1,
            "handler": dashboard_2_1,
        },
        "tab-3": {
            "id": "2-2",
            "label": "K-ICS 자본증권 명세표(AH718, AI718)",
            "merge_duplicate_headers": True,
            "dashboard_count": 1,
            "handler": dashboard_2_2,
        },
        "tab-4": {
            "id": "2-3",
            "label": "K-ICS 비지배지분 중 종속회사 요구자본의 비지배지분 상응액 (AH719, AI719)",
            "merge_duplicate_headers": False,
            "dashboard_count": 1,
            "handler": dashboard_2_3,
        },
        "tab-5": {
            "id": "2-4",
            "label": "K-ICS 지급여력기준금액 (AH720, AI720)",
            "merge_duplicate_headers": False,
            "dashboard_count": 2,
            "child_dashboards": {
                "2-4-1": {
                    "merge_duplicate_headers": False,
                },
                "2-4-2": {
                    "merge_duplicate_headers": False,
                },
            },
            "handler": dashboard_2_4,
        },
        "tab-6": {
            "id": "2-5",
            "label": "K-ICS 요구자본에 대한 법인세효과 (AH721, AI721)",
            "merge_duplicate_headers": False,
            "merge_duplicate_cells": True,
            "dashboard_count": 1,
            "handler": dashboard_2_5,
        },
        "tab-7": {
            "id": "2-6",
            "label": "K-ICS 경과조치 적용 후 지급여력비율(AH722, AI722)",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": False,
            "dashboard_count": 1,
            "handler": dashboard_2_6,
        },
        "tab-8": {
            "id": "3-2",
            "label": "K-ICS 생명 ∙ 장기손해보험위험액-대재해위험 (AH725, AI725)",
            "dashboard_count": 2,
            "child_dashboards": {
                "3-2-1": {
                    "merge_duplicate_headers": True,
                },
                "3-2-2": {
                    "merge_duplicate_headers": True,
                },
            },
            "handler": dashboard_3_2,
        },
        "tab-9": {
            "id": "5-1",
            "label": "K-ICS 시장위험액-금리위험 (AH732, AI732)",
            "dashboard_count": 4,
            "child_dashboards": {
                "5-1-1": {
                    "merge_duplicate_headers": True,
                },
                "5-1-2": {
                    "merge_duplicate_headers": False,
                },
                "5-1-3": {
                    "merge_duplicate_headers": True,
                },
                "5-1-4": {
                    "merge_duplicate_headers": False,
                },
            },
            "handler": dashboard_5_1,
        },
        "tab-10": {
            "id": "5-2",
            "label": "K-ICS 시장위험액-주식위험 (AH733, AI733)",
            "merge_duplicate_headers": True,
            "dashboard_count": 1,
            "handler": dashboard_5_2,
        },
        "tab-11": {
            "id": "5-3",
            "label": "K-ICS 시장위험액-부동산위험 (AH734, AI734)",
            "merge_duplicate_headers": False,
            "dashboard_count": 1,
            "handler": dashboard_5_3,
        },
        "tab-12": {
            "id": "5-4",
            "label": "K-ICS 시장위험액-외환위험 (AH735, AI735)",
            "merge_duplicate_headers": False,
            "merge_duplicate_cells": False,
            "dashboard_count": 1,
            "handler": dashboard_5_4,
        },
        "tab-13": {
            "id": "5-5",
            "label": "K-ICS 시장위험액-외환위험(상세) (AH736, AI736)",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": True,
            "dashboard_count": 1,
            "handler": dashboard_5_5,
        },
        "tab-14": {
            "id": "5-6",
            "label": "K-ICS 시장위험액-자산집중위험 (AH737, AI737)",
            "merge_duplicate_headers": True,
            "dashboard_count": 1,
            "handler": dashboard_5_6,
        },
        "tab-15": {
            "id": "6-1",
            "label": "K-ICS 신용위험액 (AH738, AI738)",
            "merge_duplicate_headers": False,
            "merge_duplicate_cells": False,
            "dashboard_count": 1,
            "handler": dashboard_6_1,
        },
        "tab-16": {
            "id": "6-2",
            "label": "K-ICS 신용위험액 (신용자산_위험경감반영전) (AH739, AI739)",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": False,
            "dashboard_count": 1,
            "handler": dashboard_6_2,
        },
        "tab-17": {
            "id": "6-3",
            "label": "K-ICS 신용위험액 (위험경감)(AH740, AI740)",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": False,
            "dashboard_count": 1,
            "handler": dashboard_6_3,
        },
        "tab-18": {
            "id": "6-4",
            "label": "K-ICS 신용위험액 (담보부자산) (AH741, AI741)",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": True,
            "dashboard_count": 1,
            "handler": dashboard_6_4,
        },
        "tab-19": {
            "id": "6-5",
            "label": "K-ICS 신용위험액 (재보험계약) (AH742, AI742)",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": False,
            "dashboard_count": 1,
            "handler": dashboard_6_5,
        },
        "tab-20": {
            "id": "7",
            "label": "K-ICS 운영위험액 (AH743, AI743)",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": True,
            "dashboard_count": 1,
            "handler": dashboard_7,
        },
        "tab-21": {
            "id": "9-9",
            "label": "시장위험 - 금리(참고자료) - 주요 통화별 평가결과",
            "merge_duplicate_headers": False,
            "dashboard_count": 15,
            # This dashboard generates child dashboards dynamically based on the data
            # so we need to define a some data for it to as logic required to iterate child dashboards
            "child_dashboards": {
                "9-9-1": {
                    "merge_duplicate_headers": False,
                },
                "9-9-2": {
                    "merge_duplicate_headers": True,
                },
                "9-9-3": {
                    "merge_duplicate_headers": True,
                },
                "9-9-4": {
                    "merge_duplicate_headers": True,
                },
                "9-9-5": {
                    "merge_duplicate_headers": True,
                },
                "9-9-6": {
                    "merge_duplicate_headers": True,
                },
                "9-9-7": {
                    "merge_duplicate_headers": True,
                },
                "9-9-8": {
                    "merge_duplicate_headers": True,
                },
                "9-9-9": {
                    "merge_duplicate_headers": True,
                },
                "9-9-10": {
                    "merge_duplicate_headers": True,
                },
                "9-9-11": {
                    "merge_duplicate_headers": True,
                },
                "9-9-12": {
                    "merge_duplicate_headers": True,
                },
                "9-9-13": {
                    "merge_duplicate_headers": True,
                },
                "9-9-14": {
                    "merge_duplicate_headers": True,
                },
                "9-9-15": {
                    "merge_duplicate_headers": True,
                },
                "9-9-16": {
                    "merge_duplicate_headers": True,
                },
                "9-9-17": {
                    "merge_duplicate_headers": True,
                },
                "9-9-18": {
                    "merge_duplicate_headers": True,
                },
            },
            "handler": dashboard_9_9,
        },
        "tab-22": {
            "id": "9-11",
            "label": "재보험계약 신용위험 재보험자별 세부내역",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": True,
            "dashboard_count": 1,
            "handler": dashboard_9_11,
        },
        "tab-23": {
            "id": "9-12",
            "label": "가용자본 (그룹 기준)",
            "merge_duplicate_headers": True,
            "dashboard_count": 4,
            "child_dashboards": {
                "9-12-1": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
                "9-12-2": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
                "9-12-3": {
                    "merge_duplicate_headers": True,
                },
                "9-12-4": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
            },
            "handler": dashboard_9_12,
        },
        "tab-24": {
            "id": "9-12-(2)",
            "label": "가용자본 (그룹 기준)",
            "merge_duplicate_headers": True,
            "dashboard_count": 2,
            "child_dashboards": {
                "9-12-5": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
                "9-12-6": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
            },
            "handler": dashboard_9_12_2,
        },
        "tab-25": {
            "id": "9-12-(3)",
            "label": "가용자본 (그룹 기준)",
            "merge_duplicate_headers": True,
            "dashboard_count": 6,
            "child_dashboards": {
                "9-12-7": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
                "9-12-8": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
                "9-12-9": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": False,
                },
                "9-12-10": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
                "9-12-11": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
                "9-12-12": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": True,
                },
            },
            "handler": dashboard_9_12,
        },
        "tab-26": {
            "id": "10-1",
            "label": "금리변동시 지급여력비율 추정",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": False,
            "dashboard_count": 4,
            "handler": dashboard_10_1,
            "child_dashboards": {
                "10-1-1": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": False,
                },
                "10-1-2": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": False,
                },
                "10-1-3": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": False,
                },
                "10-1-4": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": False,
                },
            },
        },
        "tab-27": {
            "id": "10-2",
            "label": "금리변동시 금리위험액 추정",
            "merge_duplicate_headers": True,
            "merge_duplicate_cells": False,
            "dashboard_count": 2,
            "handler": dashboard_10_2,
            "child_dashboards": {
                "10-2-1": {
                    "merge_duplicate_headers": False,
                    "merge_duplicate_cells": False,
                },
                "10-2-2": {
                    "merge_duplicate_headers": True,
                    "merge_duplicate_cells": False,
                },
            },
        },
    }

    # Filter some dashboards if company name is HANA
    if kics_name is not None and kics_name == "HANA":
        filter_dashboards = ["tab-7", "tab-26", "tab-27"]
        for dashboard_id in filter_dashboards:
            del dashboards[dashboard_id]
    return dashboards


def get_dashboard_data(kics_name, tab_id):
    """
    Define dashboard data (id, label, dashboard count, handler, child dashboards, merge duplicate headers)
    :param tab_id: Tab id
    :return: Dashboard data (dict)
    """
    data = get_dashboards_data(kics_name)
    return data.get(tab_id)
