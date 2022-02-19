from typing import List

from pydantic import Field

from .base import SourceFile as SourceFileModel, Task


class SourceFile(SourceFileModel):
    file_exists: bool = Field(description="File connected to the object exists on disk.")


class SourceFileWithTasks(SourceFile):
    tasks: List[Task] = Field(description="A list of tasks connected to the source file.")
