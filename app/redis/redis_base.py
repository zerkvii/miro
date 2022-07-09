from redis.client import Redis
from typing import Any, List


def set_key(con: Redis, key: str, value: str) -> None:
    try:
        con.set(key, value)
    except Exception as e:
        print(e)


def get_key(con: Redis, key: str) -> None:
    try:
        return con.get(key)
    except Exception as e:
        print(e)


def list_keys(con: Redis):
    try:
        return con.keys()
    except Exception as e:
        print(e)


def hset_key(con: Redis, key: str, field: str, value: Any) -> None:
    try:
        con.hset(key, field, value)
    except Exception as e:
        print(e)


def hexists(con: Redis, key: str, field: str) -> bool:
    try:
        return con.hexists(key, field)
    except Exception as e:
        print(e)


def hget_key(con: Redis, key: str, field: str) -> str:
    try:
        return con.hget(key, field)
    except Exception as e:
        print(e)


def lpush_key(con: Redis, key: str, value: List[Any]) -> None:
    try:
        con.lpush(key, *value)
    except Exception as e:
        print(e)


def lrange_key(con: Redis, key: str, start: int, end: int) -> List[Any]:
    try:
        return con.lrange(key, start, end)
    except Exception as e:
        print(e)


def rpush_key(con: Redis, key: str, value: List[Any]) -> None:
    try:
        con.rpush(key, *value)
    except Exception as e:
        print(e)


def lpop_key(con: Redis, key: str) -> None:
    try:
        con.lpop(key)
    except Exception as e:
        print(e)


def rpop_key(con: Redis, key):
    try:
        con.rpop(key)
    except Exception as e:
        print(e)
