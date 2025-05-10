def get_options(
    host: str,
    port: int,
    workers: int,
    timeout: int,
) -> dict:
    return {
        "bind": f"{host}:{port}",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "workers": workers,
        "timeout": timeout,
    }
