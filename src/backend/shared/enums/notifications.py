from enum import StrEnum

class NotificationTypeEnum(StrEnum):
    BASE = "base"
    TASK_SOLVED = "task_solved"
    MODULE_ACTIVITY = "module_activity"
    NEW_TASK = "new_task"
    DEADLINE_REMINDER = "deadline_reminder"