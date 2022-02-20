from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel
from sqlmodel import ARRAY, Column, Field, Enum, JSON, TEXT
from tsa import enums

from .base import SQLModel


class Task(SQLModel):
    # columns
    id: Optional[int] = Field(default=None, primary_key=True, description="Aut-generated primary identifier of a task.")
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


class NewTask(BaseModel):
    detection_model: enums.DetectionModels
    tracking_model: enums.TrackingModel
    method: enums.TaskOutputMethod
    parameters: Dict[str, Any]
