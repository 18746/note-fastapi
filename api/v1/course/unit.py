from fastapi import APIRouter, Header
from fastapi.responses import FileResponse, Response
from typing import Annotated

from utils.exception import ErrorMessage
from utils.file import Folder as FolderConfig, File as FileConfig


from crud.course    import course as CourseCrud
from schemas.course import course as CourseSchemas
from crud.course    import unit   as UnitCrud
from schemas.course import unit   as UnitSchemas

# -------------------------------------------------------------------------注册登录
unit_router = APIRouter(
    prefix="/unit",
    tags=["unit管理"],
    deprecated=False
)


# 获取课程的所有章节
@unit_router.get(
    "/{phone}/{course_no}",
    summary="获取课程的所有章节，包含深度",
    description="返回该课程的所有章节",
    # response_model=list[UnitSchemas.UnitOut]
)
async def get_course(phone: str, course_no: str):
    all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
    return UnitCrud.unit_deep_format(all_unit)

# 获取章节
@unit_router.get(
    "/{phone}/{course_no}/{unit_no}",
    summary="获取章节",
    description="返回对应章节信息",
    response_model=UnitSchemas.UnitOut
)
async def get_unit(phone: str, course_no: str, unit_no: str):
    if await UnitCrud.has_unit(phone=phone, course_no=course_no, unit_no=unit_no):
        return await UnitCrud.get_unit(phone=phone, course_no=course_no, unit_no=unit_no)
    raise ErrorMessage(
        status_code=500,
        message="课程单元不存在，查询不到"
    )

# 获取章节内容
@unit_router.get(
    "/{phone}/{course_no}/{unit_no}/content",
    summary="获取章节内容",
    description="返回章节内容",
)
async def get_content(phone: str, course_no: str, unit_no: str):
    if await UnitCrud.has_unit(phone=phone, course_no=course_no, unit_no=unit_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
        curr_unit = [item for item in all_unit if item.unit_no == unit_no][0]

        path = UnitCrud.get_deep_path(curr_course, all_unit, unit_no)
        child = UnitCrud.unit_sort([UnitSchemas.UnitOut(**dict(item)) for item in all_unit if item.parent_no == unit_no])

        content = UnitCrud.get_context(path, phone, curr_course, curr_unit)

        return dict(
            child=child,
            content=content
        )
    raise ErrorMessage(
        status_code=500,
        message="课程单元不存在，查询不到"
    )

# 获取章节内图片
@unit_router.get(
    "/picture/{phone}/{course_no}/{unit_no}/{file_path:path}",
    summary="获取章节内图标",
    description="返回图片",
    deprecated=False
)
async def get_picture(phone: str, course_no: str, unit_no: str, file_path):
    curr_course = await CourseCrud.get_course(phone, course_no)
    all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
    curr_unit = [item for item in all_unit if item.unit_no == unit_no][0]

    path = UnitCrud.get_deep_path(curr_course, all_unit, unit_no)
    if curr_unit.is_menu:
        FolderConfig.open_path(f"/{path}/{curr_unit.name}")
    else:
        FolderConfig.open_path(f"/{path}")

    return Response(content=FileConfig.read(file_path))


# 删除章节
@unit_router.delete(
    "/{phone}/{course_no}/{unit_no}",
    summary="删除章节，子目录也删除",
    description="返回删除的章节数",
    deprecated=True
)
async def delete_unit(phone: str, course_no: str, unit_no: str):
    if await UnitCrud.has_unit(phone, course_no, unit_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
        unit = [item for item in all_unit if item.unit_no == unit_no][0]
        all_unit = [item for item in all_unit if item.unit_no != unit_no]
        parent_child = [item for item in all_unit if item.parent_no == unit.parent_no]

        # 1.1 更改原前后连接，并保存
        prev_unit = [item for item in parent_child if item.next_no == unit.unit_no]
        if prev_unit:
            prev_unit[0].next_no = unit.next_no
            await prev_unit[0].save()

        # 2.1 更新列表name序号
        path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
        await UnitCrud.refresh_list_name(all_unit, unit.parent_no, path)

        # 2.2 深度删除子节点
        all_unit.append(unit)
        FolderConfig.open_path(path)
        if unit.is_menu:
            FolderConfig.delete(unit.name)
        else:
            FileConfig.delete(unit.name + ".md")
            FolderConfig.delete(f"picture.{unit.name}")
        return await UnitCrud.delete_deep_unit(all_unit, unit.unit_no)


