from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from tsa.app.database import db_engine
from tsa.app.exceptions import NotFoundError
from tsa.app.handlers import lines, source_files, tasks

fast_app = FastAPI()

fast_app.include_router(source_files.router)
fast_app.include_router(tasks.router)
fast_app.include_router(lines.router)

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@fast_app.middleware("http")
async def exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except NotFoundError as exc:
        return Response(str(exc), status_code=status.HTTP_404_NOT_FOUND)


@fast_app.on_event("startup")
async def on_app_startup():
    await db_engine.connect()


@fast_app.on_event("shutdown")
async def on_app_shutdown():
    await db_engine.disconnect()
