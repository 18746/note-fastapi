from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `email` DROP DEFAULT;
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(50)   COMMENT '邮箱';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(50) NOT NULL  COMMENT '邮箱' DEFAULT '';
        ALTER TABLE `user` ALTER COLUMN `email` SET DEFAULT '';"""
