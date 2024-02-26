from enum import StrEnum


class SenderRole(StrEnum):
    CUSTOMER = "customer"
    """Сообщение от клиента"""

    AI = "ai"
    """Сообщение от нейросети"""

    SYSTEM = "system"
    """Системное сообщение (чаще всего - инструкция или результат выполнения функции)"""

    EMPLOYEE = "employee"
    """Сообщение от сотрудника"""

    INFORMATION = "information"
    """Информационное уведомление (не отправляется в нейросеть, отображается только на фронте)"""
