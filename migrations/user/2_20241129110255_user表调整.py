from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `device_num` SET DEFAULT 1;
        ALTER TABLE `user` ALTER COLUMN `email` SET DEFAULT '';
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(50) NOT NULL  COMMENT '邮箱' DEFAULT '';
        ALTER TABLE `userinfo` DROP COLUMN `create_time`;
        ALTER TABLE `userinfo` DROP COLUMN `update_time`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `device_num` DROP DEFAULT;
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(50)   COMMENT '邮箱';
        ALTER TABLE `user` ALTER COLUMN `email` DROP DEFAULT;
        ALTER TABLE `userinfo` ADD `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间';
        ALTER TABLE `userinfo` ADD `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间';"""
