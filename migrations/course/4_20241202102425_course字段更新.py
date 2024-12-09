from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `course` ADD `description` VARCHAR(300) NOT NULL  COMMENT '课程简介';
        ALTER TABLE `course` ADD `update_num` INT NOT NULL  COMMENT '更新次数' DEFAULT 1;
        ALTER TABLE `course` ADD `click_count` INT NOT NULL  COMMENT '点击次数' DEFAULT 1;
        ALTER TABLE `unit` DROP COLUMN `prev_no`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `unit` ADD `prev_no` VARCHAR(25)   COMMENT '前一个 单元序号';
        ALTER TABLE `course` DROP COLUMN `description`;
        ALTER TABLE `course` DROP COLUMN `update_num`;
        ALTER TABLE `course` DROP COLUMN `click_count`;"""
