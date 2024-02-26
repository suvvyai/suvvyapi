from enum import StrEnum


class StopReason(StrEnum):
    CONTROL_PHRASE = "control_phrase"
    """Если в сообщении клиента или сотрудника есть контрольная фраза"""

    OTHER = "other"
    """Другая причина"""

    INTERCEPTED_BY_EMPLOYEE = "intercepted_by_employee"
    """Перехвачено сотрудником"""

    MANUAL = "manual"
    """Остановлен вручную"""

    STOP_FILE_TRIGGERED = "stop_file_triggered"
    """Был вызван файл, который останавливает диалог"""
