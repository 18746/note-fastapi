from fastapi import UploadFile
from datetime import datetime

from utils.util import time_comparison
from utils.file import Folder as FolderConfig, File as FileConfig, get_picture

from models.user import User as UserModel

from schemas.user import user as  UserSchema

# ----------------------------------------------------------User

# 返回用户信息
async def get(phone: str) -> UserModel:
    return await UserModel.get(phone=phone)

# 判断指定用户是否存在
async def has(phone: str) -> bool:
    return await UserModel.exists(phone=phone)

# 判断账号密码是否正确
async def has_pwd(phone: str, pwd: str) -> bool:
    print(phone, pwd)
    return await UserModel.exists(phone=phone, pwd=pwd)

# 判断账户是否过期
def no_expire(user: UserModel) -> bool:
    return (not bool(user.expire_time)) or time_comparison(user.expire_time) >= 0
# ----------------------------------------------------------------------------------------

# 创建用户
async def create(phone: str, user: dict) -> UserModel:
    if "email" not in user:
        user["email"] = None
    now = datetime.now()

    FolderConfig.open_path("/")
    FolderConfig.create(f"{phone}")

    user_model = await UserModel.create(
        phone=phone,
        pwd=user["pwd"],
        email=user["email"],
        create_time=now,
        update_time=now,
    )

    return user_model

# 更新用户信息
async def update(user_model: UserModel, user: dict) -> UserModel:
    if "email" in user:
        user_model.email = user["email"]
    if "pwd" in user:
        user_model.pwd = user["pwd"]
    if "device_num" in user:
        user_model.device_num = user["device_num"]
    if "is_admin" in user:
        user_model.is_admin = user["is_admin"]
    if "expire_time" in user:
        user_model.is_admin = user["expire_time"]
    user_model.update_time = datetime.now()

    await user_model.save()
    return user_model


# 删除用户
async def delete(phone: str) -> int:
    del_num = await UserModel.filter(phone=phone).delete()
    FolderConfig.open_path("/")
    FolderConfig.delete(f"{phone}")
    return del_num

# ------------------------------------------------------------------------------------
# 更新密码
async def update_pwd(user_model: UserModel, pwd: str) -> UserModel:
    user_model.pwd = pwd
    return await update(user_model, {"pwd": pwd})



