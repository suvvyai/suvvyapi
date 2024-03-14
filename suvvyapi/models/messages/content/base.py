from typing import Any

from suvvyapi.models.enums import ContentType
from pydantic import BaseModel


class BaseMessageData(BaseModel):
    data_type: ContentType
    content: Any
