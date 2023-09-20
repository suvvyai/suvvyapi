# An async API wrapper for Suvvy AI
#### built on top of httpx and pydantic :)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/suvvyapi.svg?style=flat-square&logo=python&logoColor=FFE873)](https://pypi.org/project/suvvyapi)
[![PyPI version](https://img.shields.io/pypi/v/suvvyapi.svg?style=flat-square&logo=pypi&logoColor=FFE873)](https://pypi.org/project/suvvyapi)
[![PyPI downloads](https://img.shields.io/pypi/dm/suvvyapi.svg?style=flat-square)](https://pypi.org/project/suvvyapi)

[![Suvvy AI](https://img.shields.io/badge/suvvy.ai-best%20AI%20website-blue?style=flat-square)](https://suvvy.ai)
[![Static Badge](https://img.shields.io/badge/OpenAI-ChatGPT-blue?style=flat-square&logo=openai)](https://openai.com/chatgpt)

## Installation
```shell
pip install -U suvvyapi 
```

## Synchronous Usage
No longer supported! Use

## Asynchronous Usage

```python
import asyncio
from suvvyapi import AsyncSuvvyAPIWrapper, Message

suvvy = AsyncSuvvyAPIWrapper("YOUR_TOKEN")
# You can get your token at https://home.suvvy.ai/

async def main():
    response = await suvvy.predict(Message(text="Say hello to Python!"), "random_id")
    # 'Hello!'

asyncio.run(main())
```

### Building from sources
```shell
git clone https://github.com/barabum0/suvvyapi
cd suvvyapi
pip install -r requirements.txt
python -m build
```