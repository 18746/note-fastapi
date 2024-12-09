from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

from core.config import TORTOISE_ORM
register_tortoise(
    app = app,
    config = TORTOISE_ORM
)

from crud.user    import user  as UserCrud     # 操作数据库的函数
from crud.user    import token as TokenCrud

@app.middleware("http")
async def middle(request: Request, call_next):
    # print("before2 request")      # 请求代码块
    if request.url.path[0:6] == "/login" or request.url.path[0:5] == "/note":
    # if request.url.path[0:6] == "/login":
        phone = request.headers.get("phone")
        token = request.headers.get("token")
        if phone and token:
            # 1.1 用户存在
            if await UserCrud.has(phone):
                user_model = await UserCrud.get(phone)
                # 1.2 用户未过期
                if UserCrud.no_expire(user_model):
                    # 2.1 token存在
                    if await TokenCrud.has_token(phone, token):
                        token_model = await TokenCrud.get_token(phone, token)
                        # 2.2 token 未过期
                        if TokenCrud.no_expire(token_model):
                            response = await call_next(request)
                            # print("after2 request")       # 响应代码块
                            return response
        return JSONResponse(
            status_code=400,
            content={
                "detail": "用户不存在/token已过期，请重新登录"
            },
        )
    else:
        response = await call_next(request)
        # print("after2 request")       # 响应代码块
        return response

# 用户
from api.v1.user.user  import user_router
from api.v1.user.token import token_router
from api.v1.login      import login_router

app.include_router(user_router)
app.include_router(token_router)
app.include_router(login_router)

# 笔记
from api.v1.course.course import course_router
from api.v1.course.type   import type_router
from api.v1.course.unit   import unit_router
from api.v1.note          import note_router

app.include_router(course_router)
app.include_router(type_router)
app.include_router(unit_router)
app.include_router(note_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8070, reload=True)



