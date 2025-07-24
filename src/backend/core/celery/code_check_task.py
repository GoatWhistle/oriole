import os

import docker
from requests.exceptions import ReadTimeout, ConnectionError, ConnectTimeout
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings, BASE_DIR
from features import CodeTask, Test
from features.solutions.exceptions.existence import SolutionNotFoundException
from features.solutions.models import CodeSolution
from features.tasks.exceptions import TaskNotFoundException
from shared.enums import SolutionStatusEnum
from .app import app

sync_engine = create_engine(str(settings.db.sync_url))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def run_code_in_container(
    code: str,
    input_data: str,
    mem_limit: str,
    time_limit: float,
):
    client = docker.from_env()

    container = None
    timed_out = False

    try:
        image, build_logs = client.images.build(
            path=os.path.join(BASE_DIR, "core/celery/runtimes/python"),
            dockerfile="Dockerfile",
            tag="runner-python:3.9",
            rm=True,
        )
        container = client.containers.run(
            image=image,
            command=["python", "-c", code],
            stdin_open=bool(input_data),
            stdout=True,
            stderr=True,
            tty=False,
            detach=True,
            network_mode="none",
            mem_limit=mem_limit,
            memswap_limit=mem_limit,
            oom_kill_disable=False,
            read_only=True,
            privileged=False,
            nano_cpus=1_000_000_000,
            user="nobody",
            security_opt=["no-new-privileges:true"],
            cap_drop=["ALL"],
        )
        if input_data:
            socket = container.attach_socket(params={"stdin": 1, "stream": 1})
            socket._sock.send(input_data.encode() + b"\n")
            socket._sock.close()

        try:
            result = container.wait(timeout=time_limit + 1)
        except (ReadTimeout, ConnectionError, ConnectTimeout):
            timed_out = True
            return "", "Time limit exceeded", -1, True, False

        stdout = container.logs(stdout=True, stderr=False).decode().strip()
        stderr = container.logs(stdout=False, stderr=True).decode().strip()
        status_code = result.get("StatusCode", 0)
        oom_killed = container.attrs.get("State", {}).get("OOMKilled", False)

        return stdout, stderr, status_code, timed_out, oom_killed
    finally:
        if container:
            container.remove(force=True)


@app.task(name="core.celery.code_check_task.check_code")
def check_code(solution_id):
    with SessionLocal() as session:
        solution = session.get(CodeSolution, solution_id)
        if not solution:
            raise SolutionNotFoundException()

        task = session.get(CodeTask, solution.task_id)
        if not task:
            raise TaskNotFoundException()

        tests = session.query(Test).filter(Test.task_id == task.id).all()

        mem_limit = f"{max(task.memory_limit, 6)}m"
        time_limit = task.time_limit / 1000.0

        for test in tests:
            stdout, stderr, status_code, timed_out, oom_killed = run_code_in_container(
                solution.code, test.input_data, mem_limit, time_limit
            )

            result = analyze_result(
                stdout, stderr, status_code, timed_out, oom_killed, solution, test
            )
            if result:
                break
        else:
            solution.status = SolutionStatusEnum.ACCEPTED.value
            solution.is_correct = True
            result = {"status": "success", "correct": True}

        session.commit()
        return result


def analyze_result(stdout, stderr, status_code, timed_out, oom_killed, solution, test):
    result = 0
    if timed_out:
        solution.status = SolutionStatusEnum.TIME_LIMIT_EXCEEDED.value
        result = {
            "status": "error",
            "error": "Time limit exceeded",
            "output": stdout,
        }
    elif oom_killed or status_code == 137 or "memory" in stderr.lower():
        solution.status = SolutionStatusEnum.MEMORY_LIMIT_EXCEEDED.value
        result = {
            "status": "error",
            "error": "Memory limit exceeded",
            "output": stdout,
        }
    elif stderr:
        solution.status = SolutionStatusEnum.RUNTIME_ERROR.value
        result = {"status": "error", "error": stderr, "output": stdout}
    elif stdout.strip() != test.correct_output:
        solution.status = SolutionStatusEnum.WRONG_ANSWER.value
        result = {
            "status": "fail",
            "output": stdout,
            "expected": test.correct_output,
            "correct": False,
        }
    return result
