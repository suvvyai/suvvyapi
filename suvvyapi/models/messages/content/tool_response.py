from typing import Any, Literal

from pydantic import BaseModel

from suvvyapi.models.messages.content.base import BaseMessageData
from suvvyapi.models.enums import ContentType


class ToolResponseContent(BaseModel):
    tool_call_id: str
    tool_name: str | None = None
    tool_response: str | dict[Any, Any] | list[Any]


class ToolResponseMessageData(BaseMessageData):
    data_type: Literal[ContentType.TOOL_RESPONSE] = ContentType.TOOL_RESPONSE
    content: ToolResponseContent
