from datetime import datetime

from utils.exception import ErrorMessage
from utils.util import get_no
from utils.file import Folder as FolderConfig, File as FileConfig

from models.course import Unit as UnitModel
from models.course import Course as CourseModel

from crud.course    import course as CourseCrud
from schemas.course import unit   as UnitSchemas


# 获取某个章节信息
async def get_unit(phone: str, course_no: str, unit_no: str) -> UnitModel:
    return await UnitModel.get(phone=phone, course_no=course_no, unit_no=unit_no)

# 是否存在章节
async def has(phone: str) -> bool:
    return await UnitModel.exists(phone=phone)

# 是否存在章节
async def has_unit(phone: str, course_no: str, unit_no: str) -> bool:
    return await UnitModel.exists(phone=phone, course_no=course_no, unit_no=unit_no)

# 获取某个课程的数据
async def get_course_all_unit(phone: str, course_no: str) -> list[UnitModel]:
    return await UnitModel.filter(phone=phone, course_no=course_no)
# -------------------------------------------------------------------------------------------------
# 创建章节
async def create(phone: str, course_no: str, unit: dict, path: str) -> UnitModel:
    if "unit_no" not in unit:
        unit["unit_no"] = get_no("U_")
    if "name" not in unit:
        unit["name"] = get_no("UName_")
    if "is_menu" not in unit:
        unit["is_menu"] = False
    if "parent_no" not in unit or unit["parent_no"] == "":
        unit["parent_no"] = None
    if "next_no" not in unit or unit["next_no"] == "":
        unit["next_no"] = None

    if unit["is_menu"]:
        FolderConfig.open_path(path)
        FolderConfig.create(unit["name"])
        FolderConfig.open_path(path + '/' + unit["name"])
        FileConfig.create("00.index.md")
    else:
        FolderConfig.open_path(path)
        FileConfig.create(unit["name"] + ".md")

    now = datetime.now()
    return await UnitModel.create(
        phone=phone,
        course_no=course_no,
        unit_no=unit["unit_no"],
        name=unit["name"],
        parent_no=unit["parent_no"],
        next_no=unit["next_no"],
        is_menu=unit["is_menu"],
        create_time=now,
        update_time=now,
    )

def create_format(all_unit: list[UnitModel], unit: dict):
    parent_no = unit["parent_no"]
    next_no = unit["next_no"]
    name = unit["name"]
    parent_child = unit_sort([item for item in all_unit if item.parent_no == parent_no])
    parent_unit = [item for item in all_unit if item.unit_no == parent_no]

    # 1.1 判断父章节存在，且是菜单
    if parent_no and not parent_unit:
        raise ErrorMessage(
            status_code=500,
            message="父章节不存在，请检查后重试"
        )
    elif parent_no and parent_unit and not parent_unit[0].is_menu:
        raise ErrorMessage(
            status_code=500,
            message="父章节不是目录"
        )

    # 1.2 判断后一章节存在且在当前目录管控
    next_unit = [item for item in parent_child if item.unit_no == next_no]
    if next_no and not next_unit:
        raise ErrorMessage(
            status_code=500,
            message="后一章节不在当前目录，请检查后重试"
        )

    # 1.3 管控目录名不能为空
    if not name:
        raise ErrorMessage(
            status_code=500,
            message="目录名称不能为空"
        )

    # 1.4 相同目录中，不能有同名文件
    if any(name_split(child.name)[1] == name for child in parent_child):
        raise ErrorMessage(
            status_code=500,
            message="当前目录中，已存在同名文件，请修改后重试"
        )

# 更新章节
async def update(unit_model: UnitModel, unit: dict, old_path: str = "", new_path: str = "", path: str = "") -> UnitModel:
    if path:
        old_path = path
        new_path = path
    old_name = unit_model.name
    new_name = unit_model.name
    old_is_menu = unit_model.is_menu
    new_is_menu = unit_model.is_menu
    if "name" in unit:
        unit_model.name = unit["name"]
        new_name = unit["name"]
    if "is_menu" in unit:
        unit_model.is_menu = unit["is_menu"]
        new_is_menu = unit["is_menu"]
    if "parent_no" in unit:
        unit_model.parent_no = unit["parent_no"]
    if "next_no" in unit:
        unit_model.next_no = unit["next_no"]

    if old_path and new_path:
        if new_is_menu and old_is_menu:
            if old_name != new_name:
                FolderConfig.open_path(old_path)
                FolderConfig.move(old_path, new_path, old_name, new_name)
        elif new_is_menu and not old_is_menu:
            FolderConfig.open_path(old_path)
            content = FileConfig.read(old_name + ".md")
            FileConfig.delete(old_name + ".md")
            FolderConfig.create(new_name)
            FileConfig.create(new_name + "/00.index.md", content)
        elif not new_is_menu and old_is_menu:
            FolderConfig.open_path(old_path)
            content = FileConfig.read(old_name + "/00.index.md")
            FolderConfig.delete(old_name)
            FileConfig.create(new_name + ".md", content)
        else:
            if old_name != new_name:
                FolderConfig.open_path(old_path)
                FolderConfig.move(old_path, new_path, old_name + ".md", new_name + ".md")

    unit_model.update_time = datetime.now()
    await unit_model.save()
    return unit_model

def update_init(unit_model: UnitModel, unit: dict) -> UnitSchemas.UpdateUnitIn:
    if "name" not in unit:
        unit["name"] = name_split(unit_model.name)[1]
    if "is_menu" not in unit:
        unit["is_menu"] = unit_model.is_menu
    if "parent_no" not in unit:
        unit["parent_no"] = unit_model.parent_no
    if "next_no" not in unit:
        unit["next_no"] = unit_model.next_no

    return UnitSchemas.UpdateUnitIn(**unit)

# 按列表顺序，更新name序号
async def update_later_name(parent_child: list[UnitModel], path: str):
    index = 0
    while parent_child and index < len(parent_child):
        current_unit = parent_child[index]
        no_name = name_split(current_unit.name)
        if no_name[0] != index + 1:
            await update(current_unit, {"name": num_name_connect(index + 1, name_split(current_unit.name)[1])}, path=path)
        index += 1

# 深度删除章节
async def delete_deep_unit(all_unit: list[UnitModel], unit_no: str) -> int:
    curr_unit = [item for item in all_unit if item.unit_no == unit_no][0]
    delete_num = 1
    if curr_unit.is_menu:
        current_unit_child = [item for item in all_unit if item.parent_no == curr_unit.unit_no]
        for item in current_unit_child:
            await delete_deep_unit(all_unit, item.unit_no)
            delete_num += 1

    await curr_unit.delete()
    return delete_num

# 删除课程
async def delete_course(phone: str, course_no: str) -> int:
    return await UnitModel.filter(phone=phone, course_no=course_no).delete()

# 删除课程
async def delete_all(phone: str) -> int:
    return await UnitModel.filter(phone=phone).delete()

# --------------------------------------------------------------------------------------------
# 截取序号/名称
def name_split(name: str):
    name_list = name.split('.')
    return int(name_list[0]), ".".join(name_list[1:])

# 拼接 序号 和 名称
def num_name_connect(no: int, name: str) -> str:
    return f"{str(no).rjust(2, '0')}.{name}"

# 子目录排序
def unit_sort(child: list[UnitModel]) -> list[UnitModel]:
    child_unit: list[UnitModel] = []
    if child:
        unit_item = [unit_item for unit_item in child if unit_item.next_no is None]
        while unit_item:
            child_unit.insert(0, unit_item[0])
            unit_item = [itme for itme in child if itme.next_no == child_unit[0].unit_no]
    return child_unit

# 深度生成章节目录
def unit_deep_format(all_unit: list[UnitModel], parent_no: str | None = None):
    parent_child = [item for item in all_unit if item.parent_no == parent_no]
    parent_child = [dict(item) for item in unit_sort(parent_child)]
    child_list = []
    if parent_child:
        for item in parent_child:
            item = UnitSchemas.UnitOut(**item).model_dump()
            if item["is_menu"]:
                item["child"] = unit_deep_format(all_unit, item["unit_no"])
            else:
                item["child"] = []
            child_list.append(item)
    return child_list

# 获取深度 path
def get_deep_path(course: CourseModel, all_unit: list[UnitModel], unit_no: str, include_curr: bool = False):
    path = ""
    curr_unit = [item for item in all_unit if item.unit_no == unit_no]
    if all_unit and curr_unit:
        curr_unit = curr_unit[0]
        if include_curr:
            path = f"/{curr_unit.name}{path}"
        while curr_unit.parent_no:
            curr_unit = [item for item in all_unit if item.unit_no == curr_unit.parent_no][0]
            path = f"/{curr_unit.name}{path}"

    return f"/{course.phone}/{course.name}{path}"


async def get_context(unit_model: UnitModel, path: str):
    pass

