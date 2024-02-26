from typing import Any

from pydantic import BaseModel

from suvvyapi.models.enums import ContentType


class BaseMessageData(BaseModel):
    data_type: ContentType
    content: Any
