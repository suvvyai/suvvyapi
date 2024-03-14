from typing import Literal

from suvvyapi.models.messages.content.base import BaseMessageData
from suvvyapi.models.enums import ContentType


class TextMessageData(BaseMessageData):
    data_type: Literal[ContentType.TEXT] = ContentType.TEXT
    content: str
