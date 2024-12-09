from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `token` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `phone` VARCHAR(11) NOT NULL  COMMENT '用户phone',
    `token` VARCHAR(50) NOT NULL  COMMENT 'token',
    `time_limit` INT NOT NULL  COMMENT '有效时间',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL  COMMENT '姓名',
    `phone` VARCHAR(11) NOT NULL  COMMENT '电话',
    `email` VARCHAR(50)   COMMENT '邮箱',
    `pwd` VARCHAR(20) NOT NULL  COMMENT '密码',
    `expire_time` DATETIME(6)   COMMENT '过期时间',
    `create_time` DATETIME(6) NOT NULL  COMMENT '创建时间',
    `update_time` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
