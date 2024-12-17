from fastapi import APIRouter, Header
from fastapi.responses import FileResponse, Response
from typing import Annotated

from utils.exception import ErrorMessage
from utils.file import Folder as FolderConfig, File as FileConfig, get_picture

from crud.course    import course as CourseCrud
from schemas.course import course as CourseSchemas
from crud.course    import unit   as UnitCrud
from crud.course    import type   as TypeCrud
from crud.course    import course as CourseCrud


# -------------------------------------------------------------------------课程笔记
course_router = APIRouter(
    prefix="/course",
    tags=["course管理"],
    deprecated=False
)


# 查询用户所有课程
@course_router.get(
    "",
    summary="查询用户所有课程",
    description="返回该用户的所有课程笔记",
    response_model=list[CourseSchemas.CourseOut]
)
async def get_phone(phone: str):
    course_list = await CourseCrud.get_phone(phone)
    CourseCrud.init_course_picture_url(phone, course_list)
    return course_list

# 查询课程
@course_router.get(
    "/type/{phone}",
    summary="查询指定类型的课程",
    description="返回该用户的指定类型的课程",
    response_model=list[CourseSchemas.CourseOut]
)
async def get_type(phone: str, type_no: str):
    if type_no == "":
        type_no = None
    course_list = await CourseCrud.get_type(phone, type_no)
    CourseCrud.init_course_picture_url(phone, course_list)
    return course_list

# 查询课程
@course_router.get(
    "/{phone}/{course_no}",
    summary="查询指定课程笔记",
    description="返回该用户的指定课程笔记",
    response_model=CourseSchemas.CourseOut
)
async def get_course(phone: str, course_no: str):
    if await CourseCrud.has_course(phone, course_no):
        course = await CourseCrud.get_course(phone, course_no)
        CourseCrud.init_course_picture_url(phone, [course, ])
        return course
    raise ErrorMessage(
        status_code=500,
        message="课程不存在，查询不到"
    )

# 获取课程图标
@course_router.get(
    "/picture/{phone}/{name}/{file_path:path}",
    summary="获取课程图标",
    description="返回图片",
    deprecated=False
)
async def get_picture(phone: str, name: str, file_path: str):
    FolderConfig.open_path(f"/{phone}/{name}")

    print(f"/{phone}/{name}/" + file_path)
    # FolderConfig.open_path(f"/")
    # return FileResponse(img_name)

    return Response(content=FileConfig.read(file_path))

# 删除课程
@course_router.delete(
    "/{phone}/{course_no}",
    summary="删除课程",
    description="返回删除的数量",
    deprecated=True
)
async def delete(phone: str, course_no: str):
    if await CourseCrud.has_course(phone, course_no):
        course_model = await CourseCrud.get_course(phone, course_no)
        # 先删除课程下的所有章节
        await UnitCrud.delete_course(phone, course_no)
        return await CourseCrud.delete(phone, course_model)
    raise ErrorMessage(
        status_code=200,
        message="课程不存在，不能删除"
    )



