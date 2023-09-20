from typing import Optional, Literal, Any

import httpx
from devtools import debug

from suvvyapi import Message, HistoryPrediction, Role, Prediction
from suvvyapi._utils import _merge_dicts
from suvvyapi.exceptions.api import InvalidAPITokenError, NegativeBalanceError, InternalAPIError, HistoryNotFoundError, \
    HistoryTooLongError, MessageLimitExceededError, UnknownAPIError


class SuvvyAI:
    def __init__(self, token: str, base_url: str = "https://api.suvvy.ai/",
                 placeholders: dict[str, str] | None = None,
                 source: str | None = None,
                 custom_log_info: dict[str, Any] | None = None):
        self.api_token = token
        self.base_url = base_url.lstrip("/\\")
        self.placeholders = placeholders or {}
        self.source = source or "python_api"
        self.custom_log_info = custom_log_info or {}

    def __call__(self, message: str) -> str:
        history = [Message(text=message, role=Role.HUMAN)]
        prediction = self.predict(history)
        generated = prediction.actual_response.text
        return generated

    def predict(self, history: list[Message], placeholders: dict[str, str] = {}, custom_log_info: dict[str, Any] = {}):
        """Use legacy API (not history API)

        /api/v2/predict/chat
        """
        body = {
            "placeholders": self._make_placeholders(placeholders),
            "custom_log_info": self._make_custom_log_info(custom_log_info),
            "history": [m.model_dump(exclude_none=True) for m in history]
        }
        response = self._make_request(method="POST", path=f"/api/v2/predict/chat",
                                      body=body)
        match response.status_code:
            case 202:
                prediction = HistoryPrediction()
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
            case 200:
                pass
            case _:
                raise UnknownAPIError(f"We don't know what happened. Status code is {response.status_code}")

        json = response.json()
        prediction = Prediction(**json)
        return prediction

    async def apredict(self, history: list[Message], placeholders: dict[str, str] = {}, custom_log_info: dict[str, Any] = {}):
        """Use legacy API (not history API)

        /api/v2/predict/chat
        """
        body = {
            "placeholders": self._make_placeholders(placeholders),
            "custom_log_info": self._make_custom_log_info(custom_log_info),
            "history": [m.model_dump(exclude_none=True) for m in history]
        }
        response = await self._amake_request(method="POST", path=f"/api/v2/predict/chat",
                                      body=body)
        match response.status_code:
            case 202:
                prediction = HistoryPrediction()
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
            case 200:
                pass
            case _:
                raise UnknownAPIError(f"We don't know what happened. Status code is {response.status_code}")

        json = response.json()
        prediction = Prediction(**json)
        return prediction

    def get_history(self, history: list[Message], placeholders: dict[str, str] = {}, custom_log_info: dict[str, Any] = {}):
        """Use legacy API (not history API)

        /api/v2/predict/chat
        """
        body = {
            "placeholders": self._make_placeholders(placeholders),
            "custom_log_info": self._make_custom_log_info(custom_log_info),
            "history": [m.model_dump(exclude_none=True) for m in history]
        }
        response = self._make_request(method="POST", path=f"/api/v2/predict/chat",
                                      body=body)
        match response.status_code:
            case 202:
                prediction = HistoryPrediction()
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
            case 200:
                pass
            case _:
                raise UnknownAPIError(f"We don't know what happened. Status code is {response.status_code}")

        json = response.json()
        prediction = Prediction(**json)
        return prediction


    async def _amake_request(self, method: Literal["GET", "POST", "PUT", "DELETE"], path: str,
                             body: Optional[dict] = {}) -> httpx.Response:
        headers = {
            "Authorization": f"bearer {self.api_token}"
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

    def _make_request(self, method: Literal["GET", "POST", "PUT", "DELETE"], path: str,
                             body: Optional[dict] = {}) -> httpx.Response:
        headers = {
            "Authorization": f"bearer {self.api_token}"
        }
        with httpx.Client(headers=headers, base_url=self.base_url, timeout=300) as c:
            response = c.request(method=method, url=path, json=body)
            if response.status_code == 401:
                raise InvalidAPITokenError("API Token is invalid.")
            if response.status_code == 402:
                raise NegativeBalanceError.from_detail(response.json()["detail"])
            if response.status_code == 500:
                raise InternalAPIError("Internal API error occurred. Contact suvvy.ai support.")
            return response

    def _make_placeholders(self, placeholders: dict[str, str]) -> dict[str, str]:
        return _merge_dicts(self.placeholders, placeholders)

    def _make_custom_log_info(self, custom_log_info: dict[str, str]) -> dict[str, str]:
        return _merge_dicts(self.custom_log_info, custom_log_info)


if __name__ == '__main__':
    api = SuvvyAI("934363.9Lr55IxNv9z66OnKkjw9F-EZEWooSPjAJ_NLWLyyPN4",
                  base_url="https://test.api.suvvy.ai/", placeholders={"name": "Роман"})
    debug(api("Привет!"))