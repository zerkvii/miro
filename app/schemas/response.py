from enum import Enum
from http.client import NOT_FOUND, UNAUTHORIZED
from typing import Optional
import time

from pydantic import BaseModel


class STATUS(Enum):
    BAD_REQUEST = 40000
    SUCCESS = 20000
    INTERNAL_SERVER_ERROR = 50000
    UNKNOWN_ERROR = 60000
    TOKEN_EXPIRE = 50004
    NOT_FOUND = 40400
    UNAUTHORIZED = 40100
    USER_EXIST = 40300


class Response(BaseModel):
    status: STATUS
    info: Optional[str]
    data: object
    timestamp: int = int(time.time())
