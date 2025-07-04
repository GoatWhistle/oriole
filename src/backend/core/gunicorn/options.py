def get_options(
    host: str,
    port: int,
    workers: int,
    worker_class: str,
    timeout: int,
    reload: bool = False,
) -> dict:
    return {
        "bind": f"{host}:{port}",
        "worker_class": worker_class,
        "workers": workers,
        "timeout": timeout,
        "reload": reload,
    }
