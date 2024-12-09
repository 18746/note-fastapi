from tortoise.models import Model
from tortoise import fields

class Type(Model):
    id          = fields.IntField(pk=True)
    phone       = fields.CharField(max_length=11, description="电话")
    type_no     = fields.CharField(max_length=30, description="类型唯一值")

    name        = fields.CharField(max_length=30, description="类型名")

    create_time = fields.DatetimeField(description="创建时间")
    update_time = fields.DatetimeField(description="更新时间")


class Course(Model):
    id          = fields.IntField(pk=True)
    phone       = fields.CharField(max_length=11, description="电话")
    course_no   = fields.CharField(max_length=30, description="课程序号")

    name        = fields.CharField(max_length=60, description="课程名")
    picture     = fields.CharField(max_length=30, description="课程图片")
    type_no     = fields.CharField(null=True, default=None, max_length=20, description="类型唯一值")

    description = fields.CharField(max_length=300, description="课程简介")
    update_num  = fields.IntField(default=1, description="更新次数")
    click_count = fields.IntField(default=1, description="点击次数")

    create_time = fields.DatetimeField(description="创建时间")
    update_time = fields.DatetimeField(description="更新时间")


class Unit(Model):
    id          = fields.IntField(pk=True)
    phone       = fields.CharField(max_length=11, description="电话")
    course_no   = fields.CharField(max_length=30, description="课程序号")
    unit_no     = fields.CharField(max_length=30, description="单元序号")

    name        = fields.CharField(max_length=60, description="文件名")

    is_menu     = fields.BooleanField(default=False, description="是否为菜单")
    parent_no   = fields.CharField(null=True, max_length=30, description="父节点 单元序号")
    next_no     = fields.CharField(null=True, max_length=30, description="后一个 单元序号")

    create_time = fields.DatetimeField(description="创建时间")
    update_time = fields.DatetimeField(description="更新时间")



