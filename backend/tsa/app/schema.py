from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import ARRAY, Column, Field, Enum, JSON, Relationship, SQLModel, TEXT

from tsa.app import enums


class SourceFile(SQLModel, table=True):
    __tablename__ = "source_file"
    # columns
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
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
    # relationships
    tasks: List["Task"] = Relationship(back_populates="task")


class Task(SQLModel, table=True):
    # columns
    id: str = Field(
        sa_column=Column(UUID, primary_key=True),
        description="Primary identifier of a task. This is generated when a task is created on the app level.",
    )
    models: Tuple[str] = Field(
        sa_column=Column(ARRAY(TEXT), default=[]),
        description="List of models to use when processing the task. Usually, it's one detector and one tracker.",
    )
    parameters: Dict[str, Any] = Field(
        sa_column=Column(JSON, default={}),
        description="Parameters of the models. These override the default parameters of the app.",
    )
    status: enums.TaskStatus = Field(
        default=enums.TaskStatus.created,
        sa_column=Column(Enum(enums.TaskStatus, name="task_status"), server_default="created", nullable=False),
        description="Status of the a task.",
    )
    # relationships
    source_file_id: int = Field(foreign_key="source_file.id")
