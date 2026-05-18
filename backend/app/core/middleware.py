from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
import logging

logger = logging.getLogger("CapCommanderAPI")

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Enterprise-grade logging middleware to track API performance and requests.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request details
        method = request.method
        url = request.url.path
        client_host = request.client.host
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        status_code = response.status_code
        
        logger.info(
            f"Method: {method} | Path: {url} | Status: {status_code} | "
            f"Latency: {process_time:.2f}ms | Client: {client_host}"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
