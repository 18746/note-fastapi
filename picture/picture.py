import os
import random

from utils.file import Folder as FolderConfig, File as FileConfig
from core.application import PROJECT_PATH


class Picture:
    name: str
    context: bytes
    def __init__(self, name: str, context: bytes):
        self.name = name
        self.context = context


def get_background_img() -> Picture:
    os.chdir(f'{PROJECT_PATH}/picture/background')

    file_list = FileConfig.all_file()
    file_name = random.choice(file_list)
    context = FileConfig.read(file_name)

    return Picture(
        name=file_name,
        context=context
    )


def get_user_img() -> Picture:
    os.chdir(f'{PROJECT_PATH}/picture/user')

    file_list = FileConfig.all_file()
    file_name = random.choice(file_list)
    context = FileConfig.read(file_name)

    return Picture(
        name=file_name,
        context=context
    )


def get_course_img() -> Picture:
    os.chdir(f'{PROJECT_PATH}/picture/course')

    file_list = FileConfig.all_file()
    file_name = random.choice(file_list)
    context = FileConfig.read(file_name)

    return Picture(
        name=file_name,
        context=context
    )