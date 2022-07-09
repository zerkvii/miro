from typing import Generator

import redis

from app.core.config import settings


def get_redis_conn() -> Generator:
    try:
        con = redis.from_url(settings.REDIS_URL)
        yield con
    finally:
        con.close()
