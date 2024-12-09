from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `course` DROP COLUMN `path`;
        ALTER TABLE `unit` DROP COLUMN `file_path`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `unit` ADD `file_path` VARCHAR(60) NOT NULL  COMMENT '文件路径';
        ALTER TABLE `course` ADD `path` VARCHAR(60) NOT NULL  COMMENT '课程所在路径';"""
