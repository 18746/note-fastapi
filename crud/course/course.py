from fastapi import UploadFile
from datetime import datetime

from models.course import Course as CourseModel

from utils import util
from utils.file import Folder as FolderConfig, File as FileConfig, get_course_img
from core.application import IP_URL

# -----------------------------------------------------------------------------查
async def get_phone(phone: str) -> list[CourseModel]:
    return await CourseModel.filter(phone=phone)

async def has(phone: str) -> bool:
    return await CourseModel.exists(phone=phone)

async def has_course(phone: str, course_no: str) -> bool:
    return await CourseModel.exists(phone=phone, course_no=course_no)

async def has_name(phone: str, name: str, course_no: str = "") -> bool:
    return await CourseModel.exists(phone=phone, name=name, course_no__not=course_no)

async def get_course(phone: str, course_no: str) -> CourseModel:
    return await CourseModel.get(phone=phone, course_no=course_no)

async def get_type(phone: str, type_no: str | None) -> list[CourseModel]:
    return await CourseModel.filter(phone=phone, type_no=type_no).order_by('-update_time')
# ----------------------------------------------------------------------------------增删改
async def create(phone: str, course: dict) -> CourseModel:
    if "course_no" not in course:
        course["course_no"] = util.get_no("C_")
    if "name" not in course:
        course["name"] = util.get_no("CName_")
    if "type_no" not in course or course["type_no"] == "":
        course["type_no"] = None
    if "description" not in course:
        course["description"] = ""
    if "update_num" not in course:
        course["update_num"] = 1
    if "click_count" not in course:
        course["click_count"] = 1

    FolderConfig.open_path(f"/{phone}")
    FolderConfig.create(course["name"])

    now = datetime.now()
    course_model = await CourseModel.create(
        course_no=course["course_no"],
        name=course["name"],
        phone=phone,
        picture="",
        type_no=course["type_no"],
        description=course["description"],
        update_num=course["update_num"],
        click_count=course["click_count"],
        create_time=now,
        update_time=now,
    )

    if "picture" in course and course["picture"] and type(course["picture"]) != str:
        name = update_picture(course_model, course["picture"])
        course_model.picture = name
    else:
        image = get_course_img()
        name_suffix = image.name.split('.')[-1]
        FolderConfig.open_path(f"/{phone}/{course_model.name}")
        name = util.get_no("img_") + '.' + name_suffix
        FileConfig.write(name, image.context)
        course_model.picture = name
    await course_model.save()

    return course_model

async def update(course_model: CourseModel, course: dict) -> CourseModel:
    if "name" in course:
        if course_model.name != course["name"]:
            FolderConfig.open_path(f"/{course_model.phone}")
            FolderConfig.rename(course_model.name, course["name"])
            course_model.name = course["name"]
    if "type_no" in course:
        if not course["type_no"]:
            course_model.type_no = None
        else:
            course_model.type_no = course["type_no"]
    if "description" in course:
        course_model.description = course["description"]

    if "click_count" in course:
        course_model.click_count = course["click_count"]

    if "picture" in course and course["picture"] and type(course["picture"]) != str:
        name = update_picture(course_model, course["picture"])
        course_model.picture = name

    course_model.update_time = datetime.now()

    await course_model.save()
    return course_model

def update_picture(course: CourseModel, picture: UploadFile):
    phone = course.phone
    course_name = course.name
    FolderConfig.open_path(f"/{phone}/{course_name}")

    if course.picture:
        FileConfig.delete(course.picture)

    name_suffix = picture.filename.split(".")[-1]
    name = util.get_no("img_") + '.' + name_suffix
    FileConfig.write(name, picture.file.read())

    return name

async def delete(phone: str, course: CourseModel) -> int:
    await course.delete()
    FolderConfig.open_path(f"/{phone}")
    FolderConfig.delete(course.name)
    return 1

async def delete_all(phone: str) -> int:
    return await CourseModel.filter(phone=phone).delete()

# -----------------------------------------------------------------------------------
# 笔记类型删除时，相关的笔记都要删除该类型
async def del_type(phone: str, type_no: str):
    await CourseModel.filter(phone=phone, type_no=type_no).update(
        type_no=None
    )

# 初始化课程图标url
def init_course_picture_url(phone: str, course_list: list[CourseModel]):
    for course in course_list:
        course.picture = f'{IP_URL}/course/picture/{phone}/{course.name}/{course.picture}'