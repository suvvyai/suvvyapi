from enum import StrEnum


class EventMessageType(StrEnum):
    DIALOGUE_STOPPED = "dialogue_stopped"
    """Диалог был остановлен"""

    DIALOGUE_RESUMED = "dialogue_resumed"
    """Диалог был возобновлен"""
