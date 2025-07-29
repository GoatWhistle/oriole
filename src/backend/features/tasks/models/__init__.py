__all__ = [
    "BaseTask",
    "CodeTask",
    "StringMatchTask",
    "Test",
    "MultipleChoice",
]

from .base import BaseTask
from .code import CodeTask
from .multiple_choice import MultipleChoice
from .string_match import StringMatchTask
from .test import Test
