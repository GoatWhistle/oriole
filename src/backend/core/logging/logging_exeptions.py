from fastapi import Request
from fastapi.responses import JSONResponse
from logging import getLogger
import json
from uuid import uuid4
import traceback


logger = getLogger("app")
traceback_logger = getLogger("traceback_logger")


async def global_exception_handler(request: Request, exc: Exception):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.request_id = request_id

    logger.error(
        json.dumps(
            {
                "event": "response",
                "status_code": 500,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host,
                "headers": dict(request.headers),
                "exception": str(exc),
                "request_id": request_id,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )
    traceback_logger.error(traceback.format_exc())

    response = JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "request_id": request_id},
    )
    response.headers["X-Request-ID"] = request_id
    return response
