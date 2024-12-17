from fastapi import FastAPI

from core.lifespan    import lifespan
from core.application import APP_CONFIG
from core.middleware  import TokenMiddleware
from core.database    import app_bind_database

app = FastAPI(
    lifespan=lifespan,
    version=APP_CONFIG["version"],
)

app.add_middleware(TokenMiddleware, header_namespace="TokenMiddleware")

app_bind_database(app)


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
    from core.application import IP, PORT
    uvicorn.run("main:app", host=IP, port=PORT, reload=True)



