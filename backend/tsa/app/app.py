from fastapi import FastAPI

from tsa.app.handlers import source_files, tasks


fast_app = FastAPI()

fast_app.include_router(source_files.router)
fast_app.include_router(tasks.router)
