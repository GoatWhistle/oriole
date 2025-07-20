from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from uuid import uuid4
import time
import logging
import json
from core.logging.logging_exeptions import global_exception_handler
import os


logger = logging.getLogger("app")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        is_dev = os.getenv("IS_DEV", "false").lower() == "true"
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.state.request_id = request_id

        start_time = time.time()

        try:
            body = await request.body()
            try:
                body_data = body.decode("utf-8")
            except Exception:
                body_data = str(body)
        except Exception as e:
            body_data = f"<error reading body: {e}>"

        if not (is_dev):
            body_data = ""

        logger.info(
            json.dumps(
                {
                    "event": "request",
                    "method": request.method,
                    "path": request.url.path,
                    "query": str(request.url.query),
                    "client_ip": request.client.host,
                    "headers": dict(request.headers),
                    "body": body_data[:500],
                    "request_id": request_id,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            return await global_exception_handler(request=request, exc=exc)

        process_time = time.time() - start_time

        logger.info(
            json.dumps(
                {
                    "event": "response",
                    "status_code": response.status_code,
                    "method": request.method,
                    "path": request.url.path,
                    "client_ip": request.client.host,
                    "process_time": f"{process_time:.4f}s",
                    "request_id": request_id,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )

        response.headers["X-Request-ID"] = request_id
        return response
