from typing import Optional

from pydantic import BaseModel

from suvvyapi.models.history import HistoryMessage, Message


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class BalanceUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    knowledge_usage: int = 0
    function_usage: int = 0
    total_tokens: int = 0
    token_multiplier: float = 1.0


class LLMResult(BaseModel):
    token_usage: TokenUsage = TokenUsage()
    balance_usage: BalanceUsage = BalanceUsage()


class HistoryPrediction(BaseModel):
    generation_info: LLMResult = LLMResult()
    new_messages: list[HistoryMessage] = []

    @property
    def actual_response(self) -> HistoryMessage | None:
        if self.new_messages:
            return self.new_messages[-1]
        else:
            return None


class Prediction(BaseModel):
    generation_info: LLMResult = LLMResult()
    new_messages: list[Message] = []

    @property
    def actual_response(self) -> Message | None:
        if self.new_messages:
            return self.new_messages[-1]
        else:
            return None

