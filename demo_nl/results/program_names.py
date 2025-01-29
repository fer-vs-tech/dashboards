from enum import Enum


class ProgramNames(Enum):
    """
    Used as controller to select desired DB wrapper class
    """

    FutureBSProjection = 0
    ProjectedLifeInsuranceRisk = 1
    ProjectedMarketRisk = 2
    Schema = 3
    BalanceSheet = 4
    RiskDistribution = 5
    MarketRiskDistribution = 6
    LifeInsuranceRiskDistribution = 7
    AssetMV = 8
    SolvencyResults = 9


class ChartNames(Enum):
    """
    Used as controller to generate desired chart
    """

    FutureBSProjection = 0
    ProjectedLifeInsuranceRisk = 1
    ProjectedMarketRisk = 2
    Schema = 3
    CatastropheRisk = 4
    ExpenseRisk = 5
    LongevityRisk = 6
    MorbidityRisk = 7
    MortalityRisk = 8
    LapseRisk = 9
    EquityRisk = 10
    InterestRisk = 11
    PropertyRisk = 12
    CurrencyRisk = 13
    SpreadRisk = 14
    ProjectedMarketRiskAgg = 15
    ProjectedLifeInsuranceRiskAgg = 16
    LifeInsuranceRiskAgg = 17
    BalanceSheet = 18
    RiskDistribution = 19
    MarketRiskDistribution = 20
    LifeInsuranceRiskDistribution = 21
    AssetMV = 22
    MarketRiskProjection = 23
    LifeInsuranceRiskProjection = 24
    SolvencyResults = 25
    AssetPortfolio = 26
