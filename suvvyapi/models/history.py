from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class FunctionDetails(BaseModel):
    name: str
    args: Optional[dict] = None


class Message(BaseModel):
    text: str = Field(default="", description="Message text, function result")
    role: Literal["human", "ai", "function_result", "function_call"]
    function: Optional[FunctionDetails] = Field(default=None,
                                                description="Needed for functions. Unused if role != \"function_*\".")


class HistoryMessage(Message):
    tokens: int = 0
    time: datetime
    message_id: int
    context: str = ""


class History(BaseModel):
    history: list[HistoryMessage]
    unique_id: str
    stopped: bool = False
    stop_reason: str = "unknown"