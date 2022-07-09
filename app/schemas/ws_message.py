# from enum import Enum
# from http.client import NOT_FOUND, UNAUTHORIZED
# from typing import Optional
# import time
#
# from pydantic import BaseModel
#
#
# class MSG_TYPE(Enum):
#     GREET: int = 1400
#     BROADCAST: int = 1401
#     PRIVATE: int = 1402
#     RANGE: int = 1403
#     DISCONNECT: int = 1404
#     SELF: int = 1405
#     AUTHENTICATION: int = 20000
#     INSTANT_MSG: int = 30000
#
#
# class Message(BaseModel):
#     msg_type: MSG_TYPE
#     message: Optional[str]
#     data: Optional[object]
#     timestamp: int = int(time.time())
