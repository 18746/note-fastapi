from fastapi import APIRouter, BackgroundTasks, Header, UploadFile, Form
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from utils.pydantic_field import PhoneStrDef, PasswordStrDef, NameStrDef, EmailStrDef, TimeLimitIntDef


# -----------------------------------------------user
# 创建用户
class CreateUserIn(BaseModel):
    pwd: str = PasswordStrDef("")

# 更新用户信息
class UpdateUserInfoIn(BaseModel):
    email: str | None = EmailStrDef(None)
    device_num: int | None = None

    username: str = NameStrDef(None)    # info中的 字段

    picture: UploadFile | str = ''

# 返回的用户信息
class UserInfoOut(BaseModel):
    username: str = NameStrDef("")   # info
    picture: str = ""                # info
    phone: str = PasswordStrDef("")
    email: str | None = EmailStrDef(None)
    device_num: int
    expire_time: datetime | None = None
    create_time: datetime
    update_time: datetime
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    )


# 账户登录
class UserLoginIn(BaseModel):
    pwd: str = PasswordStrDef("")
    time_limit: int | None = TimeLimitIntDef(30)
# ---------------------------------------------------------------------------




