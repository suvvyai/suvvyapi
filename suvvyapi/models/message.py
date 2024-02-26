from datetime import datetime
from typing import Literal

from pydantic import BaseModel, UUID4, Field

from suvvyapi.models.enums import SenderRole
from suvvyapi.models.message_data.text import TextMessageData


class Message(BaseModel):
    message_sender: SenderRole
    message_data: TextMessageData


class RequestMessage(Message):
    message_sender: Literal[SenderRole.CUSTOMER, SenderRole.EMPLOYEE]


class DialogueMessage(Message):
    message_id: UUID4 = Field(frozen=True)
    tokens: int = Field(frozen=True)
    created_at: datetime = Field(frozen=True)

    message_sender: SenderRole = Field(frozen=True)
    message_data: TextMessageData = Field(frozen=True)
