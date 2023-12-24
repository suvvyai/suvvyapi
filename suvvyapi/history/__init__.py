from suvvyapi import Suvvy, Prediction, Message, ChatHistory


class History(object):
    def __init__(self, unique_id: str, suvvy: Suvvy):
        self._suvvy = suvvy
        self.unique_id = unique_id

    def predict(
        self,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> Prediction | None:
        """Get answer from AI"""
        return self._suvvy.predict_history(
            self.unique_id, placeholders, custom_log_info, source
        )

    async def apredict(
        self,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> Prediction | None:
        """Get answer from AI"""
        return await self._suvvy.apredict_history(
            self.unique_id, placeholders, custom_log_info, source
        )

    def predict_add_message(
        self,
        message: list[Message] | Message,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> Prediction | None:
        """Add message and get answer from AI"""
        return self._suvvy.predict_history_add_message(
            self.unique_id, message, placeholders, custom_log_info, source
        )

    async def apredict_add_message(
        self,
        message: list[Message] | Message,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> Prediction | None:
        """Add message and get answer from AI"""
        return await self._suvvy.apredict_history_add_message(
            self.unique_id, message, placeholders, custom_log_info, source
        )

    def get(self) -> ChatHistory:
        """Get history"""
        return self._suvvy.get_history(self.unique_id)

    async def aget(self) -> ChatHistory:
        """Get history"""
        return await self._suvvy.aget_history(self.unique_id)

    def reset(self) -> ChatHistory:
        """Reset history"""
        return self._suvvy.reset_history(self.unique_id)

    async def areset(self) -> ChatHistory:
        """Reset history"""
        return await self._suvvy.areset_history(self.unique_id)

    def add_message(self, message: list[Message] | Message) -> ChatHistory:
        """Get history"""
        return self._suvvy.add_message_to_history(self.unique_id, message)

    async def async_add_message(self, message: list[Message] | Message) -> ChatHistory:
        """Get history"""
        return await self._suvvy.async_add_message_to_history(self.unique_id, message)
