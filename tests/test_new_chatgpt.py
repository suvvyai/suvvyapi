import os

from devtools import debug

from suvvyapi import Suvvy

suvvy = Suvvy(os.getenv("TEST1_SUVVY_TOKEN"))


def test_check_connection():
    assert suvvy.check_connection()


async def test_async_check_connection():
    assert await suvvy.acheck_connection()


def test_get_history():
    r = suvvy.get_history(
        "pytest-2023-12-24T16:42:36.386464-ZSaKvG3D6VcLdV5sdJGl6UrYtJLgdC71G5kU29WYrmBpbg4qDi"
    )
    debug(r)


async def test_aget_history():
    r = await suvvy.aget_history(
        "pytest-2023-12-24T16:42:36.386464-ZSaKvG3D6VcLdV5sdJGl6UrYtJLgdC71G5kU29WYrmBpbg4qDi"
    )
    debug(r)


def test_reset_history():
    r = suvvy.reset_history(
        "pytest-2023-12-24T16:42:36.386464-ZSaKvG3D6VcLdV5sdJGl6UrYtJLgdC71G5kU29WYrmBpbg4qDi"
    )
    debug(r)


async def test_areset_history():
    r = await suvvy.areset_history(
        "pytest-2023-12-24T16:42:36.386464-ZSaKvG3D6VcLdV5sdJGl6UrYtJLgdC71G5kU29WYrmBpbg4qDi"
    )
    debug(r)
