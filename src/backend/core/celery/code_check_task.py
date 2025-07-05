import os
import tempfile
from dataclasses import dataclass
from typing import List

import docker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from features.solutions.models import CodeSolution
from .app import app

sync_engine = create_engine(
    "postgresql://Trava:1234@pg:5432/DB_project",
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)


@dataclass
class TestResult:
    input: str
    expected_output: str
    actual_output: str
    passed: bool
    error: str | None = None


@dataclass
class CheckResult:
    status: str  # "success", "failed", "error"
    results: List[TestResult]


# @app.task
# def check_code(solution_id: int):
#     with SessionLocal() as session:
#         solution = session.query(CodeSolution).get(solution_id)
#         time.sleep(20)
#         solution.code = "zzzzzzzzzzzz"
#         session.commit()


@app.task(bind=True)
def check_code(self, solution_id: int):
    with SessionLocal() as db:
        solution = db.query(CodeSolution).get(solution_id)
        if not solution:
            raise ValueError("No solution found")

        try:
            result = run_in_docker(solution)
            # solution.status = result.status
        except Exception as e:
            # solution.status = "error"
            pass
        db.commit()


def run_in_docker(solution) -> CheckResult:
    client = docker.from_env()

    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = os.path.join(tmpdir, "code.py")
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(solution.code)

        results = []
        failed = False

        for test in solution.task.test_cases:  # test.input_data, test.expected_output
            try:
                container_output = client.containers.run(
                    image="code-checker:python",
                    command="python3 /app/code.py",
                    volumes={tmpdir: {"bind": "/app", "mode": "ro"}},
                    mem_limit="128m",
                    network_disabled=True,
                    stdin_open=True,
                    tty=False,
                    detach=False,
                    remove=True,
                    user="1000",  # без root
                    environment={},  # опционально
                    stdout=True,
                    stderr=True,
                    # input=test.input_data.encode("utf-8") if test.input_data else None,
                    working_dir="/app",
                )

                actual_output = container_output.decode().strip()
                expected_output = test.expected_output.strip()

                result = TestResult(
                    input=test.input_data,
                    expected_output=expected_output,
                    actual_output=actual_output,
                    passed=(actual_output == expected_output),
                )
                results.append(result)

                if not result.passed:
                    failed = True

            except docker.errors.ContainerError as e:
                results.append(
                    TestResult(
                        input=test.input_data,
                        expected_output=test.expected_output,
                        actual_output="",
                        passed=False,
                        error=str(e),
                    )
                )
                failed = True

    return CheckResult(status="failed" if failed else "success", results=results)
