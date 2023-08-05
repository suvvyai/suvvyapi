from typing import Literal, Optional
import httpx
from devtools import debug

from suvvyapi.exceptions.api import InvalidAPITokenError, NegativeBalanceError, DialogStoppedError, \
    HistoryNotFoundError, HistoryTooLongError, MessageLimitExceededError, UnknownAPIError, InternalAPIError
from suvvyapi.models.history import History, Message
from suvvyapi.models.responses import Prediction


class AsyncSuvvyAPIWrapper:
    def __init__(self, token: str, base_url: str = "https://api.suvvy.ai/", check_connection: bool = True, placeholders: dict = {}, custom_log_info: dict = {}):
        self.token = token
        self.base_url = base_url.lstrip("/")
        self.placeholders = placeholders
        self.custom_log_info = custom_log_info

        if check_connection:
            self._make_request("GET", "/api/check")

    async def _make_request(self, method: Literal["GET", "POST", "PUT", "DELETE"], path: str, body: Optional[dict] = {}) -> httpx.Response:
        headers = {
            "Authorization": f"bearer {self.token}"
        }
        async with httpx.AsyncClient(headers=headers, base_url=self.base_url, timeout=300) as c:
            response = await c.request(method=method, url=path, json=body)
            if response.status_code == 401:
                raise InvalidAPITokenError("API Token is invalid.")
            if response.status_code == 402:
                raise NegativeBalanceError.from_detail(response.json()["detail"])
            if response.status_code == 500:
                raise InternalAPIError("Internal API error occurred. Contact suvvy.ai support.")
            return response

    async def get_history(self, unique_id: str) -> History:
        response = await self._make_request(method="GET", path=f"/api/v1/history?unique_id={unique_id}")
        json = response.json()
        history = History(**json)
        return history

    async def reset_history(self, unique_id: str) -> None:
        response = await self._make_request(method="PUT", path=f"/api/v1/history?unique_id={unique_id}")

    async def add_message(self, message: Message | list[Message], unique_id: str, pass_ai_as_employee: bool = True):
        if not isinstance(message, list):
            message = [message]

        body = {
            "messages": message,
            "pass_ai_as_employee": pass_ai_as_employee
        }
        response = await self._make_request(method="POST", path=f"/api/v1/history/message?unique_id={unique_id}", body=body)

    async def predict_from_history(self, unique_id: str, placeholders: Optional[dict] = {}, auto_insert_ai: bool = True, custom_log_info: Optional[dict] = {}, raise_if_dialog_stopped: bool = False) -> Prediction:
        custom_log_info = dict(**self.custom_log_info, **custom_log_info)
        placeholders = dict(**self.placeholders, **placeholders)

        body = {
            "placeholders": placeholders,
            "custom_log_info": custom_log_info,
            "auto_insert_ai": auto_insert_ai
        }
        response = await self._make_request(method="POST", path=f"/api/v1/history/message?unique_id={unique_id}", body=body)
        match response.status_code:
            case 202:
                if raise_if_dialog_stopped:
                    raise DialogStoppedError("History is marked as stopped")
                else:
                    prediction = Prediction()
                    return prediction
            case 404:
                raise HistoryNotFoundError()
            case 413:
                json = response.json()
                detail = json["detail"]
                if detail.startswith("Maximum token limit"):
                    raise HistoryTooLongError("History is too long to process")
                else:
                    raise MessageLimitExceededError("Message limit for that instance is exceeded")
            case 200: pass
            case _:
                raise UnknownAPIError(f"We don't know what happened. Status code is {response.status_code}")

        json = response.json()
        prediction = Prediction(**json)
        return prediction

    async def predict(self, message: Message | list[Message], unique_id: str, pass_ai_as_employee: bool = True, placeholders: Optional[dict] = {}, auto_insert_ai: bool = True, custom_log_info: Optional[dict] = {}, raise_if_dialog_stopped: bool = False):
        await self.add_message(message, unique_id, pass_ai_as_employee)

        return await self.predict_from_history(unique_id, placeholders, auto_insert_ai, custom_log_info, raise_if_dialog_stopped)