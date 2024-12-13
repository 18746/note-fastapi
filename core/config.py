import os

# 根目录
ROOT_PATH = "Z:/99.笔记"
PROJECT_PATH = os.getcwd()

# 数据库配置
TORTOISE_ORM = {
    "connections": {             # 数据库连接
        "user": {                                 # 1、连接名、及配置
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",      # 数据库地址
                "port": "3306",           # 数据库端口
                "user": "root",           # 数据库用户名
                "password": "123456",     # 数据库密码
                "database": "user",       # 数据库名称
                "minsize": 1,             # 连接池最小连接数
                "maxsize": 5,             # 连接池大小
                "charset": "utf8mb4",     # 字符集
                "echo": True              # 是否打印SQL语句
            },
        },
        "course": {                                 # 1、连接名、及配置
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "localhost",      # 数据库地址
                "port": "3306",           # 数据库端口
                "user": "root",           # 数据库用户名
                "password": "123456",     # 数据库密码
                "database": "course",     # 数据库名称
                "minsize": 1,             # 连接池最小连接数
                "maxsize": 5,             # 连接池大小
                "charset": "utf8mb4",     # 字符集
                "echo": True              # 是否打印SQL语句
            },
        },
    },
    "apps": {
        "user": {                                 # 2、模型列表名称 (模型指定外键时 用该名称下的模型)
            "default_connection": "user",         # 3、默认连接，指定【连接名】
            "models": [                           # 4、指定模型路径
                "models.user",
                "aerich.models"  # aerich.models是自动生成迁移文件
            ],
        },
        "course": {                               # 2、模型列表名称 (模型指定外键时 用该名称下的模型)
            "default_connection": "course",       # 3、默认连接，指定【连接名】
            "models": [                           # 4、指定模型路径
                "models.course",
                # "aerich.models"  # aerich.models是自动生成迁移文件
            ],
        },
    },
    # "use_tz": True,              # 是否使用时区
    "use_tz": False,

    "timezone": "Asia/Shanghai",   # 时区
    # "timezone": "UTC"
}
