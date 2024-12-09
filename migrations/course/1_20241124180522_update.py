from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `course` MODIFY COLUMN `type_no` VARCHAR(20)   COMMENT '类型唯一值';
        ALTER TABLE `unit` MODIFY COLUMN `parent_no` VARCHAR(20)   COMMENT '父节点 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `prev_no` VARCHAR(20)   COMMENT '前一个 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `next_no` VARCHAR(20)   COMMENT '后一个 单元序号';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `unit` MODIFY COLUMN `parent_no` VARCHAR(20) NOT NULL  COMMENT '父节点 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `prev_no` VARCHAR(20) NOT NULL  COMMENT '前一个 单元序号';
        ALTER TABLE `unit` MODIFY COLUMN `next_no` VARCHAR(20) NOT NULL  COMMENT '后一个 单元序号';
        ALTER TABLE `course` MODIFY COLUMN `type_no` VARCHAR(20) NOT NULL  COMMENT '类型唯一值';"""
