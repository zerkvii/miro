
from fastapi import Request, Depends
import uuid
from app.services.logger import get_logger
import time
from main import app


@app.middleware("http")
async def log_requests(request: Request, call_next: Request):
    logger = next(get_logger())
    logger.debug(f"rid={uuid.uuid4()} {request.method}:{request.url.path}")
    start_time = time.time()
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.debug(f"rid={uuid.uuid4()} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response
