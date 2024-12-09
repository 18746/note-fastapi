from fastapi import APIRouter, BackgroundTasks, Header, UploadFile, Form
from typing import Annotated
from datetime import datetime

from schemas.user import user  as UserSchema   # 定义数据结构的类
from crud.user    import user  as UserCrud     # 操作数据库的函数
from crud.user    import userinfo as UserInfoCrud     # 操作数据库的函数
from schemas.user import token as TokenSchema
from crud.user    import token as TokenCrud

from utils.exception import ErrorMessage

# -------------------------------------------------------------------------------------------账号操作
login_router = APIRouter(
    prefix="/login",
    tags=["账号操作"],
    deprecated=False
)

# 获取用户基本信息
@login_router.get(
    "/info",
    summary="获取用户基本信息",
    description="获取用户的 用户名，手机号等信息",
    response_model=UserSchema.UserInfoOut
)
async def get_userinfo(phone: Annotated[str, Header()]):
    # 账户存在且没过期
    user = await UserCrud.get(phone)
    user_info = await UserInfoCrud.get(phone)

    return UserInfoCrud.get_info(user, user_info)

# 更新用户数据
@login_router.put(
    "/info",
    summary="更新用户基本信息",
    description="返回更新后的信息"
)
async def update(phone: Annotated[str, Header()], user_info: Annotated[UserSchema.UpdateUserInfoIn, Form()]):
    # 账户存在未过期，且存在token登录信息
    user_dict = user_info.model_dump(exclude_unset=True)

    user_model = await UserCrud.get(phone)
    userinfo_model = await UserInfoCrud.get(phone)

    if user_dict.keys():
        user_model = await UserCrud.update(user_model, user_dict)
        userinfo_model = await UserInfoCrud.update(userinfo_model, user_dict)

    return UserInfoCrud.get_info(user_model, userinfo_model)

# 更改头像
@login_router.put(
    "/info/picture",
    summary="更改用户头像",
    description="返回更新成功/失败 bool",
)
async def update_picture(phone: Annotated[str, Header()], picture: UploadFile):
    user_model = await UserInfoCrud.get(phone)
    return UserInfoCrud.update_picture(user_model, picture)

# 更改密码
@login_router.put(
    "/pwd",
    summary="更改用户密码",
    description="返回更新成功/失败 bool",
)
async def update_pwd(phone: Annotated[str, Header()], pwds: TokenSchema.UpdatePwdIn):
    if pwds.old_pwd == pwds.new_pwd:
        raise ErrorMessage(
            status_code=500,
            message="新密码与老密码相同"
        )
    # 用户密码正确
    if await UserCrud.has_pwd(phone, pwds.old_pwd):
        user_model = await UserCrud.get(phone)
        await UserCrud.update_pwd(user_model, pwds.new_pwd)
        return True
    raise ErrorMessage(
        status_code=500,
        message="密码输入错误，不能修改"
    )

# 刷新token
@login_router.put(
    "/refresh",
    summary="刷新token",
    description="返回更新后的token信息",
    response_model=TokenSchema.TokenOut
)
async def refresh_token(phone: Annotated[str, Header()], token: Annotated[str, Header()],  background_tasks: BackgroundTasks):
    user_model = await UserCrud.get(phone)
    # 删除过期token，及 超出允许的设备数量的token
    background_tasks.add_task(TokenCrud.delete_phone_time_limit, user_model)

    token_model = await TokenCrud.get_token(phone, token)

    return await TokenCrud.refresh(token_model)

# 注销登录
@login_router.delete(
    "/logout",
    summary="用户注销登录",
    description="返回更新成功/失败 int",
)
async def logout(phone: Annotated[str, Header()], token: Annotated[str, Header()]) -> int:
    return await TokenCrud.delete_token(phone, token)

# 删号跑路
@login_router.delete(
    "",
    summary="删号跑路，账号指定过期",
    description="返回更新成功/失败 int",
)
async def delete(phone: Annotated[str, Header()]) -> bool:
    user_model = await UserCrud.get(phone)
    user_model.expire_time = datetime.now()
    await user_model.save()
    return True







