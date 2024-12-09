from fastapi import APIRouter, Header
from typing import Annotated

from schemas.user import token as TokenSchema
from crud.user    import token as TokenCrud
from crud.user    import user  as UserCrud     # 操作数据库的函数

from utils.exception import ErrorMessage


# -------------------------------------------------------------------------token管理
token_router = APIRouter(
    prefix="/token",
    tags=["token管理"],
    deprecated=False
)


# 获取token
@token_router.get(
    "",
    summary="获取token",
    description="返回删除数目 int",
    response_model=list[TokenSchema.TokenOut],
    deprecated=False
)
async def get_phone(phone: Annotated[str, Header()]):
    return await TokenCrud.get_phone(phone)

# 删除token
@token_router.delete(
    "",
    summary="删除token",
    description="返回删除数目 int",
    deprecated=True
)
async def delete_phone_token(phone: Annotated[str, Header()], token: Annotated[str, Header()]) -> int:
    if await TokenCrud.has_token(phone, token):
        return await TokenCrud.delete_token(phone, token)
    else:
        raise ErrorMessage(
            status_code=200,
            message="删除失败，不存在登录信息"
        )







