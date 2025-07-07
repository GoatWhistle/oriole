from features.tasks.models import Test
from features.tasks.schemas import TestRead


def build_test_read_list(
    tests: list[Test],
) -> list[TestRead]:
    return [test.get_validation_schema() for test in tests]
