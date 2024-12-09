from fastapi import APIRouter, Header, UploadFile, Body, Form
from typing import Annotated
from utils.exception import ErrorMessage
from utils.file import Folder as FolderConfig, File as FileConfig


from schemas.course import type   as TypeSchemas
from crud.course    import type   as TypeCrud
from schemas.course import course as CourseSchemas
from crud.course    import course as CourseCrud
from schemas.course import unit   as UnitSchemas
from crud.course    import unit   as UnitCrud

# ----------------------------------------------------------------------------------------type
type_router = APIRouter(
    prefix="/type",
    tags=["笔记"],
    deprecated=False
)


@type_router.post(
    "",
    summary="创建课程类型",
    description="返回创建的课程类型",
    response_model=TypeSchemas.CourseOut
)
async def create(phone: Annotated[str, Header()], type_in: TypeSchemas.TypeCreateIn):
    if not type_in.name:
        raise ErrorMessage(
            status_code=500,
            message="类型名不能为空"
        )
    if await TypeCrud.has_name(phone, type_in.name):
        raise ErrorMessage(
            status_code=500,
            message="已存在同名类型"
        )
    return await TypeCrud.create(phone, type_in.model_dump(exclude_unset=True))

@type_router.put(
    "/{type_no}",
    summary="更新课程类型",
    description="返回更新后的课程了类型",
    response_model=TypeSchemas.CourseOut
)
async def update(phone: Annotated[str, Header()], type_no: str, type_in: TypeSchemas.TypeCreateIn):
    if await TypeCrud.has_type(phone, type_no):
        type_model = await TypeCrud.get_type(phone, type_no)

        return await TypeCrud.update(type_model, type_in.model_dump(exclude_unset=True))
    raise ErrorMessage(
        status_code=500,
        message="类型不存在，不能更新"
    )

@type_router.delete(
    "/{type_no}",
    summary="删除课程类型",
    description="返回删除课程类型数目",
)
async def delete(phone: Annotated[str, Header()], type_no: str):
    if await TypeCrud.has_type(phone, type_no):
        await CourseCrud.del_type(phone, type_no)
        return await TypeCrud.delete(phone, type_no)
    raise ErrorMessage(
        status_code=200,
        message="类型不存在，不能删除"
    )

# ------------------------------------------------------------------------------------------课程
course_router = APIRouter(
    prefix="/course",
    tags=["笔记"],
    deprecated=False
)


@course_router.post(
    "",
    summary="创建新的课程笔记",
    description="返回创建的课程笔记",
    response_model=CourseSchemas.CourseOut
)
async def create(phone: Annotated[str, Header()], course: Annotated[CourseSchemas.CourseCreateIn, Form()]):
    if not course.name:
        raise ErrorMessage(
            status_code=500,
            message="课程名不能为空，请检查"
        )
    # 检查该用户名下是否有同名 课程
    if await CourseCrud.has_name(phone, course.name):
        raise ErrorMessage(
            status_code=500,
            message="已存在同名课程，不能创建"
        )
    # 若有类型，检查该用户创建的类型 数据库中是否存在
    if course.type_no and not await TypeCrud.has_type(phone, course.type_no):
        raise ErrorMessage(
            status_code=500,
            message="课程类型不存在，请检查"
        )
    return await CourseCrud.create(phone, course.model_dump(exclude_unset=True))

@course_router.put(
    "/{course_no}",
    summary="更新课程笔记",
    description="返回更新后的课程笔记",
    response_model=CourseSchemas.CourseOut
)
async def update(phone: Annotated[str, Header()], course_no: str, course: Annotated[CourseSchemas.CourseCreateIn, Form()]):
    if await CourseCrud.has_course(phone, course_no):
        if not course.name:
            print(course.name)
            raise ErrorMessage(
                status_code=500,
                message="课程名不能为空，请检查"
            )
        # 检查该用户名下是否有同名 课程
        if await CourseCrud.has_name(phone, course.name, course_no):
            raise ErrorMessage(
                status_code=500,
                message="已存在同名课程，不能更改"
            )
        # 若有类型，检查该用户创建的类型 数据库中是否存在
        if course.type_no and not await TypeCrud.has_type(phone, course.type_no):
            raise ErrorMessage(
                status_code=500,
                message="课程类型不存在，请检查"
            )

        course_model = await CourseCrud.get_course(phone, course_no)

        return await CourseCrud.update(course_model, course.model_dump(exclude_unset=True))
    raise ErrorMessage(
        status_code=500,
        message="课程不存在，不能更新"
    )

# 更改课程图标
@course_router.put(
    "/picture/{course_no}",
    summary="更改课程图标",
    description="返回更新成功/失败 bool",
)
async def update_picture(phone: Annotated[str, Header()], course_no: str, picture: UploadFile):
    course_model = await CourseCrud.get_course(phone, course_no)
    return CourseCrud.update_picture(course_model, picture)

@course_router.delete(
    "/{course_no}",
    summary="删除课程笔记",
    description="返回删除的数量",
)
async def delete(phone: Annotated[str, Header()], course_no: str):
    if await CourseCrud.has_course(phone, course_no):
        course_model = await CourseCrud.get_course(phone, course_no)
        # 先删除课程下的所有章节
        await UnitCrud.delete_course(phone, course_no)
        return await CourseCrud.delete(phone, course_model)
    raise ErrorMessage(
        status_code=200,
        message="课程不存在，不能删除"
    )

# -----------------------------------------------------------------------------------------章节
unit_router = APIRouter(
    prefix="/unit",
    tags=["笔记"],
    deprecated=False
)

# 新增章节
@unit_router.post(
    "/{course_no}",
    summary="新增章节",
    description="返回新增的课程章节",
    response_model=UnitSchemas.UnitOut
)
async def create(phone: Annotated[str, Header()], course_no: str, unit: UnitSchemas.UnitCreateIn):
    # 存在课程的情况下
    if await CourseCrud.has_course(phone, course_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
        parent_child = UnitCrud.unit_sort([item for item in all_unit if item.parent_no == unit.parent_no])

        # 1.1 格式校验
        UnitCrud.create_format(all_unit, unit.model_dump())

        # 2.1 补充name 序号
        next_unit = [item for item in parent_child if item.unit_no == unit.next_no]
        if next_unit:
            no_name = UnitCrud.name_split(next_unit[0].name)
            unit.name = UnitCrud.num_name_connect(no_name[0], unit.name)
        else:
            unit.name = UnitCrud.num_name_connect(len(parent_child) + 1, unit.name)
            pass

        # 3.1 创建章节
        path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
        unit_model = await UnitCrud.create(phone, course_no, unit.model_dump(exclude_unset=True), path)
        all_unit.append(unit_model)

        # 3.2 新增的章节插入到列表中
        parent_child.insert(UnitCrud.name_split(unit_model.name)[0] - 1, unit_model)

        # 3.3 更新前面章节的下一个节点数据
        prev_unit = [item for item in parent_child if item.next_no == unit_model.next_no and item.unit_no != unit_model.unit_no]
        if prev_unit:
            await UnitCrud.update(prev_unit[0], {"next_no": unit_model.unit_no})

        # 3.4 更新列表name序号
        await UnitCrud.update_later_name(parent_child, path=path)

        return unit_model
    raise ErrorMessage(
        status_code=500,
        message="该课程不存在，不能增加单元"
    )

# 更新章节信息
@unit_router.put(
    "/{course_no}/{unit_no}",
    summary="更新章节信息",
    description="返回更新后的章节",
    response_model=UnitSchemas.UnitOut
)
async def update(phone: Annotated[str, Header()], course_no: str, unit_no: str, unit: UnitSchemas.UpdateUnitIn):
    # 存在单元
    if await UnitCrud.has_unit(phone, course_no, unit_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
        old_unit = [item for item in all_unit if item.unit_no == unit_no][0]

        # 0.0 过滤掉要更新的节点，初始化要更新的数据
        all_unit = [item for item in all_unit if item.unit_no != old_unit.unit_no]
        unit = UnitCrud.update_init(old_unit, unit.model_dump(exclude_unset=True))

        # 0.1 更改老节点前后的连接
        old_parent_child = [item for item in all_unit if item.parent_no == old_unit.parent_no]
        old_prev_unit = [item for item in old_parent_child if item.next_no == old_unit.unit_no]
        if old_prev_unit:
            old_prev_unit[0].next_no = old_unit.next_no

        # 0.2 重新排序
        old_parent_child = UnitCrud.unit_sort(old_parent_child)
        parent_child = UnitCrud.unit_sort([item for item in all_unit if item.parent_no == unit.parent_no])

        # 1.1 格式校验
        UnitCrud.create_format(all_unit, unit.model_dump(exclude_unset=True))

        # 2.1 老节点，前后连接更新
        if old_prev_unit:
            await old_prev_unit[0].save()

        # 2.2 老节点name更新
        new_path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
        old_path = new_path
        if old_unit.parent_no != unit.parent_no:
            old_path = UnitCrud.get_deep_path(curr_course, all_unit, old_unit.parent_no, True)
            await UnitCrud.update_later_name(old_parent_child, old_path)

        # 3.1 补充name 序号
        next_unit = [item for item in parent_child if item.unit_no == unit.next_no]
        if next_unit:
            no_name = UnitCrud.name_split(next_unit[0].name)
            unit.name = UnitCrud.num_name_connect(no_name[0] - 1, unit.name)
        else:
            unit.name = UnitCrud.num_name_connect(len(parent_child) + 1, unit.name)
            pass

        # 3.2 从目录变为md的，要删除目录的子节点
        if not unit.is_menu and old_unit.is_menu:
            li = [item for item in all_unit if item.parent_no == unit_no]
            for it in li:
                await UnitCrud.delete_deep_unit(all_unit, it.unit_no)

        # 4.1 更新章节数据
        unit_model = await UnitCrud.update(old_unit, unit.model_dump(exclude_unset=True), old_path=old_path, new_path=new_path)
        all_unit.append(unit_model)

        # 4.2 更新列表前后节点的连接
        prev_unit = [item for item in parent_child if item.next_no == unit_model.next_no]
        if prev_unit:
            await UnitCrud.update(prev_unit[0], {"next_no": unit_model.unit_no})

        # 4.3 章节插入到新位置列表中，更新列表name序号
        parent_child.insert(UnitCrud.name_split(unit_model.name)[0] - 1, unit_model)
        await UnitCrud.update_later_name(parent_child, new_path)

        return unit_model
    raise ErrorMessage(
        status_code=500,
        message="该课程不存在，不能修改"
    )

# 删除章节
@unit_router.delete(
    "/{course_no}/{unit_no}",
    summary="删除章节，子目录也删除",
    description="返回删除的章节数",
)
async def delete_unit(phone: Annotated[str, Header()], course_no: str, unit_no: str):
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
        parent_child = UnitCrud.unit_sort(parent_child)
        path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
        await UnitCrud.update_later_name(parent_child, path)

        # 2.2 深度删除子节点
        all_unit.append(unit)
        FolderConfig.open_path(path)
        if unit.is_menu:
            FolderConfig.delete(unit.name)
        else:
            FileConfig.delete(unit.name + ".md")
        return await UnitCrud.delete_deep_unit(all_unit, unit.unit_no)

# 章节更新内容
@unit_router.put(
    "/context/{course_no}/{unit_no}",
    summary="更新章节内容",
    description="返回 true",
)
async def update_context(phone: Annotated[str, Header()], course_no: str, unit_no: str, text: Annotated[str, Body()]):
    if await UnitCrud.has_unit(phone=phone, course_no=course_no, unit_no=unit_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
        curr_unit = [item for item in all_unit if item.unit_no == unit_no][0]

        path = UnitCrud.get_deep_path(curr_course, all_unit, course_no)
        if curr_unit.is_menu:
            FolderConfig.open_path(f"/{path}/{curr_unit.name}")
            FileConfig.write("00.index.md", text.encode("utf-8"))
        else:
            FolderConfig.open_path(f"/{path}")
            FileConfig.write(f"{curr_unit.name}.md", text.encode("utf-8"))

        return True
    raise ErrorMessage(
        status_code=500,
        message="课程单元不存在，查询不到"
    )

# ------------------------------------------------------------------------------------------笔记

note_router = APIRouter(
    prefix="/note",
    tags=["笔记"],
    deprecated=False
)

note_router.include_router(type_router)
note_router.include_router(course_router)
note_router.include_router(unit_router)
