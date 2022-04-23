from itertools import chain
from pathlib import Path
from typing import Set

from tsa.config import config


class DiskManager:
    ALLOWED_SOURCE_FORMATS = ("mp4", "mov")

    def __init__(self):
        self.source_files_dir: Path = config.SOURCE_FILES_PATH

    def read_source_files_folder(self) -> Set[Path]:
        return self.read_folder(self.source_files_dir)

    def exists_in_source_files_folder(self, path: str) -> bool:
        return (self.source_files_dir / path).exists()

    def read_folder(self, folder: Path) -> Set[Path]:
        paths_generator = chain.from_iterable(
            folder.glob(f"*.{source_format}") for source_format in self.ALLOWED_SOURCE_FORMATS
        )
        return {path.relative_to(folder) for path in paths_generator}
