
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from crud.user    import user  as UserCrud     # 操作数据库的函数
from crud.user    import token as TokenCrud
# token验证
class TokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_namespace: str):
        super().__init__(app)
        # 自定义参数，用于定义middleware的header名称空间
        self.header_namespace = header_namespace

    async def dispatch(self, request: Request, call_next):
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
            phone = request.headers.get("phone")
            token = request.headers.get("token")
            not_token = False
            if phone and token:
                if request.url.path[0:7] == "/course" or request.url.path[0:5] == "/type" or request.url.path[0:5] == "/unit":
                    # 1.1 用户存在
                    if await UserCrud.has(phone):
                        user_model = await UserCrud.get(phone)
                        # 1.2 用户未过期
                        if UserCrud.no_expire(user_model):
                            # 2.1 token不存在
                            if not await TokenCrud.has_token(phone, token):
                                not_token = True

            response = await call_next(request)
            if not_token:
                response.headers["not-token"] = "1"
            # print("after2 request")       # 响应代码块
            return response


