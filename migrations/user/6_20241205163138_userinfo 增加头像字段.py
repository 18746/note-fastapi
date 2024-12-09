from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `userinfo` ADD `picture` VARCHAR(30) NOT NULL  COMMENT '用户头像';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `userinfo` DROP COLUMN `picture`;"""
