from fastapi import APIRouter, Header
from typing import Annotated

from utils.exception import ErrorMessage

from crud.course    import type   as TypeCrud
from schemas.course import type   as TypeSchemas
from crud.course    import course as CourseCrud

# -------------------------------------------------------------------------注册登录
type_router = APIRouter(
    prefix="/type",
    tags=["type管理"],
    deprecated=False
)


# 获取账号所有笔记类型
@type_router.get(
    "/{phone}",
    summary="获取账号所有笔记类型",
    description="返回该账号的所有类型",
    response_model=list[TypeSchemas.CourseOut]
)
async def get(phone: str):
    return await TypeCrud.get_phone(phone)

# 获取笔记类型
@type_router.get(
    "/{phone}/{type_no}",
    summary="获取笔记类型",
    description="返回指定账号的指定类型",
    response_model=TypeSchemas.CourseOut
)
async def get_type(phone: str, type_no: str):
    if await TypeCrud.has_type(phone, type_no):
        return await TypeCrud.get_type(phone, type_no)
    raise ErrorMessage(
        status_code=500,
        message="类型不存在，查询不到"
    )

# 删除类型
@type_router.delete(
    "/{phone}/{type_no}",
    summary="删除类型",
    description="返回删除课程类型数目",
    deprecated=True
)
async def delete(phone: str, type_no: str):
    if await TypeCrud.has_type(phone, type_no):
        await CourseCrud.del_type(phone, type_no)
        return await TypeCrud.delete(phone, type_no)
    raise ErrorMessage(
        status_code=200,
        message="类型不存在，不能删除"
    )
