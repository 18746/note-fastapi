
from fastapi import FastAPI

from contextlib import asynccontextmanager
# 监听项目启动和关闭
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup event，项目启动")
    yield
    print("shutdown event，项目关闭")



