from typing import Literal

from suvvyapi.models.enums import ContentType
from suvvyapi.models.message_data.base import BaseMessageData


class TextMessageData(BaseMessageData):
    data_type: Literal[ContentType.TEXT] = ContentType.TEXT
    content: str
