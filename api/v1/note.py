from fastapi import APIRouter, Header, UploadFile, Body, Form, BackgroundTasks
from fastapi.responses import FileResponse, Response
from typing import Annotated
from datetime import datetime
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
    "/{phone}",
    summary="创建课程类型",
    description="返回创建的课程类型",
    response_model=TypeSchemas.CourseOut
)
async def create(phone: str, type_in: TypeSchemas.TypeCreateIn):
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
    "/{phone}/{type_no}",
    summary="更新课程类型",
    description="返回更新后的课程了类型",
    response_model=TypeSchemas.CourseOut
)
async def update(phone: str, type_no: str, type_in: TypeSchemas.TypeCreateIn):
    if await TypeCrud.has_type(phone, type_no):
        type_model = await TypeCrud.get_type(phone, type_no)

        return await TypeCrud.update(type_model, type_in.model_dump(exclude_unset=True))
    raise ErrorMessage(
        status_code=500,
        message="类型不存在，不能更新"
    )

@type_router.delete(
    "/{phone}/{type_no}",
    summary="删除课程类型",
    description="返回删除课程类型数目",
)
async def delete(phone: str, type_no: str):
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
    "/{phone}",
    summary="创建新的课程笔记",
    description="返回创建的课程笔记",
    response_model=CourseSchemas.CourseOut
)
async def create(phone: str, course: Annotated[CourseSchemas.CourseCreateIn, Form()]):
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
    course = await CourseCrud.create(phone, course.model_dump(exclude_unset=True))
    CourseCrud.init_course_picture_url(phone, [course, ])
    return course

@course_router.put(
    "/{phone}/{course_no}",
    summary="更新课程笔记",
    description="返回更新后的课程笔记",
    response_model=CourseSchemas.CourseOut
)
async def update(phone: str, course_no: str, course: Annotated[CourseSchemas.CourseCreateIn, Form()]):
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

        course = await CourseCrud.update(course_model, course.model_dump(exclude_unset=True))
        CourseCrud.init_course_picture_url(phone, [course, ])
        return course
    raise ErrorMessage(
        status_code=500,
        message="课程不存在，不能更新"
    )

# 更改课程图标
@course_router.put(
    "/{phone}/{course_no}/picture",
    summary="更改课程图标",
    description="返回更新成功/失败 bool",
)
async def update_picture(phone: str, course_no: str, picture: UploadFile):
    course_model = await CourseCrud.get_course(phone, course_no)
    return CourseCrud.update_picture(course_model, picture)

@course_router.delete(
    "/{phone}/{course_no}",
    summary="删除课程笔记",
    description="返回删除的数量",
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

def deleteZip(phone: str, course_name_zip: str):
    FolderConfig.open_path(f'/{phone}')
    FileConfig.delete(course_name_zip)

@course_router.get(
    "/export/{phone}/{course_no}",
    summary="导出课程笔记",
    description="返回导出的压缩包",
)
async def export(phone: str, course_no: str, background_tasks: BackgroundTasks):
    if await CourseCrud.has_course(phone, course_no):
        course_model = await CourseCrud.get_course(phone, course_no)
        FolderConfig.open_path(f'/{phone}')
        export_name = FolderConfig.zip(f'{course_model.name}', "export")
        background_tasks.add_task(deleteZip, phone, export_name)

        FolderConfig.open_path(f'/{phone}')
        return FileResponse(f'{course_model.name}.zip', filename=export_name)
    raise ErrorMessage(
        status_code=500,
        message="课程不存在，不能导出"
    )

@course_router.post(
    "/import/{phone}",
    summary="导入课程笔记",
    description="返回导入的课程",
    response_model=CourseSchemas.CourseOut
)
async def import_course(phone: str, file: UploadFile, type_no: Annotated[str | None, Body()], background_tasks: BackgroundTasks):
    filename = file.filename
    if not await CourseCrud.has_same_name(phone, ".".join(filename.split('.')[0:-1])):
        FolderConfig.open_path(f'/{phone}')
        FileConfig.write(filename, file.file.read())
        folder_name = FolderConfig.un_zip(filename)
        FileConfig.delete(filename)

        try:
            if not type_no:
                type_no = None
            course_and_unit = CourseCrud.init_import_course(phone, folder_name, type_no)
            course = course_and_unit[0]
            unit_list = course_and_unit[1]
            for item in unit_list:
                await item.save()
            await course.save()

            CourseCrud.init_course_picture_url(phone, [course, ])
            return course
        except Exception as e:
            FolderConfig.open_path(f'/{phone}')
            FolderConfig.delete(folder_name)
            raise ErrorMessage(
                status_code=500,
                message=str(e)
            )
    raise ErrorMessage(
        status_code=500,
        message="已存在同名课程，不能导入"
    )

# -----------------------------------------------------------------------------------------章节
unit_router = APIRouter(
    prefix="/unit",
    tags=["笔记"],
    deprecated=False
)

# 新增章节
@unit_router.post(
    "/{phone}/{course_no}",
    summary="新增章节",
    description="返回新增的课程章节",
    response_model=UnitSchemas.UnitOut
)
async def create(phone: str, course_no: str, unit: UnitSchemas.UnitCreateIn):
    # 存在课程的情况下
    if await CourseCrud.has_course(phone, course_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)

        # 1.1 格式校验
        # 校验父节点
        _format = UnitCrud.insert_parent_no_format(all_unit, unit.parent_no)
        if not _format.state:
            raise ErrorMessage(
                status_code=500,
                message=_format.message
            )
        # 校验下一节点
        _format = UnitCrud.insert_next_no_format(all_unit, unit.parent_no, unit.next_no)
        if not _format.state:
            raise ErrorMessage(
                status_code=500,
                message=_format.message
            )
        # 校验name
        _format = UnitCrud.insert_name_format(all_unit, unit.parent_no, unit.name)
        if not _format.state:
            raise ErrorMessage(
                status_code=500,
                message=_format.message
            )

        # 2.1 补充name 序号
        unit.name = UnitCrud.init_name_no(all_unit, unit.model_dump())

        # 2.2 创建章节-创建文件
        path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
        unit_model = await UnitCrud.create(phone, course_no, unit.model_dump(exclude_unset=True), path)
        UnitCrud.create_name(unit_model, path)
        # 2.2.1 插入列表
        all_unit.append(unit_model)

        # 2.3 更新前面章节的下一个节点数据
        await UnitCrud.refresh_link_add(all_unit, unit_model)

        # 2.4 更新列表name序号
        path = UnitCrud.get_deep_path(curr_course, all_unit, unit_model.parent_no, True)
        await UnitCrud.refresh_list_name(all_unit, unit_model.parent_no, path)

        return unit_model
    raise ErrorMessage(
        status_code=500,
        message="该课程不存在，不能增加单元"
    )

# 更新章节信息
@unit_router.put(
    "/{phone}/{course_no}/{unit_no}",
    summary="更新章节信息",
    description="返回更新后的章节",
    response_model=UnitSchemas.UnitOut
)
async def update(phone: str, course_no: str, unit_no: str, unit: UnitSchemas.UpdateUnitIn):
    # 存在单元
    if await UnitCrud.has_unit(phone, course_no, unit_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
        # 0.0 初始化更新的数据
        old_unit = [item for item in all_unit if item.unit_no == unit_no][0]
        unit = UnitCrud.update_init(old_unit, unit.model_dump(exclude_unset=True))

        if unit.parent_no != old_unit.parent_no:
            # 1.1 格式校验
            # 校验父节点
            _format = UnitCrud.insert_parent_no_format(all_unit, unit.parent_no)
            if not _format.state:
                raise ErrorMessage(
                    status_code=500,
                    message=_format.message
                )
            # 校验下一节点
            _format = UnitCrud.insert_next_no_format(all_unit, unit.parent_no, unit.next_no)
            if not _format.state:
                raise ErrorMessage(
                    status_code=500,
                    message=_format.message
                )
            # 校验name
            _format = UnitCrud.insert_name_format(all_unit, unit.parent_no, unit.name)
            if not _format.state:
                raise ErrorMessage(
                    status_code=500,
                    message=_format.message
                )

            # 2.1 格式校验通过，从原位置去除
            await UnitCrud.refresh_link_del(all_unit, old_unit)
            all_unit = [item for item in all_unit if item.unit_no != old_unit.unit_no]

            # 2.2 更新老链接的name序号
            old_path = UnitCrud.get_deep_path(curr_course, all_unit, old_unit.parent_no, True)
            await UnitCrud.refresh_list_name(all_unit, old_unit.parent_no, path=old_path)

            # 3.1 获取name序号
            unit.name = UnitCrud.init_name_no(all_unit, unit.model_dump())

            # 3.2 更新数据
            new_path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
            UnitCrud.update_name(old_unit, unit.model_dump(), old_path=old_path, new_path=new_path)
            unit_model = await UnitCrud.update(old_unit, unit.model_dump())
            # 3.2.1 插入列表
            all_unit.append(unit_model)

            # 3.3 更新前面章节的下一个节点数据
            await UnitCrud.refresh_link_add(all_unit, unit_model)

            # 3.4 更新新链接的name序号
            new_path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
            await UnitCrud.refresh_list_name(all_unit, unit_model.parent_no, path=new_path)

            return unit_model
        else:
            if unit.next_no != old_unit.next_no:
                # 1.0 从原位置去除
                old_prve = await UnitCrud.refresh_link_del(all_unit, old_unit, auto_save=False)
                all_unit = [item for item in all_unit if item.unit_no != old_unit.unit_no]

                # 1.1 格式校验
                # 校验父节点
                _format = UnitCrud.insert_parent_no_format(all_unit, unit.parent_no)
                if not _format.state:
                    raise ErrorMessage(
                        status_code=500,
                        message=_format.message
                    )
                # 校验下一节点
                _format = UnitCrud.insert_next_no_format(all_unit, unit.parent_no, unit.next_no)
                if not _format.state:
                    raise ErrorMessage(
                        status_code=500,
                        message=_format.message
                    )
                # 校验name
                _format = UnitCrud.insert_name_format(all_unit, unit.parent_no, unit.name)
                if not _format.state:
                    raise ErrorMessage(
                        status_code=500,
                        message=_format.message
                    )

                # 2.1 格式校验通过，从原位置去除
                if old_prve:
                    await old_prve.save()

                # 3.1 获取name序号
                unit.name = UnitCrud.init_name_no(all_unit, unit.model_dump())

                # 3.2 更新数据
                path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
                UnitCrud.update_name(old_unit, unit.model_dump(), path=path)
                unit_model = await UnitCrud.update(old_unit, unit.model_dump())
                # 3.2.1 插入列表
                all_unit.append(unit_model)

                # 3.3 更新前面章节的下一个节点数据
                await UnitCrud.refresh_link_add(all_unit, unit_model)

                # 3.4 更新新链接的name序号
                path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
                await UnitCrud.refresh_list_name(all_unit, unit_model.parent_no, path=path)

                return unit_model
            else:
                # 1.0 从原位置去除
                all_unit = [item for item in all_unit if item.unit_no != old_unit.unit_no]

                # 2.1 获取name序号
                no_name = UnitCrud.name_split(UnitCrud.init_name_no(all_unit, unit.model_dump()))
                unit.name = UnitCrud.num_name_connect(no_name[0] - 1, no_name[1])

                # 2.2 更新数据
                path = UnitCrud.get_deep_path(curr_course, all_unit, unit.parent_no, True)
                UnitCrud.update_name(old_unit, unit.model_dump(), path=path)
                unit_model = await UnitCrud.update(old_unit, unit.model_dump())
                # 2.2.1 插入列表
                all_unit.append(unit_model)

                return unit_model
    raise ErrorMessage(
        status_code=500,
        message="该课程不存在，不能修改"
    )

# 删除章节
@unit_router.delete(
    "/{phone}/{course_no}/{unit_no}",
    summary="删除章节，子目录也删除",
    description="返回删除的章节数",
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

# 章节更新内容
@unit_router.put(
    "/context/{phone}/{course_no}/{unit_no}",
    summary="更新章节内容",
    description="返回 更新后的值",
)
async def update_context(phone: str, course_no: str, unit_no: str, text: Annotated[str, Body()], background_tasks: BackgroundTasks):
    if await UnitCrud.has_unit(phone=phone, course_no=course_no, unit_no=unit_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
        curr_unit = [item for item in all_unit if item.unit_no == unit_no][0]

        path = UnitCrud.get_deep_path(curr_course, all_unit, unit_no)

        UnitCrud.set_context(path, phone, curr_course, curr_unit, text)

        if curr_unit.is_menu:
            FolderConfig.open_path(f"/{path}/{curr_unit.name}/picture.00.index")
        else:
            FolderConfig.open_path(f"/{path}/picture.{curr_unit.name}")

        # background_tasks.add_task(UnitCrud.delete_phone_time_limit, user_model)

        img_name_list = FileConfig.all_file()

        for img_name in img_name_list:
            if img_name not in text:
                FileConfig.delete(img_name)

        curr_course.update_num += 1
        curr_unit.update_time = datetime.now()
        await curr_course.save()
        await curr_unit.save()
        return text
    raise ErrorMessage(
        status_code=500,
        message="课程单元不存在，查询不到"
    )

# 章节上传图片
@unit_router.post(
    "/picture/{phone}/{course_no}/{unit_no}",
    summary="章节上传图片",
    description="返回 上传位置",
)
async def upload_picture(phone: str, course_no: str, unit_no: str, picture: UploadFile):
    if await UnitCrud.has_unit(phone=phone, course_no=course_no, unit_no=unit_no):
        curr_course = await CourseCrud.get_course(phone, course_no)
        all_unit = await UnitCrud.get_course_all_unit(phone, course_no)
        curr_unit = [item for item in all_unit if item.unit_no == unit_no][0]

        path = UnitCrud.get_deep_path(curr_course, all_unit, unit_no)

        picture_url = UnitCrud.upload_picture(path, phone, curr_course, curr_unit, picture)

        return dict(
            picture_url=picture_url,
        )
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
