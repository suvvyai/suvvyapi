import datetime

from pydantic import ConfigDict, BaseModel, Field

from suvvyapi.models.enums import StopReason, Channel
from suvvyapi.models.message import DialogueMessage


class Dialogue(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    dialogue_id: str = Field(serialization_alias="_id", frozen=True)

    messages: list[DialogueMessage] = Field(frozen=True)

    unique_id: str = Field(frozen=True)
    user_id: int = Field(frozen=True)
    instance_id: int | None = Field(frozen=True)

    source: str | None = Field(frozen=True)

    is_stopped: bool = Field(frozen=True)
    stopped_at: datetime.datetime | None = Field(frozen=True)
    stop_reason: StopReason | None = Field(frozen=True)

    is_deleted: bool = Field(frozen=True)
    deleted_at: datetime.datetime | None = Field(frozen=True)

    created_at: datetime.datetime = Field(frozen=True)
    channel_name: Channel = Field(frozen=True)
