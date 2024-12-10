import os
import shutil
import random

from core.config import ROOT_PATH

class File:
    @staticmethod
    def has(folder_name: str):
        return os.path.exists(folder_name)

    @staticmethod
    def create(file_name: str, context: bytes=''):
        with open(file_name, "w") as file_obj:
            file_obj.write(context)

    @staticmethod
    def delete(file_name: str):
        if File.has(file_name):
            os.remove(file_name)
            return True
        else:
            return False

    @staticmethod
    def rename(old_name: str, new_name: str):
        if File.has(old_name) and not File.has(new_name):
            os.rename(old_name, new_name)
            return True
        else:
            return False

    @staticmethod
    def read(file_name: str) -> bytes:
        file_obj =  open(file_name, 'rb')
        content = file_obj.read()
        file_obj.close()
        return content

    @staticmethod
    def write(file_name: str, context: bytes, append: bool = False):
        if append:
            with open(file_name, "ab") as file_obj:
                file_obj.write(context)
        else:
            with open(file_name, "wb") as file_obj:
                file_obj.write(context)

    @staticmethod
    def all_file() -> list[str]:
        # 推导式
        return [
            file_name
            for file_name in os.listdir()
            if not os.path.isdir(file_name)
        ]

class Folder:
    @staticmethod
    def open_path(path: str, root_path: str = ""):
        if not root_path:
            root_path = ROOT_PATH
        # 打开指定目录
        if path == '/':
            path = ''
        os.chdir(root_path + path)
        return True

    @staticmethod
    def has(folder_name: str):
        return os.path.exists(folder_name)

    @staticmethod
    def create(folder_name: str):
        # 判断文件夹不存在
        if not Folder.has(folder_name):
            # 创建新文件夹
            os.makedirs(folder_name)
            print(f"add {folder_name}：成功，文件夹 已创建！")
            return True
        else:
            print(f"add {folder_name}：失败，文件夹 不存在！")
            return False

    @staticmethod
    def delete(folder_name: str):
        # 判断文件夹存在
        if Folder.has(folder_name):
            # 删除文件夹
            shutil.rmtree(folder_name)
            print(f"del {folder_name}：成功，文件夹 已删除！")
            return True
        else:
            print(f"del {folder_name}：失败，文件夹 不存在！")
            return False

    @staticmethod
    def rename(old_name: str, new_name: str):
        # 判断改名的文件夹存在
        if Folder.has(old_name):
            # 判断不存在新名称的文件夹
            # window 下大小写不敏感，判断存在会始终存在不执行
            # if not Folder.has(new_name):
            os.rename(old_name, new_name)
            print(f"rename {old_name} --> {new_name}: 成功，文件夹 已重命名！")
            return True
            # else:
            #     print(f"rename {old_name} --> {new_name}: 失败，{new_name} 文件夹 已存在！")
        else:
            print(f"rename {old_name} --> {new_name}: 失败，{old_name} 文件夹 不存在！")
        return False

    @staticmethod
    def move(old_path: str, new_path: str, old_name: str, new_name: str, root_path: str = ""):
        if not root_path:
            root_path = ROOT_PATH
        if Folder.has(f"{root_path}{old_path}/{old_name}"):
            # 判断不存在新名称的文件夹
            if not Folder.has(f"{root_path}{new_path}/{new_name}"):
                shutil.move(f"{root_path}{old_path}/{old_name}", f"{root_path}{new_path}/{new_name}")
                print(f"rename {old_name} --> {new_path}: 成功，文件夹 已重命名！")
                return True
            else:
                print(f"rename {old_name} --> {new_name}: 失败，{new_name} 文件夹 已存在！")
        else:
            print(f"rename {old_name} --> {new_name}: 失败，{old_name} 文件夹 不存在！")
        return False

    @staticmethod
    def all() -> list[str]:
        # 推导式
        return [
            file_name
            for file_name in os.listdir()
        ]

    @staticmethod
    def all_folder() -> list[str]:
        # 推导式
        return [
            file_name
            for file_name in os.listdir()
            if os.path.isdir(file_name)
        ]


class Picture:
    name: str
    context: bytes
    def __init__(self, name: str, context: bytes):
        self.name = name
        self.context = context

def get_picture() -> Picture:
    Folder.open_path("/img/touxiang")

    file_list = File.all_file()
    file_name: str = random.choice(file_list)
    context = File.read(file_name)

    return Picture(
        name= file_name,
        context= context
    )

def get_course_img() -> Picture:
    Folder.open_path("/img/course")

    file_list = File.all_file()
    file_name = random.choice(file_list)
    context = File.read(file_name)

    return Picture(
        name=file_name,
        context=context
    )


if __name__ == '__main__':

    curr_path = "\\img\\course"
    Folder.open_path(curr_path)
    li = File.all_file()
    with open(li[0], "rb") as f:
        print(f.read())

    current_path = os.getcwd()
    print(current_path)
