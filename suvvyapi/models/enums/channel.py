from enum import StrEnum


class Channel(StrEnum):
    API = "api"
    TELEGRAM_BOT = "telegram_bot"
    JIVO = "jivo"
    BITRIX = "bitrix"
    AMOCRM = "amocrm"
    WHATSAPP = "whatsapp"
    USEDESK = "usedesk"
    KOMMO = "kommo"
    PLANFIX = "planfix"
    TEST_CHAT = "test_chat"
