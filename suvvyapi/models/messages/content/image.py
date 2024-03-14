from typing import Literal

from suvvyapi.models.files.file import Base64File
from suvvyapi.models.messages.content.base import BaseMessageData
from suvvyapi.models.enums import ContentType
from pydantic import BaseModel
from pydantic.json_schema import SkipJsonSchema


class ImageContent(BaseModel):
    base64_file: Base64File
    found_file_text: SkipJsonSchema[str | None] = None


class ImageMessageData(BaseMessageData):
    data_type: Literal[ContentType.IMAGE] = ContentType.IMAGE
    content: ImageContent
