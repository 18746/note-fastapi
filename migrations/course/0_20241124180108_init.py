from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `course` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `course_no` VARCHAR(20) NOT NULL  COMMENT '课程序号',
    `name` VARCHAR(30) NOT NULL  COMMENT '课程名',
    `path` VARCHAR(30) NOT NULL  COMMENT '课程所在路径',
    `phone` VARCHAR(11) NOT NULL  COMMENT '电话',
    `type_no` VARCHAR(20) NOT NULL  COMMENT '类型唯一值',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `type` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `type_no` VARCHAR(20) NOT NULL  COMMENT '类型唯一值',
    `name` VARCHAR(30) NOT NULL  COMMENT '类型名',
    `phone` VARCHAR(11) NOT NULL  COMMENT '电话',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `unit` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `unit_no` VARCHAR(20) NOT NULL  COMMENT '单元序号',
    `name` VARCHAR(60) NOT NULL  COMMENT '文件名',
    `file_path` VARCHAR(20) NOT NULL  COMMENT '文件路径',
    `parent_no` VARCHAR(20) NOT NULL  COMMENT '父节点 单元序号',
    `prev_no` VARCHAR(20) NOT NULL  COMMENT '前一个 单元序号',
    `next_no` VARCHAR(20) NOT NULL  COMMENT '后一个 单元序号',
    `is_menu` BOOL NOT NULL  COMMENT '是否为菜单' DEFAULT 0,
    `course_no` VARCHAR(20) NOT NULL  COMMENT '课程序号',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
