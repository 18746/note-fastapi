from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `pwd` VARCHAR(30) NOT NULL  COMMENT '密码';
        ALTER TABLE `userinfo` MODIFY COLUMN `username` VARCHAR(30) NOT NULL  COMMENT '姓名';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `pwd` VARCHAR(20) NOT NULL  COMMENT '密码';
        ALTER TABLE `userinfo` MODIFY COLUMN `username` VARCHAR(20) NOT NULL  COMMENT '姓名';"""
