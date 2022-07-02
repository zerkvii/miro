from typing import Optional, List
from fastapi import Header, HTTPException


class PageQuery:
    def __init__(self, page: Optional[int] = None, limit: Optional[int] = None):
        """ common page query

        Args:
            page (Optional[int], optional): _description_. Defaults to None.
            limit (Optional[int], optional): _description_. Defaults to None.
        """
        self.page = page
        self.limit = limit


# async def get_token_header(token: str = Header(...)):
#     if token != 'token':
#         raise HTTPException(status_code=400, detail=f'invalid x_token{x_token}')


# async def get_query_token(token: str = Header(...)):
#     if token != 'gjt-token':
#         raise HTTPException(status_code=400, detail=f'invalid_token{token}')
