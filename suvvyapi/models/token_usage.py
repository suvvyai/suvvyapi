from pydantic import BaseModel


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


class Usage(BaseModel):
    token_usage: TokenUsage = TokenUsage()
    balance_usage: BalanceUsage = BalanceUsage()
