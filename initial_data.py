import json
import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.redis.redis_base import list_keys, set_key, get_key
from app.services.redis import get_redis_conn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    # con = next(get_redis_conn())
    # set_key(con, "tesee", json.dumps({'a': [1, 2, 3], 'b': [4, 5, 6]}))
    # print(list_keys(con)[0])
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
