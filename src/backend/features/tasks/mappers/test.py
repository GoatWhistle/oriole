from features.tasks.models import Test
from features.tasks.schemas import TestRead


def build_test_read(
    test: Test,
    module_id: int,
    space_id: int,
) -> TestRead:
    return TestRead(
        id=test.id,
        module_id=module_id,
        space_id=space_id,
        task_id=test.task_id,
        correct_output=test.correct_output,
        is_public=test.is_public,
        input_data=test.input_data,
    )


def build_test_read_list(
    module_id: int,
    space_id: int,
    tests: list[Test] | None,
) -> list[TestRead]:
    return [
        build_test_read(
            test=test,
            module_id=module_id,
            space_id=space_id,
        )
        for test in tests
    ]
