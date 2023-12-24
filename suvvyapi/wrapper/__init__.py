import httpx

from suvvyapi import History
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
    raise exceptions[response.status_code](response.json().get("detail", None))


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

    def get_history(self, unique_id: str) -> History:
        """Get history by unique_id"""
        r = self._sync_request(
            "GET", "/api/v1/history", params={"unique_id": unique_id}
        )
        return History(**r.json())

    async def aget_history(self, unique_id: str) -> History:
        """Get history by unique_id"""
        r = await self._async_request(
            "GET", "/api/v1/history", params={"unique_id": unique_id}
        )
        return History(**r.json())

    def reset_history(self, unique_id: str) -> History:
        """Reset history by unique_id and return deleted history"""
        r = self._sync_request(
            "PUT", "/api/v1/history", params={"unique_id": unique_id}
        )
        return History(**r.json()["deleted_history"])

    async def areset_history(self, unique_id: str) -> History:
        """Reset history by unique_id and return deleted history"""
        r = await self._async_request(
            "PUT", "/api/v1/history", params={"unique_id": unique_id}
        )
        return History(**r.json()["deleted_history"])
