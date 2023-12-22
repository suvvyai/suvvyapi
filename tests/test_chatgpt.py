import datetime
import os
import random
import string

from suvvyapi import SuvvyAPIWrapper, Message, AsyncSuvvyAPIWrapper

suvvy = SuvvyAPIWrapper(token=os.getenv("TEST1_SUVVY_TOKEN"))
async_suvvy = AsyncSuvvyAPIWrapper(token=os.getenv("TEST1_SUVVY_TOKEN"))


def generate_unique_id() -> str:
    return f"pytest-{datetime.datetime.utcnow().isoformat()}-{''.join(random.choices(string.digits + string.ascii_letters, k=50))}"


def test_sync_message_responded():
    unique_id = generate_unique_id()
    response = suvvy.predict(Message(text="Hello"), unique_id=unique_id)

    assert response.actual_response is not None


def test_sync_message_interrupted():
    unique_id = generate_unique_id()

    # Interrupt reason - control phrase
    response = suvvy.predict(Message(text="Хорошо, подождите минутку"), unique_id=unique_id)

    assert response.actual_response is None


async def test_async_message_responded():
    unique_id = generate_unique_id()
    response = await async_suvvy.predict(Message(text="Hello"), unique_id=unique_id)

    assert response.actual_response is not None


async def test_async_message_interrupted():
    unique_id = generate_unique_id()

    # Interrupt reason - control phrase
    response = await async_suvvy.predict(Message(text="Хорошо, подождите минутку"), unique_id=unique_id)

    assert response.actual_response is None

