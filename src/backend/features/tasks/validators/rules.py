from features.tasks.exceptions import (
    TaskCounterLimitExceededException,
    TaskAlreadySolved,
)


def check_counter_limit(
    task_max_attempts: int,
    user_reply_attempts: int,
) -> None:
    if user_reply_attempts >= task_max_attempts:
        raise TaskCounterLimitExceededException()


def check_task_is_already_correct(
    user_reply_is_correct: bool,
) -> None:
    if user_reply_is_correct:
        raise TaskAlreadySolved()
