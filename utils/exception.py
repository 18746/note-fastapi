from fastapi.exceptions import HTTPException
from fastapi import status

def ErrorMessage(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误", error=None):
    return HTTPException(
        status_code=status_code,
        detail=message
    )
