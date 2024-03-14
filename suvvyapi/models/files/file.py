import base64
from typing import Any, Self

import httpx
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema, CoreSchema


class Base64File(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=core_schema.str_schema(),
            ),
        )

    @classmethod
    def _validate(cls, v: str) -> Self:
        try:
            base64.b64decode(v, validate=True)
        except ValueError as e:
            raise ValueError(f"Invalid base64 string or file issue: {e}")
        return cls(v)

    @classmethod
    def _serialize(cls, v: Self) -> str:
        return str(v)

    @classmethod
    def from_bytes(cls, b: bytes) -> Self:
        encoded = base64.b64encode(b).decode()
        return cls(encoded)

    @classmethod
    async def afrom_url(cls, url: str) -> Self:
        file_bytes = await _adownload_file(url)
        return cls.from_bytes(file_bytes)

    @classmethod
    def from_url(cls, url: str) -> Self:
        file_bytes = _download_file(url)
        return cls.from_bytes(file_bytes)


async def _adownload_file(url: str) -> bytes:
    """Асинхронная функция для скачивания файла по URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.content


def _download_file(url: str) -> bytes:
    """Синхронная функция для скачивания файла по URL."""
    with httpx.Client() as client:
        response = client.get(url)
        return response.content
