<div align="center">

# SuvvyAPI

[![Supported Python versions](https://img.shields.io/pypi/pyversions/suvvyapi.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/suvvyapi)
[![PyPI version](https://img.shields.io/pypi/v/suvvyapi.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/suvvyapi)
[![PyPI downloads](https://img.shields.io/pypi/dm/suvvyapi.svg)](https://pypi.org/project/suvvyapi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Formatted with: isort](https://img.shields.io/badge/formatted%20with-isort-blue.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

</div>

## About SuvvyAPI 📘

SuvvyAPI is an asynchronous Python API wrapper built on top of `httpx` and `pydantic` for the Suvvy AI API, offering an easy and Pythonic way to interact with the Suvvy AI services.

## Installation 🛠️

To install SuvvyAPI, simply use pip:

```bash
pip install -U suvvyapi
```

## Usage 🚀

### Synchronous Usage

You can use SuvvyAPI synchronously as follows:

```python
from suvvyapi import Suvvy, Message

suvvy = Suvvy("YOUR_TOKEN")
history = suvvy.as_history("random_id")
response = history.predict_add_message("Hi!")
```
*Note: Replace "YOUR_TOKEN" with your actual token from [Suvvy AI](https://home.suvvy.ai/).*

### [More in documentation](https://github.com/suvvyai/suvvyapi/wiki)

## Troubleshooting 💡

For issues and troubleshooting, please refer to the [issues section](https://github.com/suvvyai/suvvyapi/issues) on the GitHub repository.

## Contribution 👥

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.

## License 📄

SuvvyAPI is released under the [MIT License](https://github.com/suvvyai/suvvyapi/blob/main/LICENSE).