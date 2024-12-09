from tortoise.models import Model
from tortoise import fields


class User(Model):
    id          = fields.IntField(pk=True)
    phone       = fields.CharField(max_length=11, description="电话")
    email       = fields.CharField(max_length=50, null=True, default=None, description="邮箱")
    pwd         = fields.CharField(max_length=30, description="密码")

    # 多端登录
    device_num  = fields.IntField(default=1, description="允许同时登录的设备数量")
    # 问题：待完善
    is_admin     = fields.BooleanField(default=False, description="是否为管理员账户")

    expire_time = fields.DatetimeField(null=True, default=None, description="过期时间")

    create_time = fields.DatetimeField(description="创建时间")
    update_time = fields.DatetimeField(description="更新时间")


class UserInfo(Model):
    id       = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, description="姓名")
    picture  = fields.CharField(max_length=30, description="用户头像")
    phone    = fields.CharField(max_length=11, description="电话")


class Token(Model):
    id          = fields.IntField(pk=True)
    phone       = fields.CharField(max_length=11, description="用户phone")
    token       = fields.CharField(max_length=50, description="token")

    time_limit  = fields.IntField(description="有效时间")

    create_time = fields.DatetimeField(description="创建时间")
    update_time = fields.DatetimeField(description="更新时间")



