from typing import Literal, Any

from pydantic import BaseModel

from suvvyapi.models.enums import ContentType
from suvvyapi.models.message_data.base import BaseMessageData


class ToolCallFunction(BaseModel):
    name: str
    arguments: dict[str, Any] = {}


class ToolCall(BaseModel):
    tool_call_id: str
    tool_type: Literal["function"] = "function"
    function: ToolCallFunction


class ToolCallsContent(BaseModel):
    tool_calls: list[ToolCall]


class ToolResponseContent(BaseModel):
    tool_call_id: str
    tool_name: str | None = None
    tool_response: str | dict[Any, Any] | list[Any]


class ToolCallsMessageData(BaseMessageData):
    data_type: Literal[ContentType.TOOL_CALLS] = ContentType.TOOL_CALLS
    content: ToolCallsContent


class ToolResponseMessageData(BaseMessageData):
    data_type: Literal[ContentType.TOOL_RESPONSE] = ContentType.TOOL_RESPONSE
    content: ToolResponseContent
