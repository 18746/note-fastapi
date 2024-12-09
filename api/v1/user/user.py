from fastapi import APIRouter, BackgroundTasks, Header, UploadFile
from fastapi.responses import FileResponse, Response
from typing import Annotated

from utils.exception import ErrorMessage
from utils.file import Folder as FolderConfig, File as FileConfig, get_picture

from schemas.user import user     as UserSchema   # 定义数据结构的类
from crud.user    import user     as UserCrud     # 操作数据库的函数
from crud.user    import userinfo as UserInfoCrud     # 操作数据库的函数
from schemas.user import token    as TokenSchema
from crud.user    import token    as TokenCrud

from crud.course    import course as CourseCrud
from crud.course    import type   as TypeCrud
from crud.course    import unit   as UnitCrud


user_router = APIRouter(
    prefix="/user",
    tags=["user管理"],
    deprecated=False
)


# 获取头像
@user_router.get(
    "/picture/{phone}/{file_path:path}",
    summary="获取头像",
    description="返回图片",
    deprecated=False
)
async def get_picture(phone: str, file_path: str):
    FolderConfig.open_path(f"/{phone}")

    print(f"/{phone}/" + file_path)
    return Response(content=FileConfig.read(file_path))

# 账户注册
@user_router.post(
    "/register/{phone}",
    summary="注册账号",
    description="返回注册后的基本信息",
    response_model=UserSchema.UserInfoOut
)
async def create(phone: str, user: UserSchema.CreateUserIn):
    if not await UserCrud.has(phone):
        user = user.model_dump(exclude_unset=True)
        user_model = await UserCrud.create(phone, user)
        user_info = await UserInfoCrud.create(phone, user)

        return UserInfoCrud.get_info(user_model, user_info)
    raise ErrorMessage(
        status_code=500,
        message="该用户已存在，不能创建"
    )

# 账户登录
@user_router.post(
    "/login/{phone}",
    summary="账号登录",
    description="返回登录成功的token信息",
    response_model=TokenSchema.TokenOut
)
async def login(phone: str, user: UserSchema.UserLoginIn, background_tasks: BackgroundTasks):
    pwd = user.pwd
    # 用户密码正确，且未过期
    if await UserCrud.has_pwd(phone, pwd):
        user_model = await UserCrud.get(phone)
        if UserCrud.no_expire(user_model):

            # 删除过期token，及 超出允许的设备数量的token
            background_tasks.add_task(TokenCrud.delete_phone_time_limit, user_model)

            return await TokenCrud.create(phone, user.model_dump(exclude_unset=True))
    raise ErrorMessage(
        status_code=500,
        message="手机号/密码错误，不能登录"
    )

async def token_delete_phone(phone: str) -> int:
    if await UserInfoCrud.has(phone):
        return await UserInfoCrud.delete(phone)
    if await TokenCrud.has_phone(phone):
        return await TokenCrud.delete(phone)
    if await CourseCrud.has(phone):
        return await CourseCrud.delete_all(phone)
    if await TypeCrud.has(phone):
        return await TypeCrud.delete_all(phone)
    if await UnitCrud.has(phone):
        return await UnitCrud.delete_all(phone)
# 删号跑路
@user_router.delete(
    "",
    summary="删号跑路",
    description="返回更新成功/失败 int",
    deprecated=True
)
async def delete(phone: Annotated[str, Header()], background_tasks: BackgroundTasks) -> int:
    background_tasks.add_task(token_delete_phone, phone)
    return await UserCrud.delete(phone)













