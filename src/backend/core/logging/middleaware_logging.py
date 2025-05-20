from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"Request: {request.method} {request.url} | Time: {process_time:.4f}s")
        return response