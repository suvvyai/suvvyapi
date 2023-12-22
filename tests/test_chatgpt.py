import datetime
import os
import random
import string

from suvvyapi import SuvvyAPIWrapper, Message, AsyncSuvvyAPIWrapper

suvvy_1 = SuvvyAPIWrapper(token=os.getenv("TEST1_SUVVY_TOKEN"))
async_suvvy_1 = AsyncSuvvyAPIWrapper(token=os.getenv("TEST1_SUVVY_TOKEN"))


def test_sync_message_responded():
    unique_id = f"pytest-{datetime.datetime.utcnow().isoformat()}-{random.choices(string.digits + string.ascii_letters, k=50)}"
    response = suvvy_1.predict(Message(text="Hello"), unique_id=unique_id)

    assert response.actual_response is not None


def test_sync_message_interrupted():
    unique_id = f"pytest-{datetime.datetime.utcnow().isoformat()}-{random.choices(string.digits + string.ascii_letters, k=50)}"

    # Interrupt reason - control phrase
    response = suvvy_1.predict(Message(text="Хорошо, подождите минутку"), unique_id=unique_id)

    assert response.actual_response is None
