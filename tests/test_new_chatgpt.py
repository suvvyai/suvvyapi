import datetime
import os
import random
import string

from devtools import debug

from suvvyapi import Suvvy, Message

suvvy = Suvvy(os.getenv("TEST1_SUVVY_TOKEN"))


def generate_unique_id() -> str:
    return f"pytest-{datetime.datetime.utcnow().isoformat()}-{''.join(random.choices(string.digits + string.ascii_letters, k=50))}"


unique_id = generate_unique_id()


def test_check_connection():
    assert suvvy.check_connection()


async def test_async_check_connection():
    assert await suvvy.acheck_connection()


def test_get_history():
    r = suvvy.get_history(unique_id)
    debug(r)


def test_reset_history():
    r = suvvy.reset_history(unique_id)
    debug(r)


async def test_aget_history():
    r = await suvvy.aget_history(unique_id)
    debug(r)


async def test_areset_history():
    r = await suvvy.areset_history(unique_id)
    debug(r)


def test_add_message():
    r = suvvy.add_message_to_history(
        unique_id,
        Message(text="Привет!"),
    )
    debug(r)


async def test_async_add_message():
    r = await suvvy.async_add_message_to_history(
        unique_id,
        Message(text="Привет!"),
    )
    debug(r)
