from typing import Any, Literal

from pydantic import BaseModel

from suvvyapi.models.messages.content.base import BaseMessageData
from suvvyapi.models.enums import ContentType


class ToolCallFunction(BaseModel):
    name: str
    arguments: dict[str, Any] = {}


class ToolCall(BaseModel):
    tool_call_id: str
    tool_type: Literal["function"] = "function"
    function: ToolCallFunction


class ToolCallsContent(BaseModel):
    tool_calls: list[ToolCall]


class ToolCallsMessageData(BaseMessageData):
    data_type: Literal[ContentType.TOOL_CALLS] = ContentType.TOOL_CALLS
    content: ToolCallsContent
