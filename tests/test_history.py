# mypy: ignore_errors
import datetime
import os
import random
import string

from devtools import debug

from suvvyapi import Suvvy, Message

suvvy = Suvvy(os.getenv("TEST1_SUVVY_TOKEN"), api_url="https://test.api.suvvy.ai")


def generate_unique_id() -> str:
    """Generate a unique dialog ID"""
    return (
        f"pytest-"
        f"{datetime.datetime.utcnow().isoformat()}-"
        f"{''.join(random.choices(string.digits + string.ascii_letters, k=50))}"
    )


unique_id = generate_unique_id()
async_unique_id = generate_unique_id()

history = suvvy.as_history(unique_id)
async_history = suvvy.as_history(async_unique_id)


def test_get():
    r = history.get()
    debug(r)


async def test_aget():
    r = await async_history.aget()
    debug(r)


def test_add_message():
    r = history.add_message(Message(text="Привет!"))
    debug(r)


async def test_async_add_message():
    r = await async_history.async_add_message(Message(text="Привет!"))
    debug(r)


def test_predict():
    r = history.predict()
    debug(r)


async def test_apredict():
    r = await async_history.apredict()
    debug(r)


def test_reset():
    r = history.reset()
    debug(r)


async def test_areset():
    r = await async_history.areset()
    debug(r)


def test_predict_add_message():
    r = history.predict_add_message(Message(text="Привет!"))
    debug(r)


async def test_apredict_add_message():
    r = await async_history.apredict_add_message(Message(text="Привет!"))
    debug(r)
