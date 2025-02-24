from fastapi import Request
import time
import logging
from typing import Callable
import uuid

logger = logging.getLogger(__name__)

async def request_middleware(request: Request, call_next: Callable):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(
        f"RequestID: {request_id} Method: {request.method} "
        f"Path: {request.url.path} Time: {process_time:.2f}s"
    )
    
    return response 