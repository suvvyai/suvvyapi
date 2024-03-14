from datetime import datetime
from typing import Literal, Union

from pydantic import BaseModel, UUID4, Field

from suvvyapi.models.enums import SenderRole, ContentType
from suvvyapi.models.messages.content.audio import AudioMessageData
from suvvyapi.models.messages.content.event import EventMessageData
from suvvyapi.models.messages.content.image import ImageMessageData
from suvvyapi.models.messages.content.text import TextMessageData
from suvvyapi.models.messages.content.tool_call import ToolCallsMessageData
from suvvyapi.models.messages.content.tool_response import ToolResponseMessageData

MessageDataUnion = Union[
    TextMessageData,
    ImageMessageData,
    AudioMessageData,
    ToolCallsMessageData,
    ToolResponseMessageData,
    EventMessageData,
]


class Message(BaseModel):
    message_sender: SenderRole
    message_data: MessageDataUnion

    def is_visible(self, acceptable_data_types: set[ContentType] | None = None) -> bool:
        acceptable_data_types = acceptable_data_types or {ContentType.TEXT}
        return self.message_data.data_type in acceptable_data_types


class RequestMessage(Message):
    message_sender: Literal[SenderRole.CUSTOMER, SenderRole.EMPLOYEE]


class DialogueMessage(Message):
    message_id: UUID4 = Field(frozen=True)
    tokens: int = Field(frozen=True)
    created_at: datetime = Field(frozen=True)

    message_sender: SenderRole = Field(frozen=True)
    message_data: MessageDataUnion = Field(frozen=True)
