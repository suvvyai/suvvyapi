from typing import Literal, Union

from pydantic import BaseModel

from suvvyapi.models.enums import StopReason, ContentType
from suvvyapi.models.enums.event import EventMessageType
from suvvyapi.models.messages.content.base import BaseMessageData


class BaseEventContent(BaseModel):
    event_type: EventMessageType


class StopEventContent(BaseEventContent):
    event_type: Literal[
        EventMessageType.DIALOGUE_STOPPED
    ] = EventMessageType.DIALOGUE_STOPPED
    reason: StopReason


class ResumeEventContent(BaseEventContent):
    event_type: Literal[
        EventMessageType.DIALOGUE_RESUMED
    ] = EventMessageType.DIALOGUE_RESUMED


class EventMessageData(BaseMessageData):
    data_type: Literal[ContentType.EVENT] = ContentType.EVENT
    content: Union[StopEventContent, ResumeEventContent]
