from fastapi import UploadFile

from models.user import User as UserModel
from models.user  import UserInfo as UserInfoModel

from crud.user    import user as UserCrud     # 操作数据库的函数
from schemas.user import user as UserSchema

from utils import util
from utils.file import Folder as FolderConfig, File as FileConfig
from picture.picture import get_user_img
from core.application import IP_URL

# 返回用户信息 没有的话创建一个
async def get(phone: str) -> UserInfoModel:
    if not await has(phone):
        return await create(phone, {})
    return await UserInfoModel.get(phone=phone)

# 判断用户信息是否存在
async def has(phone: str) -> bool:
    return await UserInfoModel.exists(phone=phone)

# ------------------------------------------------------------------------------------
# 创建用户信息
async def create(phone: str, userinfo: dict) -> UserInfoModel:
    if "username" not in userinfo:
        userinfo["username"] = util.get_no("User_")

    image = get_user_img()
    name_suffix = image.name.split('.')[-1]
    name = util.get_no("img_") + '.' + name_suffix

    FolderConfig.open_path(f"/{phone}")
    FileConfig.write(name, image.context)

    return await UserInfoModel.create(
        username=userinfo["username"],
        phone=phone,
        picture=name,
    )

# 更新用户信息
async def update(userinfo_model: UserInfoModel, userinfo: dict) -> UserInfoModel:
    if "username" in userinfo:
        userinfo_model.username = userinfo["username"]

    if "picture" in userinfo and userinfo["picture"] and type(userinfo["picture"]) != str:
        name = update_picture(userinfo_model, userinfo["picture"])
        userinfo_model.picture = name

    await userinfo_model.save()
    return userinfo_model

def update_picture(user_model: UserInfoModel, picture: UploadFile):
    phone = user_model.phone
    FolderConfig.open_path(f"/{phone}")

    if user_model.picture:
        FileConfig.delete(user_model.picture)

    name_suffix = picture.filename.split(".")[-1]
    name = util.get_no("img_") + '.' + name_suffix
    FileConfig.write(name, picture.file.read())

    return name

# 删除用户信息
async def delete(phone: str) -> int:
    return await UserInfoModel.filter(phone=phone).delete()

# ------------------------------------------------------------------------------------------

# 格式化返回的用户信息（用于接口返回）
def get_info(user: UserModel, user_info: UserInfoModel) -> UserSchema.UserInfoOut:
    userinfo_out = dict(user)
    userinfo_out["username"] = user_info.username
    userinfo_out["picture"] = user_info.picture
    return UserSchema.UserInfoOut(**userinfo_out)

def init_userinfo_picture_url(phone: str, userinfo_list: list[UserInfoModel]):
    for userinfo in userinfo_list:
        userinfo.picture = f'{IP_URL}/user/picture/{phone}/{userinfo.picture}'

