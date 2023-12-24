import os

from suvvyapi import Suvvy

suvvy = Suvvy(os.getenv("TEST1_SUVVY_TOKEN"))


def test_check_connection():
    assert suvvy.check_connection()


async def test_async_check_connection():
    assert await suvvy.acheck_connection()
