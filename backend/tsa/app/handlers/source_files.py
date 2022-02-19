from typing import List

from fastapi import APIRouter, Depends

from tsa.app.disk_manager import DiskManager
from tsa.app.repositories.source_file import SourceFileRepository
from tsa.app.schemas import SourceFile, SourceFileModel


router = APIRouter(prefix="/source_file", tags=["source_files"])


def check_source_files_exist(source_files: List[SourceFileModel], location: DiskManager) -> List[bool]:
    files_on_disk = {str(path) for path in location.read_source_files_folder()}
    return [source_file.path in files_on_disk for source_file in source_files]


@router.get("", response_model=List[SourceFile])
async def read(
    disk_manager: DiskManager = Depends(DiskManager),
    source_file_repository: SourceFileRepository = Depends(SourceFileRepository),
):
    source_files = await source_file_repository.list()
    source_files_existence = check_source_files_exist(source_files, disk_manager)

    return [
        SourceFile(**source_file.dict(), file_exists=exists)
        for source_file, exists in zip(source_files, source_files_existence)
    ]


@router.post(
    "/discover",
    description="Run discovery of new files in the source files folder.",
    response_model=List[SourceFile],
    response_description="Newly discovered source files. Already existing source files are not counted.",
)
async def discover(
    disk_manager: DiskManager = Depends(DiskManager),
    source_file_repository: SourceFileRepository = Depends(SourceFileRepository),
):
    discovered_files = []

    for file in disk_manager.read_source_files_folder():
        source_file = SourceFile(path=str(file))
        new_object = await source_file_repository.create(source_file)

        if new_object is not None:
            discovered_files.append(SourceFile(**new_object.dict(), file_exists=True))

    return discovered_files
