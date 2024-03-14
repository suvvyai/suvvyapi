from typing import Literal

from suvvyapi.models.enums import ContentType
from suvvyapi.models.files.file import Base64File
from suvvyapi.models.messages.content.base import BaseMessageData
from pydantic import BaseModel
from pydantic.json_schema import SkipJsonSchema


class AudioContent(BaseModel):
    base64_file: Base64File
    transcribed_text: SkipJsonSchema[str | None] = None


class AudioMessageData(BaseMessageData):
    data_type: Literal[ContentType.AUDIO] = ContentType.AUDIO
    content: AudioContent
