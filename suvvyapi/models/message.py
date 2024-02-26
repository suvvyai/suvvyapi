from typing import Literal

from pydantic import BaseModel

from suvvyapi.models.enums import SenderRole
from suvvyapi.models.message_data.text import TextMessageData


class Message(BaseModel):
    message_sender: SenderRole
    message_data: TextMessageData


class RequestMessage(Message):
    message_sender: Literal[SenderRole.CUSTOMER, SenderRole.EMPLOYEE]
