from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import NoResultFound
from starlette.status import HTTP_404_NOT_FOUND

from tsa.app.handlers import lines, source_files, tasks


fast_app = FastAPI()

fast_app.include_router(source_files.router)
fast_app.include_router(tasks.router)
fast_app.include_router(lines.router)

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@fast_app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        return await call_next(request)
    except NoResultFound as exc:
        raise HTTPException(HTTP_404_NOT_FOUND, str(exc)) from exc
