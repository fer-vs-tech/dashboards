from enum import Enum


class ProgramNames(Enum):
    """
    Used as controller to select desired DB wrapper class
    """

    SOLVENCY_OVERALL = 1
    REQUIRED_CAPITAL = 2
    SCHEMA = 3
    ASSET_PORTFOLIO = 4
    PROJECTED_RISK_REGULATORY = 5
    LIFE_AND_HEALTH_RISK = 6
    MARKET_RISK = 7
    CREDIT_RISK = 8


class ChartNames(Enum):
    """
    Used as controller to generate desired chart
    """

    SOLVENCY_OVERALL = 1
    AVAILABLE_CAPITAL = 2
    REQUIRED_CAPITAL = 3
    SCHEMA = 4
    ASSET_PORTFOLIO = 5
    PROJECTED_RISK_REGULATORY = 6
    LIFE_AND_HEALTH_RISK = 7
    LIFE_AND_HEALTH_INSURANCE_RISK = 8
    LIFE_AND_HEALTH_RISK_OVERALL = 9
    MORTALITY_RISK = 10
    LONGEVITY_RISK = 11
    MORBITITY_RISK = 12
    LAPSE_RISK = 13
    EXPENSE_RISK = 14
    CATASTROPHE_RISK = 15
    MARKET_RISK = 16
    MARKET_RISK_OVERALL = 17
    INTEREST_RISK = 18
    EQUITY_RISK = 19
    FOREX_RISK = 20
    PROPERTY_RISK = 21
    CONCENTRATION_RISK = 22
    CREDIT_RISK = 23
