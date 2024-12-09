from pydantic import BaseModel, ConfigDict
from datetime import datetime

from utils.pydantic_field import PhoneStrDef, TokenStrDef, TimeLimitIntDef, NameStrDef, EmailStrDef, PasswordStrDef


# 返回token
class TokenOut(BaseModel):
    phone: str = PhoneStrDef("")
    token: str = TokenStrDef("")
    time_limit: int = TimeLimitIntDef(30)
    create_time: str | datetime
    update_time: str | datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
    )

# 更新密码
class UpdatePwdIn(BaseModel):
    old_pwd: str = PasswordStrDef("")
    new_pwd: str = PasswordStrDef("")



