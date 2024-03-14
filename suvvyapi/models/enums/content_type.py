from enum import StrEnum


class ContentType(StrEnum):
    TEXT = "text"
    """Текстовое сообщение. Соответствует `TextMessageData`"""

    IMAGE = "image"
    """Изображение. Соответствует `ImageMessageData`"""

    AUDIO = "audio"
    """Аудиосообщение. Соответствует `AudioMessageData`"""

    TOOL_CALLS = "tool_calls"
    """Вызов одной/нескольких функций. Соответствует `ToolCallsMessageData`"""

    TOOL_RESPONSE = "tool_response"
    """Результат выполнения функции. Соответствует `ToolResponseMessageData`"""

    EVENT = "event"
    """Сообщения об изменении состояния диалога (разморозка, заморозка и т.п)"""
