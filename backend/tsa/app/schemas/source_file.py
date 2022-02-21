from typing import List, Optional

from sqlmodel import Column, Field, Enum, TEXT
from tsa import enums

from .base import SQLModel
from .task import Task


class SourceFileBase(SQLModel):
    # columns
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        description="Auto-incremented primary key of a source file.",
    )
    name: Optional[str] = Field(
        sa_column=Column(TEXT),
        description="Name of the source file assigned by a user.",
    )
    path: str = Field(
        sa_column=Column(TEXT, nullable=False, unique=True),
        description="Relative path to the source file. It has to be unique.",
    )
    status: enums.SourceFileStatus = Field(
        default=enums.SourceFileStatus.new,
        sa_column=Column(Enum(enums.SourceFileStatus, name="source_file_status"), server_default="new", nullable=False),
        description="Status of the source file.",
    )


class SourceFileModel(SourceFileBase, table=True):
    __tablename__ = "source_file"


class SourceFile(SourceFileBase):
    file_exists: bool = Field(description="File connected to the object exists on disk.")


class SourceFileWithTasks(SourceFile):
    tasks: List[Task] = Field(description="A list of tasks connected to the source file.")
