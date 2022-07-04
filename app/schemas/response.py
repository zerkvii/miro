from enum import Enum
from typing import Optional
import time

from pydantic import BaseModel


class STATUS(Enum):
    BAD_REQUEST = 400
    SUCCESS = 200
    INTERNAL_SERVER_ERROR = 500
    UNKNOWN_ERROR = 60000
    TOKEN_EXPIRE = 50000


class Response(BaseModel):
    status: STATUS
    info: Optional[str]
    data: object
    timestamp: int = int(time.time())
