from features.tasks.exceptions import (
    InvalidStringMatchTaskWithNumberConfiguration,
    InvalidStringMatchTaskWithStringConfiguration,
)


def validate_string_match_task_configuration(task) -> None:
    if task.compare_as_number:
        if task.is_case_sensitive is not None or task.normalize_whitespace is not None:
            raise InvalidStringMatchTaskWithNumberConfiguration()
    else:
        if task.is_case_sensitive is None or task.normalize_whitespace is None:
            raise InvalidStringMatchTaskWithStringConfiguration()
