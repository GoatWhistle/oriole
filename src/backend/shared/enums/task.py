from enum import Enum


class TaskTypeEnum(str, Enum):
    BASE = "base"
    STRING_MATCH = "string_match"
    MULTIPLE_CHOICE = "multiple_choice"
    FILE_UPLOAD = "file_upload"
    CODE = "code"
    FLEXIBLE_AI = "flexible_ai"
    COMBINED = "combined"
