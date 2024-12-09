from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `device_num` INT NOT NULL  COMMENT '允许同时登录的设备数量';
        ALTER TABLE `user` DROP COLUMN `username`;
        CREATE TABLE IF NOT EXISTS `userinfo` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL  COMMENT '姓名',
    `phone` VARCHAR(11) NOT NULL  COMMENT '电话',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `username` VARCHAR(20) NOT NULL  COMMENT '姓名';
        ALTER TABLE `user` DROP COLUMN `device_num`;
        DROP TABLE IF EXISTS `userinfo`;"""
