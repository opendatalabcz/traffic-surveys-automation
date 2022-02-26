from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, validator
from sqlmodel import ARRAY, Column, Field, Enum, JSON, TEXT
from tsa import enums

from tsa.config import CONFIGURABLE_VARIABLES
from .base import SQLModel
from .line import LinesBase


class Task(SQLModel):
    # columns
    id: Optional[int] = Field(
        default=None, primary_key=True, nullable=False, description="Aut-generated primary identifier of a task."
    )
    name: str = Field(sa_column=Column(TEXT, nullable=False), description="Name of the task.")
    models: Tuple[str, ...] = Field(
        sa_column=Column(ARRAY(TEXT), default=[], nullable=False),
        description="List of models to use when processing the task. Usually, it's one detector and one tracker.",
    )
    output_method: enums.TaskOutputMethod = Field(
        sa_column=Column(Enum(enums.TaskOutputMethod, name="task_output_method"), nullable=False),
        description="Method used for creating an output of the task.",
    )
    output_path: str = Field(
        sa_column=Column(TEXT, nullable=False, unique=True),
        description="Output file generated as a result of a task.",
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


class TaskModel(Task, table=True):
    __tablename__ = "task"


class TaskWithLines(Task):
    lines: List[LinesBase]


class NewTask(BaseModel):
    name: str
    detection_model: enums.DetectionModels
    tracking_model: enums.TrackingModel
    method: enums.TaskOutputMethod
    parameters: Dict[str, Any]

    @validator("parameters")
    def correct_parameters(cls, v: Dict[str, Any]):
        diff = set(v.keys()).difference(CONFIGURABLE_VARIABLES)
        if not diff:
            raise ValueError(f"Parameters contain unexpected variables: {', '.join(diff)}")
