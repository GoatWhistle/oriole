from fastapi import HTTPException, status


def check_counter_limit(
    user_id: int,
    task_id: int,
    task_max_attempts: int,
    user_reply_attempts: int,
) -> None:
    if user_reply_attempts >= task_max_attempts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The number of user {user_id} attempts is more than the number of maximum attempts of task {task_id}",
        )


def check_task_is_already_correct(
    user_id: int,
    task_id: int,
    user_reply_is_correct: bool,
) -> None:
    if user_reply_is_correct:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Task {task_id} has already been solved correctly by user {user_id}.",
        )
