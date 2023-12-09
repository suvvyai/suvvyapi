<div align="center">

# SuvvyAPI

[![Supported Python versions](https://img.shields.io/pypi/pyversions/suvvyapi.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/suvvyapi)
[![PyPI version](https://img.shields.io/pypi/v/suvvyapi.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/suvvyapi)
[![PyPI downloads](https://img.shields.io/pypi/dm/suvvyapi.svg)](https://pypi.org/project/suvvyapi)

</div>

## About SuvvyAPI

SuvvyAPI is an asynchronous Python API wrapper built on top of `httpx` and `pydantic` for the Suvvy AI API, offering an easy way to interact with the Suvvy AI services in a Pythonic way.

## Installation

To install SuvvyAPI, simply use pip:

```bash
pip install -U suvvyapi
```

## Usage

### Synchronous Usage

You can use SuvvyAPI synchronously as follows:

```python
from suvvyapi import SuvvyAPIWrapper, Message

suvvy = SuvvyAPIWrapper("YOUR_TOKEN")
response = suvvy.predict(Message(text="Say hello to Python!"), "random_id")
```
*Note: Replace "YOUR_TOKEN" with your actual token from [Suvvy AI](https://home.suvvy.ai/).*


### Asynchronous Usage

For asynchronous usage:

```python
import asyncio
from suvvyapi import AsyncSuvvyAPIWrapper, Message

suvvy = AsyncSuvvyAPIWrapper("YOUR_TOKEN")

async def main():
    response = await suvvy.predict(Message(text="Say hello to Python!"), "random_id")

asyncio.run(main())
```

## Building from Sources

If you prefer to build from source:

```bash
git clone https://github.com/barabum0/suvvyapi
cd suvvyapi
pip install -r requirements.txt
python -m build
```

## Contribution

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.

## License

SuvvyAPI is released under the [MIT License](https://github.com/suvvyai/suvvyapi/blob/main/LICENSE).
