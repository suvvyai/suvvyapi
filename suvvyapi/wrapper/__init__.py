import httpx


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
            return client.request(method, path, json=body_json, params=params)

    async def _async_request(
        self,
        method: str,
        path: str,
        body_json: dict | None = None,
        params: dict | None = None,
    ) -> httpx.Response:
        with httpx.AsyncClient(
            headers=self._headers, base_url=self._api_url, timeout=300
        ) as client:
            return await client.request(method, path, json=body_json, params=params)
