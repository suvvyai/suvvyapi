from suvvyapi import Suvvy, Message, Usage
from suvvyapi.models.dialogue import Dialogue
from suvvyapi.models.message import DialogueMessage


class History(object):
    def __init__(self, unique_id: str, suvvy: Suvvy):
        self._suvvy = suvvy
        self.unique_id = unique_id

    def predict(
        self,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> tuple[list[DialogueMessage], Usage]:
        """Get answer from AI"""
        return self._suvvy.predict_history(
            self.unique_id, placeholders, custom_log_info, source
        )

    async def apredict(
        self,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> tuple[list[DialogueMessage], Usage]:
        """Get answer from AI"""
        return await self._suvvy.apredict_history(
            self.unique_id, placeholders, custom_log_info, source
        )

    def predict_add_message(
        self,
        message: list[Message] | Message | str,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> tuple[list[DialogueMessage], Usage]:
        """Add message and get answer from AI"""
        return self._suvvy.predict_history_add_message(
            self.unique_id, message, placeholders, custom_log_info, source
        )

    async def apredict_add_message(
        self,
        message: list[Message] | Message | str,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> tuple[list[DialogueMessage], Usage]:
        """Add message and get answer from AI"""
        return await self._suvvy.apredict_history_add_message(
            self.unique_id, message, placeholders, custom_log_info, source
        )

    def get(self) -> Dialogue:
        """Get history"""
        return self._suvvy.get_dialogue(self.unique_id)

    async def aget(self) -> Dialogue:
        """Get history"""
        return await self._suvvy.aget_dialogue(self.unique_id)

    def reset(self) -> Dialogue:
        """Reset history"""
        return self._suvvy.reset_dialogue(self.unique_id)

    async def areset(self) -> Dialogue:
        """Reset history"""
        return await self._suvvy.areset_dialogue(self.unique_id)

    def add_message(
        self, message: list[Message] | Message
    ) -> tuple[list[DialogueMessage], int]:
        """Get history"""
        return self._suvvy.add_message_to_dialogue(self.unique_id, message)

    async def async_add_message(
        self, message: list[Message] | Message
    ) -> tuple[list[DialogueMessage], int]:
        """Get history"""
        return await self._suvvy.async_add_message_to_dialogue(self.unique_id, message)
