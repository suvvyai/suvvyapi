from enum import Enum


class Role(str, Enum):
    HUMAN = "human"
    AI = "ai"
    FUNCTION_CALL = "function_call"
    FUNCTION_RESULT = "function_result"
    IMAGE_MESSAGE = "sent_image"
    AUDIO_MESSAGE = "audio_message"
