from fastapi import UploadFile
from datetime import datetime

from models.course import Course as CourseModel
from models.course import Unit as UnitModel

from utils import util
from utils.file import Folder as FolderConfig, File as FileConfig
from picture.picture import get_course_img

# -----------------------------------------------------------------------------查
async def get_phone(phone: str) -> list[CourseModel]:
    return await CourseModel.filter(phone=phone)

async def has(phone: str) -> bool:
    return await CourseModel.exists(phone=phone)

async def has_course(phone: str, course_no: str) -> bool:
    return await CourseModel.exists(phone=phone, course_no=course_no)

async def has_same_name(phone: str, name: str) -> bool:
    return await CourseModel.exists(phone=phone, name=name)

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
        course.picture = f'/course/picture/{phone}/{course.name}/{course.picture}'


def init_import_course_picture():
    file_list = FileConfig.all_file()
    picture_list = [item for item in file_list if item.split('.')[-1] != "md"]
    if picture_list:
        return picture_list[0]
    else:
        raise Exception("缺少课程图标")

def init_import_course_unit(path: str, phone: str, course: CourseModel, parent_no: str | None = None, parent_name: str = "") -> list[UnitModel]:
    FolderConfig.open_path(path)
    folder_list = [item for item in FolderConfig.all_folder() if item.split('.')[0] != "picture"]
    file_list = [item for item in FileConfig.all_file() if item.split('.')[-1] == "md"]

    # 1.1 格式校验，是否存在 00.index.md
    if parent_no:
        if "00.index.md" in file_list:
            file_list.remove("00.index.md")
        else:
            raise Exception(f"格式错误，{parent_name} 文件夹下 缺少00.index.md文件")

    unit_list: list[UnitModel] = []
    # 2.1 md文件组装，model
    for item in file_list:
        no = int(item.split('.')[0])
        name = '.'.join(item.split('.')[0:-1])
        unit_no = util.get_no("U_")
        now = datetime.now()
        unit_list.append(UnitModel(
            phone=phone,
            course_no=course.course_no,
            unit_no=unit_no,
            name=name,
            is_menu=False,
            parent_no=parent_no,
            create_time=now,
            update_time=now,
        ))

    # 2.2 md文件夹组装，model
    for item in folder_list:
        if item.split('.')[0] != "piction":
            no = int(item.split('.')[0])
            name = item
            now = datetime.now()
            unit_no = util.get_no("U_")
            unit_list.append(UnitModel(
                phone=phone,
                course_no=course.course_no,
                unit_no=unit_no,
                name=name,
                is_menu=True,
                parent_no=parent_no,
                create_time=now,
                update_time=now,
            ))

    # 2.3 根据name排序
    unit_list.sort(key=lambda item: item.name, reverse=False)

    # 3.1 校验前后name序号，并补充前后链接
    i = 0
    while i < len(unit_list):
        if int(unit_list[i].name.split('.')[0]) != i + 1:
            raise Exception(f"格式有误，{parent_name} 文件夹下 序号排不下来")
        if i != 0:
            unit_list[i - 1].next_no = unit_list[i].unit_no
        i += 1

    # 3.2 是目录的结构，深度调用，并合并
    for item in unit_list:
        if item.is_menu:
            unit_list = unit_list + init_import_course_unit(f"{path}/{item.name}", phone, course, item.unit_no, item.name)

    return unit_list


def init_import_course(phone: str, course_name: str, type_no: str | None = None) -> [CourseModel, list[UnitModel]]:
    FolderConfig.open_path(f'/{phone}/{course_name}')
    now = datetime.now()
    course = CourseModel(
        phone=phone,
        course_no=util.get_no("C_"),
        name=course_name,
        picture=init_import_course_picture(),
        type_no=type_no,
        description="",
        create_time=now,
        update_time=now,
    )
    unit_list = init_import_course_unit(f'/{phone}/{course_name}', phone, course, parent_name="根目录")

    return course, unit_list