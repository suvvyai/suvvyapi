import json
from typing import Type
from urllib.parse import quote

import httpx

from suvvyapi import Message, Usage
from suvvyapi.exceptions.api import (
    InvalidAPITokenError,
    NegativeBalanceError,
    HistoryTooLongError,
    InternalAPIError,
    HistoryNotFoundError,
    InternalMessageAdded,
)
from suvvyapi.models.dialogue import Dialogue
from suvvyapi.models.enums import SenderRole
from suvvyapi.models.message import DialogueMessage
from suvvyapi.models.messages.content.text import TextMessageData


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
    if response.status_code not in exceptions:
        raise Exception(json.dumps(response.json(), indent=2, ensure_ascii=False))
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

    def get_dialogue(self, unique_id: str) -> Dialogue:
        """Get dialogue by unique_id"""
        r = self._sync_request("GET", f"/api/dialogue/{quote(unique_id, safe='')}/get")
        return Dialogue.model_validate(r.json())

    async def aget_dialogue(self, unique_id: str) -> Dialogue:
        """Get history by unique_id"""
        r = await self._async_request(
            "GET", f"/api/dialogue/{quote(unique_id, safe='')}/get"
        )
        return Dialogue.model_validate(**r.json())

    def reset_dialogue(self, unique_id: str) -> Dialogue:
        """Reset history by unique_id and return deleted history"""
        r = self._sync_request(
            "PUT", f"/api/dialogue/{quote(unique_id, safe='')}/delete"
        )
        if r.status_code == 404:
            raise HistoryNotFoundError
        return Dialogue.model_validate(**r.json())

    async def areset_dialogue(self, unique_id: str) -> Dialogue:
        """Reset history by unique_id and return deleted history"""
        r = await self._async_request(
            "PUT", f"/api/dialogue/{quote(unique_id, safe='')}/delete"
        )
        if r.status_code == 404:
            raise HistoryNotFoundError
        return Dialogue.model_validate(**r.json())

    def add_message_to_dialogue(
        self, unique_id: str, message: list[Message] | Message
    ) -> tuple[list[DialogueMessage], int]:
        """Add message to history by unique_id. Returns new messages and used tokens"""
        if not isinstance(message, list):
            message = [message]
        message = [m.model_dump(mode="json") for m in message]

        r = self._sync_request(
            "POST",
            f"/api/dialogue/{quote(unique_id, safe='')}/messages/add",
            body_json={"messages": message},
        )
        used_tokens = r.json().get("used_tokens", 0)
        added_messages = [
            DialogueMessage.model_validate(m)
            for m in r.json().get("added_messages", [])
        ]
        return added_messages, used_tokens

    async def async_add_message_to_dialogue(
        self, unique_id: str, message: list[Message] | Message
    ) -> tuple[list[DialogueMessage], int]:
        """Add message to history by unique_id. Returns new messages and used tokens"""
        if not isinstance(message, list):
            message = [message]
        message = [m.model_dump(mode="json") for m in message]

        r = await self._async_request(
            "POST",
            f"/api/dialogue/{quote(unique_id, safe='')}/messages/add",
            body_json={"messages": message},
        )
        used_tokens = r.json().get("used_tokens", 0)
        added_messages = [
            DialogueMessage.model_validate(m)
            for m in r.json().get("added_messages", [])
        ]
        return added_messages, used_tokens

    def predict_history(
        self,
        unique_id: str,
        placeholders: dict | None = None,
        additional_log_info: dict | None = None,
        source: str | None = None,
    ) -> tuple[list[DialogueMessage], Usage]:
        """Get answer from AI by unique_id. Returns new messages and token usage."""

        r = self._sync_request(
            method="POST",
            path=f"/api/dialogue/{quote(unique_id, safe='')}/predict",
            body_json={
                "placeholders": self._get_placeholders(placeholders),
                "custom_log_info": self._get_custom_log_info(additional_log_info),
                "source": source or self.source,
            },
        )

        if r.status_code == 202:
            return [], Usage()

        usage = Usage.model_validate(r.json().get("token_usage"))
        added_messages = [
            DialogueMessage.model_validate(m) for m in r.json().get("new_messages", [])
        ]
        return added_messages, usage

    async def apredict_history(
        self,
        unique_id: str,
        placeholders: dict | None = None,
        additional_log_info: dict | None = None,
        source: str | None = None,
    ) -> tuple[list[DialogueMessage], Usage]:
        """Get answer from AI by unique_id. Returns new messages and token usage."""

        r = await self._async_request(
            method="POST",
            path=f"/api/dialogue/{quote(unique_id, safe='')}/predict",
            body_json={
                "placeholders": self._get_placeholders(placeholders),
                "custom_log_info": self._get_custom_log_info(additional_log_info),
                "source": source or self.source,
            },
        )

        if r.status_code == 202:
            return [], Usage()

        usage = Usage.model_validate(r.json().get("token_usage"))
        added_messages = [
            DialogueMessage.model_validate(m) for m in r.json().get("new_messages", [])
        ]
        return added_messages, usage

    def predict_history_add_message(
        self,
        unique_id: str,
        message: list[Message] | Message | str,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> tuple[list[DialogueMessage], Usage]:
        """Add message and get answer from AI by unique_id. Returns new messages and token usage."""
        if isinstance(message, str):
            message = [
                Message(
                    message_sender=SenderRole.CUSTOMER,
                    message_data=TextMessageData(content=message),
                )
            ]
        elif not isinstance(message, list):
            message = [message]
        message = [m.model_dump() for m in message]

        r = self._sync_request(
            method="POST",
            path=f"/api/dialogue/{quote(unique_id, safe='')}/predict/add_message",
            body_json={
                "placeholders": self._get_placeholders(placeholders),
                "custom_log_info": self._get_custom_log_info(custom_log_info),
                "source": source or self.source,
                "messages": message,
            },
        )

        if r.status_code == 202:
            return [], Usage()

        usage = Usage.model_validate(r.json().get("token_usage"))
        added_messages = [
            DialogueMessage.model_validate(m) for m in r.json().get("new_messages", [])
        ]
        return added_messages, usage

    async def apredict_history_add_message(
        self,
        unique_id: str,
        message: list[Message] | Message | str,
        placeholders: dict | None = None,
        custom_log_info: dict | None = None,
        source: str | None = None,
    ) -> tuple[list[DialogueMessage], Usage]:
        """Add message and get answer from AI by unique_id. Returns new messages and token usage."""
        if isinstance(message, str):
            message = [
                Message(
                    message_sender=SenderRole.CUSTOMER,
                    message_data=TextMessageData(content=message),
                )
            ]
        elif not isinstance(message, list):
            message = [message]
        message = [m.model_dump() for m in message]

        r = await self._async_request(
            method="POST",
            path=f"/api/dialogue/{quote(unique_id, safe='')}/predict/add_message",
            body_json={
                "placeholders": self._get_placeholders(placeholders),
                "custom_log_info": self._get_custom_log_info(custom_log_info),
                "source": source or self.source,
                "messages": message,
            },
        )

        if r.status_code == 202:
            return [], Usage()

        usage = Usage.model_validate(r.json().get("token_usage"))
        added_messages = [
            DialogueMessage.model_validate(m) for m in r.json().get("new_messages", [])
        ]
        return added_messages, usage

    def as_history(self, unique_id: str) -> "History":  # type: ignore
        """Represent history as a History object"""
        from suvvyapi.history import History

        return History(unique_id, self)  # type: ignore
