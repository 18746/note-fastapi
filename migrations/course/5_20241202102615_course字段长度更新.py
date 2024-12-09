from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `course` MODIFY COLUMN `course_no` VARCHAR(30) NOT NULL  COMMENT '课程序号';
        ALTER TABLE `type` MODIFY COLUMN `type_no` VARCHAR(30) NOT NULL  COMMENT '类型唯一值';
        ALTER TABLE `unit` MODIFY COLUMN `course_no` VARCHAR(30) NOT NULL  COMMENT '课程序号';
        ALTER TABLE `unit` MODIFY COLUMN `parent_no` VARCHAR(30)   COMMENT '父节点 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `next_no` VARCHAR(30)   COMMENT '后一个 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `unit_no` VARCHAR(30) NOT NULL  COMMENT '单元序号';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `type` MODIFY COLUMN `type_no` VARCHAR(25) NOT NULL  COMMENT '类型唯一值';
        ALTER TABLE `unit` MODIFY COLUMN `course_no` VARCHAR(25) NOT NULL  COMMENT '课程序号';
        ALTER TABLE `unit` MODIFY COLUMN `parent_no` VARCHAR(25)   COMMENT '父节点 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `next_no` VARCHAR(25)   COMMENT '后一个 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `unit_no` VARCHAR(25) NOT NULL  COMMENT '单元序号';
        ALTER TABLE `course` MODIFY COLUMN `course_no` VARCHAR(25) NOT NULL  COMMENT '课程序号';"""
