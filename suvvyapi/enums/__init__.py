from enum import Enum


class Role(Enum):
    HUMAN = "human"
    AI = "ai"
    FUNCTION_CALL = "function_call"
    FUNCTION_RESULT = "function_result"
