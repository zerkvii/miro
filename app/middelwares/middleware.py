from fastapi import Request
from main import app
import time


@app.middleware('http')
async def get_http_req_time(req: Request, call_next):
    start_time = time.time()
    response = await call_next(req)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
