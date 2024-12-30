import os
import shutil
import zipfile

from core.application import ROOT_PATH

class File:
    @staticmethod
    def has(folder_name: str):
        return os.path.exists(folder_name)

    @staticmethod
    def create(file_name: str, context: bytes | str = b'', b_flag: bool = True):
        mode = "w"
        if b_flag:
            mode += "b"
        with open(file_name, mode) as file_obj:
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
    def read(file_name: str, b_flag: bool = True) -> str | bytes:
        mode = "r"
        if b_flag:
            mode += "b"
        file_obj =  open(file_name, mode)
        content = file_obj.read()
        file_obj.close()
        return content

    @staticmethod
    def write(file_name: str, context: bytes | str, append: bool = False, b_flag: bool = True):
        if append:
            mode = "a"
            if b_flag:
                mode += "b"
            with open(file_name, mode) as file_obj:
                file_obj.write(context)
        else:
            mode = "w"
            if b_flag:
                mode += "b"
            with open(file_name, mode) as file_obj:
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
                print(f"move {old_name} --> {new_name}: 成功，文件夹 已移动！")
                return True
            else:
                print(f"move {old_name} --> {new_name}: 失败，{new_name} 文件夹 已存在！")
        else:
            print(f"move {old_name} --> {new_name}: 失败，{old_name} 文件夹 不存在！")
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

    @staticmethod
    def zip(folder_name: str, zip_name: str = ""):
        zip_file_new = f"{zip_name}"

        filelist = []
        for root, dirs, files in os.walk(folder_name, topdown=False):
            if not files and not dirs:
                filelist.append(root)
            for name in files:
                filelist.append(os.path.join(root, name))

        zf = zipfile.ZipFile(zip_file_new, "w", zipfile.ZIP_DEFLATED)
        for tar in filelist:
            arcname = tar[len(folder_name):]
            zf.write(tar, arcname)
        zf.close()

        return zip_file_new

    @staticmethod
    def un_zip(file_name: str):
        """unzip zip file"""
        folder_name = ''.join(file_name.split('.')[0:-1])

        os.mkdir(folder_name)

        zip_file = zipfile.ZipFile(file_name)
        for names in zip_file.namelist():
            zip_file.extract(names, folder_name)
        zip_file.close()
        return folder_name



if __name__ == '__main__':

    # curr_path = "\\img\\course"
    # Folder.open_path(curr_path)
    # li = File.all_file()
    # with open(li[0], "rb") as f:
    #     print(f.read())
    #
    # current_path = os.getcwd()
    # print(current_path)

    # month_rank_dir = "test_dir"
    #
    # Folder.zip(month_rank_dir)

    Folder.un_zip("git.zip")


