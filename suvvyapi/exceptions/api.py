import re
from typing import Optional


class InvalidAPITokenError(BaseException):
    """Raised, when API token is invalid"""


class NegativeBalanceError(BaseException):
    """Raised, when your Suvvy AI balance is under zero"""

    balance: Optional[int] = None

    @classmethod
    def from_detail(cls, detail: str) -> "NegativeBalanceError":
        exc = cls("Your balance is under zero")

        balance_match = re.search(pattern=r"(\(\d*\))", string=detail)
        if balance_match is None:
            return exc

        balance = int(balance_match.group(0).strip("()"))
        exc.balance = balance
        return exc


class HistoryStoppedError(BaseException):
    """Raised, when history is marked as stopped"""


class HistoryNotFoundError(BaseException):
    """Raised, when history with this unique id is not found"""


class MessageNotFoundError(BaseException):
    """Raised, when message with this message_id is not found"""


class InternalMessageAdded(BaseException):
    """Raised, when message with internal role or role-specific information is added"""


class HistoryTooLongError(BaseException):
    """Raised, when history is too long to process"""


class MessageLimitExceededError(BaseException):
    """Raised, when message limit for that instance is exceeded"""


class UnknownAPIError(BaseException):
    """Raised, when WE DON'T KNOW WHAT HAPPENED"""


class InternalAPIError(BaseException):
    """Raised, when internal api error occurred"""
