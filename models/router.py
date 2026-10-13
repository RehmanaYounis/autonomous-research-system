from enum import Enum

from models.base import BaseModelProvider


class ModelTier(str, Enum):
    CHEAP = "cheap"
    STRONG = "strong"


class ModelRouter:
    def __init__(
        self,
        cheap_model: BaseModelProvider,
        strong_model: BaseModelProvider,
    ):
        self.cheap_model = cheap_model
        self.strong_model = strong_model

    def get_model(self, tier: ModelTier) -> BaseModelProvider:
        if tier == ModelTier.CHEAP:
            return self.cheap_model

        if tier == ModelTier.STRONG:
            return self.strong_model

        raise ValueError(f"Unsupported model tier: {tier}")