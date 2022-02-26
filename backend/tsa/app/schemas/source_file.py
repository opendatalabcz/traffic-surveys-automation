from typing import List, Optional

from pydantic import BaseModel, Field
from tsa import enums

from .task import Task


class SourceFileBase(BaseModel):
    # columns
    id: Optional[int] = Field(
        default=None,
        description="Auto-incremented primary key of a source file.",
    )
    name: str = Field(description="Name of the source file created according to the file path.")
    path: str = Field(description="Relative path to the source file. It has to be unique.")
    status: enums.SourceFileStatus = Field(default=enums.SourceFileStatus.new, description="Status of the source file.")


class SourceFile(SourceFileBase):
    file_exists: bool = Field(description="File connected to the object exists on disk.")


class SourceFileWithTasks(SourceFile):
    tasks: List[Task] = Field(description="A list of tasks connected to the source file.")
