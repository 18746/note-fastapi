from fastapi import BackgroundTasks
from datetime import datetime, timedelta
import random
import base64

from models.user import User as UserModel
from models.user import Token as TokenModel

from schemas.user import user  as UserSchema   # 定义数据结构
from crud.user    import user  as UserCrud     # 操作数据库的函数
from schemas.user import token as TokenSchema

from utils import util

# -----------------------------------------------------------token

# 获取登录信息
async def get_token(phone: str, token: str) -> TokenModel:
    return await TokenModel.get(phone=phone, token=token)

# 获取登录信息
async def get_phone(phone: str) -> list[TokenModel]:
    return await TokenModel.filter(phone=phone)

# 判断账户是否有登录信息
async def has_phone(phone: str) -> bool:
    return await TokenModel.exists(phone=phone)

# 判断token是否有登录信息
async def has_token(phone: str, token: str) -> bool:
    return await TokenModel.exists(phone=phone, token=token)

# 判断token是否过期
def no_expire(token: TokenModel) -> bool:
    return util.time_comparison(token.update_time + timedelta(minutes=token.time_limit)) >= 0

# ------------------------------------------------------------------------------------------
# 创建登录信息
async def create(phone: str, token: dict) -> TokenModel:
    now = datetime.now()
    if "token" not in token:
        token["token"] = new_token(phone=phone)
    if "time_limit" not in token:
        token["time_limit"] = 30

    return await TokenModel.create(
        phone=phone,
        token=token["token"],
        time_limit=token["time_limit"],
        create_time=now,
        update_time=now
    )

# 更新登录信息
async def update(token_model: TokenModel, token: dict) -> TokenModel:
    if "token" in token:
        token_model.token = token["token"]
    if "time_limit" in token:
        token_model.time_limit = token["time_limit"]
    token_model.update_time = datetime.now()

    await token_model.save()
    return token_model



# 删除账户token登录信息
async def delete_token(phone: str, token: str) -> int:
    return await TokenModel.filter(phone=phone, token=token).delete()

# 删除账户token登录信息
async def delete(phone: str) -> int:
    return await TokenModel.filter(phone=phone).delete()

# -----------------------------------------------------------------------------------------------------
# 刷新token
async def refresh(token_model: TokenModel) -> TokenModel:
    return await update(token_model, {"token": new_token(phone=token_model.phone)})

# 删除账户过期的登录信息，超出设备数量的也删除
async def delete_phone_time_limit(user: UserModel):
    # 查询账户所有登录信息
    token_list = await TokenModel.filter(phone=user.phone).order_by('-create_time')
    # 分拣 过期与没过期的登录信息
    expire_token_value: list[TokenModel] = [item for item in token_list if not no_expire(item)]
    no_expire_token_value: list[TokenModel] = [item for item in token_list if no_expire(item)]

    # 超出允许登录的设备数量的 token 也算作过期
    device_num = user.device_num
    expire_token_value.extend(no_expire_token_value[device_num:])

    # 全部删除
    for item in expire_token_value:
        await item.delete()

def new_token(phone: str):
    date_time = datetime.now()
    date_time_strf = date_time.strftime('%Y%m%d%H%M')

    random.seed(date_time.timestamp() * 100)
    ran_int = random.randint(100000, 999999)

    s = f"{date_time_strf}{ran_int}"
    s_bytes = s.encode('utf-8')
    return f"Token_{phone}_{base64.b64encode(s_bytes).decode("utf-8")}"



