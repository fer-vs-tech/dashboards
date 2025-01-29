from enum import Enum


class ProgramNames(Enum):
    """
    Used as controller to select desired DB wrapper class
    """

    CompanyLevelAssetRisk = "CompanyLevelAssetRisk"
    MarketRisk = "CompanyLevelAssetRisk"
    ProductLevelAssetRisk = "ProductLevelAssetRisk"
    AssetInfo = "AssetInfo"
    ProductLevelLifeRisk = "ProductLevelLifeRisk"
    ProductInfo = "ProductInfo"
    LiabilityInfo = "ProductLevelLifeRisk"
    CompanyLevelLifeRiskTotal = "CompanyLevelLifeRiskTotal"
    ProductLevelLifeRiskTotal = "ProductLevelLifeRiskTotal"
    OperationRiskTotal = "OperationRiskTotal"
    LiabilityMovement = "LiabilityMovement"
    AssetMovement = "AssetMovement"
    InsuranceAndMarketRisk = "InsuranceAndMarketRisk"
    RatioMovement = "RatioMovement"
    CapitalAndIndividualRisksMovement = "CapitalAndIndividualRisksMovement"
    InterestRateSensitivity = "InterestRateSensitivity"
    AvailableCapital = "AvailableCapital"
    TierOne = "TierOne"
    TierTwo = "TierTwo"


class ChartNames(Enum):
    """
    Used as controller to generate desired chart
    """

    CompanyRisk = "CompanyRisk"
    AssetInfo = "AssetInfo"
    MarketRisk = "MarketRisk"
    LiabilityInfo = "LiabilityInfo"
    ProductInfo = "ProductInfo"
    LiabilityMovement = "LiabilityMovement"
    AssetMovement = "AssetMovement"
    InsuranceAndMarketRisk = "InsuranceAndMarketRisk"
    RatioMovement = "RatioMovement"
    CapitalAndIndividualRisksMovement = "CapitalAndIndividualRisksMovement"
    InterestRateSensitivity = "InterestRateSensitivity"
    AvailableCapital = "AvailableCapital"
    TierOne = "TierOne"
    TierTwo = "TierTwo"


class ColorSchema:
    """
    Used for waterfall chart generation
    """

    def __init__(
        self,
        current="ADD5D7",
        increase="#F8AA7C",
        decrease="#ADD5D7",
        total="#ADD5D7",
        connector="#91A7DF",
    ):
        self.current = current
        self.increase = increase
        self.decrease = decrease
        self.total = total
        self.connector = connector
