from datetime import datetime

from utils.exception import ErrorMessage
from utils import util
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
        unit["unit_no"] = util.get_no("U_")
    if "name" not in unit:
        unit["name"] = util.get_no("UName_")
    if "is_menu" not in unit:
        unit["is_menu"] = False
    if "parent_no" not in unit or unit["parent_no"] == "":
        unit["parent_no"] = None
    if "next_no" not in unit or unit["next_no"] == "":
        unit["next_no"] = None

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

def create_name(unit_model: UnitModel, path: str):
    if unit_model.is_menu:
        FolderConfig.open_path(path)
        FolderConfig.create(unit_model.name)
        FolderConfig.open_path(path + '/' + unit_model.name)
        FileConfig.create("00.index.md")
    else:
        FolderConfig.open_path(path)
        FileConfig.create(unit_model.name + ".md")


# 更新章节
async def update(unit_model: UnitModel, unit: dict) -> UnitModel:
    if "name" in unit:
        unit_model.name = unit["name"]
    if "is_menu" in unit:
        unit_model.is_menu = unit["is_menu"]
    if "parent_no" in unit:
        unit_model.parent_no = unit["parent_no"]
    if "next_no" in unit:
        unit_model.next_no = unit["next_no"]

    unit_model.update_time = datetime.now()
    await unit_model.save()
    return unit_model

# 初始化（没传的参数，给默认值）
def update_init(unit_model: UnitModel, unit: dict) -> UnitSchemas.UpdateUnitIn:
    if "name" not in unit:
        unit["name"] = name_split(unit_model.name)[1]
    if "is_menu" not in unit:
        unit["is_menu"] = unit_model.is_menu

    if "parent_no" in unit and unit["parent_no"] == "":
        unit["parent_no"] = unit_model.parent_no
    if "next_no" in unit and unit["next_no"] == "":
        unit["next_no"] = None

    return UnitSchemas.UpdateUnitIn(**unit)

# 更新名称
def update_name(unit_model: UnitModel, unit: dict, old_path: str = "", new_path: str = "", path: str = ""):
    if path:
        old_path = path
        new_path = path
    old_name = unit_model.name
    new_name = unit_model.name
    old_is_menu = unit_model.is_menu
    new_is_menu = unit_model.is_menu
    if "name" in unit:
        new_name = unit["name"]
    if "is_menu" in unit:
        new_is_menu = unit["is_menu"]

    if old_path and new_path:
        if new_is_menu and not old_is_menu:
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
            refresh_name(unit_model, new_name, old_path, new_path)

    return unit_model


# 深度删除章节 model
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


# 校验父节点
def insert_parent_no_format(all_unit: list[UnitModel], parent_no: str | None) -> util.UnitFormat:
    parent_unit = [item for item in all_unit if item.unit_no == parent_no]
    # 父章节存在，且是菜单
    if parent_no and not parent_unit:
        return util.UnitFormat(
            state=False,
            message="父章节不存在，请检查后重试"
        )
    elif parent_no and parent_unit and not parent_unit[0].is_menu:
        return util.UnitFormat(
            state=False,
            message="父章节不是目录"
        )
    return util.UnitFormat(
        state=True,
        message="成功"
    )
# 校验下一节点
def insert_next_no_format(all_unit: list[UnitModel], parent_no: str | None, next_no: str | None) -> util.UnitFormat:
    # 后一章节存在时，必须在当前目录
    if next_no:
        next_unit = [item for item in all_unit if item.parent_no == parent_no and item.unit_no == next_no]
        if not next_unit:
            return util.UnitFormat(
                state=False,
                message="后一章节不在当前目录，请检查后重试"
            )
    return util.UnitFormat(
        state=True,
        message="成功"
    )
# 校验name
def insert_name_format(all_unit: list[UnitModel], parent_no: str | None, name: str) -> util.UnitFormat:
    # 目录名不能为空
    if not name:
        return util.UnitFormat(
            state=False,
            message="目录名称不能为空"
        )
    parent_child = [item for item in all_unit if item.parent_no == parent_no]
    # 目录中，不能有同名文件
    if any(name_split(child.name)[1] == name for child in parent_child):
        return util.UnitFormat(
            state=False,
            message="当前目录中，已存在同名文件，请修改后重试"
        )
    return util.UnitFormat(
        state=True,
        message="成功"
    )


# 初始化name序号（当前节点不在时）
def init_name_no(all_unit: list[UnitModel], unit: dict) -> str:
    parent_child = [item for item in all_unit if item.parent_no == unit["parent_no"]]
    next_unit = [item for item in parent_child if item.unit_no == unit["next_no"]]
    if next_unit:
        no_name = name_split(next_unit[0].name)
        unit["name"] = num_name_connect(no_name[0], unit["name"])
    else:
        unit["name"] = num_name_connect(len(parent_child) + 1, unit["name"])
    return unit["name"]


# 更新前面章节的下一个节点数据
async def refresh_link_add(all_unit: list[UnitModel], unit_model: UnitModel):
    parent_child = [item for item in all_unit if item.parent_no == unit_model.parent_no]

    # 更新前面章节的下一个节点数据
    prev_unit = [item for item in parent_child if item.next_no == unit_model.next_no and item.unit_no != unit_model.unit_no]
    if prev_unit:
        prev_unit[0].next_no = unit_model.unit_no
        await prev_unit[0].save()
async def refresh_link_del(all_unit: list[UnitModel], unit_model: UnitModel, auto_save: bool = True):
    parent_child = [item for item in all_unit if item.parent_no == unit_model.parent_no]

    # 更新前面章节的下一个节点数据
    prev_unit = [item for item in parent_child if item.next_no == unit_model.unit_no]
    if prev_unit:
        prev_unit[0].next_no = unit_model.next_no
        if auto_save:
            await prev_unit[0].save()
        return prev_unit[0]

# 更新列表 name 序号
async def refresh_list_name(all_unit: list[UnitModel],  parent_no: str | None, path: str):
    parent_child = unit_sort([item for item in all_unit if item.parent_no == parent_no])
    index = 0
    while parent_child and index < len(parent_child):
        current_unit = parent_child[index]
        no_name = name_split(current_unit.name)
        if no_name[0] != index + 1:
            new_name = num_name_connect(index + 1, name_split(current_unit.name)[1])
            refresh_name(current_unit, new_name, path=path)
            current_unit.name = new_name
            await current_unit.save()
        index += 1
# 更新 name 序号（不切换is_menu）
def refresh_name(unit_model: UnitModel, new_name: str, old_path: str = "", new_path: str = "", path: str = ""):
    if path:
        old_path = path
        new_path = path
    is_menu = unit_model.is_menu
    old_name = unit_model.name
    if is_menu:
        if old_name != new_name:
            FolderConfig.open_path(old_path)
            FolderConfig.move(old_path, new_path, old_name, new_name)
    else:
        if old_name != new_name:
            FolderConfig.open_path(old_path)
            FolderConfig.move(old_path, new_path, old_name + ".md", new_name + ".md")

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

