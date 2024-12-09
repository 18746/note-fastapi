from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `course` MODIFY COLUMN `name` VARCHAR(60) NOT NULL  COMMENT '课程名';
        ALTER TABLE `course` MODIFY COLUMN `path` VARCHAR(60) NOT NULL  COMMENT '课程所在路径';
        ALTER TABLE `course` MODIFY COLUMN `course_no` VARCHAR(25) NOT NULL  COMMENT '课程序号';
        ALTER TABLE `type` MODIFY COLUMN `type_no` VARCHAR(25) NOT NULL  COMMENT '类型唯一值';
        ALTER TABLE `unit` ADD `phone` VARCHAR(11) NOT NULL  COMMENT '电话';
        ALTER TABLE `unit` MODIFY COLUMN `parent_no` VARCHAR(25)   COMMENT '父节点 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `file_path` VARCHAR(60) NOT NULL  COMMENT '文件路径';
        ALTER TABLE `unit` MODIFY COLUMN `next_no` VARCHAR(25)   COMMENT '后一个 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `prev_no` VARCHAR(25)   COMMENT '前一个 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `unit_no` VARCHAR(25) NOT NULL  COMMENT '单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `course_no` VARCHAR(25) NOT NULL  COMMENT '课程序号';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `type` MODIFY COLUMN `type_no` VARCHAR(20) NOT NULL  COMMENT '类型唯一值';
        ALTER TABLE `unit` DROP COLUMN `phone`;
        ALTER TABLE `unit` MODIFY COLUMN `parent_no` VARCHAR(20)   COMMENT '父节点 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `file_path` VARCHAR(20) NOT NULL  COMMENT '文件路径';
        ALTER TABLE `unit` MODIFY COLUMN `next_no` VARCHAR(20)   COMMENT '后一个 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `prev_no` VARCHAR(20)   COMMENT '前一个 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `unit_no` VARCHAR(20) NOT NULL  COMMENT '单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `course_no` VARCHAR(20) NOT NULL  COMMENT '课程序号';
        ALTER TABLE `course` MODIFY COLUMN `name` VARCHAR(30) NOT NULL  COMMENT '课程名';
        ALTER TABLE `course` MODIFY COLUMN `path` VARCHAR(30) NOT NULL  COMMENT '课程所在路径';
        ALTER TABLE `course` MODIFY COLUMN `course_no` VARCHAR(20) NOT NULL  COMMENT '课程序号';"""
