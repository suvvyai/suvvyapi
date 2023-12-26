from typing import Type

import httpx

from suvvyapi import ChatHistory, Message, Prediction
from suvvyapi.exceptions.api import (
    InvalidAPITokenError,
    NegativeBalanceError,
    HistoryTooLongError,
    InternalAPIError,
    HistoryNotFoundError,
    InternalMessageAdded,
)


def _handle_error(response: httpx.Response) -> None:
    if response.status_code <= 299:
        return

    exceptions = {
        401: InvalidAPITokenError,
        402: NegativeBalanceError.from_detail,
        406: InternalMessageAdded,
        413: HistoryTooLongError,
        404: HistoryNotFoundError,
        500: InternalAPIError,
    }
    exception: Type[BaseException] = exceptions[response.status_code]  # type: ignore
    raise exception(response.json().get("detail", None))


class Suvvy(object):
    def __init__(
        self,
        api_token: str,
        api_url: str = "https://api.suvvy.ai",
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ):
        self.placeholders = placeholders or {}
        self.custom_log_info = custom_log_info or {}
        self.source = source or "https://github.com/suvvyai/suvvyapi"

        self._headers = {"Authorization": f"Bearer {api_token}"}
        self._api_url = api_url.rstrip("/ \\\n")

    def _get_placeholders(self, placeholders: dict | None = None) -> dict:
        placeholders = placeholders or {}
        return {**self.placeholders, **placeholders}

    def _get_custom_log_info(self, custom_log_info: dict | None = None) -> dict:
        custom_log_info = custom_log_info or {}
        return {**self.custom_log_info, **custom_log_info}

    def _sync_request(
        self,
        method: str,
        path: str,
        body_json: dict | None = None,
        params: dict | None = None,
    ) -> httpx.Response:
        with httpx.Client(
            headers=self._headers, base_url=self._api_url, timeout=300
        ) as client:
            r = client.request(method, path, json=body_json, params=params)
            _handle_error(r)
            return r

    async def _async_request(
        self,
        method: str,
        path: str,
        body_json: dict | None = None,
        params: dict | None = None,
    ) -> httpx.Response:
        async with httpx.AsyncClient(
            headers=self._headers, base_url=self._api_url, timeout=300
        ) as client:
            r = await client.request(method, path, json=body_json, params=params)
            _handle_error(r)
            return r

    def check_connection(self) -> bool:
        """Check connection and API token"""
        self._sync_request("GET", "/api/check")
        return True

    async def acheck_connection(self) -> bool:
        """Check connection and API token"""
        await self._async_request("GET", "/api/check")
        return True

    def get_history(self, unique_id: str) -> ChatHistory:
        """Get history by unique_id"""
        r = self._sync_request(
            "GET", "/api/v1/history", params={"unique_id": unique_id}
        )
        return ChatHistory(**r.json())

    async def aget_history(self, unique_id: str) -> ChatHistory:
        """Get history by unique_id"""
        r = await self._async_request(
            "GET", "/api/v1/history", params={"unique_id": unique_id}
        )
        return ChatHistory(**r.json())

    def reset_history(self, unique_id: str) -> ChatHistory:
        """Reset history by unique_id and return deleted history"""
        r = self._sync_request(
            "PUT", "/api/v1/history", params={"unique_id": unique_id}
        )
        if r.status_code == 202:
            raise HistoryNotFoundError
        return ChatHistory(**r.json()["deleted_history"])

    async def areset_history(self, unique_id: str) -> ChatHistory:
        """Reset history by unique_id and return deleted history"""
        r = await self._async_request(
            "PUT", "/api/v1/history", params={"unique_id": unique_id}
        )
        if r.status_code == 202:
            raise HistoryNotFoundError
        return ChatHistory(**r.json()["deleted_history"])

    def add_message_to_history(
        self, unique_id: str, message: list[Message] | Message
    ) -> ChatHistory:
        """Add message to history by unique_id"""
        if not isinstance(message, list):
            message = [message]
        message = [m.model_dump() for m in message]

        r = self._sync_request(
            "POST",
            "/api/v1/history/message",
            params={"unique_id": unique_id},
            body_json={"messages": message},
        )
        return ChatHistory(**r.json())

    async def async_add_message_to_history(
        self, unique_id: str, message: list[Message] | Message
    ) -> ChatHistory:
        """Add message to history by unique_id"""
        if not isinstance(message, list):
            message = [message]
        message = [m.model_dump() for m in message]

        r = await self._async_request(
            "POST",
            "/api/v1/history/message",
            params={"unique_id": unique_id},
            body_json={"messages": message},
        )
        return ChatHistory(**r.json())

    def predict_history(
        self,
        unique_id: str,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> Prediction | None:
        """Get answer from AI by unique_id.
        None means API refused to answer"""

        r = self._sync_request(
            method="POST",
            path="/api/v1/history/predict",
            params={"unique_id": unique_id},
            body_json={
                "placeholders": self._get_placeholders(placeholders),
                "custom_log_info": self._get_custom_log_info(custom_log_info),
                "source": source or self.source,
            },
        )

        if r.status_code == 202:
            return None

        return Prediction(**r.json())

    async def apredict_history(
        self,
        unique_id: str,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> Prediction | None:
        """Get answer from AI by unique_id.
        None means API refused to answer"""

        r = await self._async_request(
            method="POST",
            path="/api/v1/history/predict",
            params={"unique_id": unique_id},
            body_json={
                "placeholders": self._get_placeholders(placeholders),
                "custom_log_info": self._get_custom_log_info(custom_log_info),
                "source": source or self.source,
            },
        )

        if r.status_code == 202:
            return None

        return Prediction(**r.json())

    def predict_history_add_message(
        self,
        unique_id: str,
        message: list[Message] | Message,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> Prediction | None:
        """Add message and get answer from AI by unique_id.
        None means API refused to answer"""

        if not isinstance(message, list):
            message = [message]
        message = [m.model_dump() for m in message]

        r = self._sync_request(
            method="POST",
            path="/api/v1/history/message/predict",
            params={"unique_id": unique_id},
            body_json={
                "placeholders": self._get_placeholders(placeholders),
                "custom_log_info": self._get_custom_log_info(custom_log_info),
                "source": source or self.source,
                "messages": message,
            },
        )

        if r.status_code == 202:
            return None

        return Prediction(**r.json())

    async def apredict_history_add_message(
        self,
        unique_id: str,
        message: list[Message] | Message,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> Prediction | None:
        """Add message and get answer from AI by unique_id.
        None means API refused to answer"""

        if not isinstance(message, list):
            message = [message]
        message = [m.model_dump() for m in message]

        r = await self._async_request(
            method="POST",
            path="/api/v1/history/message/predict",
            params={"unique_id": unique_id},
            body_json={
                "placeholders": self._get_placeholders(placeholders),
                "custom_log_info": self._get_custom_log_info(custom_log_info),
                "source": source or self.source,
                "messages": message,
            },
        )

        if r.status_code == 202:
            return None

        return Prediction(**r.json())

    def as_history(self, unique_id: str) -> "History":  # type: ignore
        from suvvyapi.history import History

        return History(unique_id, self)  # type: ignore
