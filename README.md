# 一、起步

## 1. 安装依赖

### 1.1 fastapi

```cmd
pip install fastapi
pip install uvicorn==0.20.0
```

### 1.2 tortoise-orm

```cmd
pip install tortoise-orm      # ORM系统
pip install aiomysql          # 数据库驱动

pip install python-multipart  # 上传文件
```

### 1.3 aerich

```cmd
pip install aerich            # 安装数据库迁移

aerich init -t configs.TORTOISE_ORM     # 生成迁移文件，只需要执行一次
aerich init-db                          # 初始化数据库（生成各种表）

# 当数据库模型变更后，执行，更新数据库
aerich migrate [--name "更新信息"]       # 执行迁移文件，生成更新表结构的文件
aerich upgrade                          # 根据迁移文件，升级数据库
aerich downgrade                        # 根据迁移文件，降级数据库

aerich history                          # 查看迁移文件历史
```

## 2. 生成依赖配置文件

```cmd
# 有新的依赖安装时，可以更新依赖文件
pip freeze > requirements.txt    # 生成依赖配置文件

pip install -r requirements.txt  # 安装依赖
```

## 3. 项目启动
```txt
http://127.0.0.1:8080/docs#/    接口文档
```





