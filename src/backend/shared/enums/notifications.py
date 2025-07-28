from enum import StrEnum, IntEnum


class NotificationTypeEnum(StrEnum):
    BASE = "base"
    TASK_SOLVED = "task_solved"
    MODULE_ACTIVITY = "module_activity"
    NEW_TASK = "new_task"
    DEADLINE_24H = "deadline_24h"
    DEADLINE_1H = "deadline_1h"
    DEADLINE_OVERDUE = "deadline_overdue"
    CHAT_MESSAGE = "chat_message"

class NotificationChannelType(IntEnum):
    EMAIL = 0
    TELEGRAM = 1