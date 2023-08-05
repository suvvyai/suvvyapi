# An async API wrapper for Suvvy AI

[![Supported Python versions](https://img.shields.io/pypi/pyversions/suvvyapi.svg?style=flat-square&logo=python&logoColor=FFE873)](https://pypi.org/project/suvvyapi)
[![PyPI version](https://img.shields.io/pypi/v/suvvyapi.svg?style=flat-square&logo=pypi&logoColor=FFE873)](https://pypi.org/project/aiogram-translation)
[![PyPI downloads](https://img.shields.io/pypi/dm/suvvyapi.svg?style=flat-square)](https://pypi.org/project/suvvyapi)

[![suvvy.ai](https://img.shields.io/badge/suvvy.ai-best%20AI%20website-blue?style=flat-square)](https://suvvy.ai)

## Installation
```shell
pip install -U suvvyapi 
```

## Synchronous Usage
```python
from suvvyapi import SuvvyAPIWrapper, Message

suvvy = SuvvyAPIWrapper("YOUR_TOKEN")
# You can get your token at https://home.suvvy.ai/

response = suvvy.predict(Message(text="Say hello to Python!"), "random_id")
# 'Hello!'
```

## Asynchronous Usage

```python
import asyncio
from suvvyapi import AsyncSuvvyAPIWrapper, Message

suvvy = AsyncSuvvyAPIWrapper("YOUR_TOKEN")
# You can get your token at https://home.suvvy.ai/

async def main():
    response = suvvy.predict(Message(text="Say hello to Python!"), "random_id")
    # 'Hello!'

asyncio.run(main())
```