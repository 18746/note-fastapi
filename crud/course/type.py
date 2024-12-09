from datetime import datetime

from utils.util import get_no

from models.course import Type as TypeModel

from schemas.course import type as TypeSchemas
# -------------------------------------------------------------------------------------查
async def get_phone(phone: str) -> list[TypeModel]:
    return await TypeModel.filter(phone=phone)

async def get_type(phone: str, type_no: str) -> TypeModel:
    return await TypeModel.get(phone=phone, type_no=type_no)

async def has(phone: str) -> bool:
    return await TypeModel.exists(phone=phone)

async def has_type(phone: str, type_no: str) -> bool:
    return await TypeModel.exists(phone=phone, type_no=type_no)

async def has_name(phone: str, name: str) -> bool:
    return await TypeModel.exists(phone=phone, name=name)


# ----------------------------------------------------------------------------------------------增删改
async def create(phone: str, type_in: dict) -> TypeModel:
    if "type_no" not in type_in:
        type_in["type_no"] = get_no("T_")
    if "name" not in type_in:
        type_in["name"] = get_no("TName_")
    now = datetime.now()
    return await TypeModel.create(
        type_no=type_in["type_no"],
        name=type_in["name"],
        phone=phone,
        create_time=now,
        update_time=now,
    )

async def update(type_model: TypeModel, type_in: dict) -> TypeModel:
    if "name" in type_in:
        type_model.name = type_in["name"]

    type_model.update_time = datetime.now()
    await type_model.save()
    return type_model

async def delete(phone: str, type_no: str) -> int:
    return await TypeModel.filter(phone=phone, type_no=type_no).delete()

async def delete_all(phone: str) -> int:
    return await TypeModel.filter(phone=phone).delete()


# ------------------------------------------------------------------------------

