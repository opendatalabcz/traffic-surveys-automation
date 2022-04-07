from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field, validator

from tsa import enums
from tsa.config import CONFIGURABLE_VARIABLES

from .line import LinesBase

PARAMETERS_TYPE = Dict[str, Union[float, int]]


class Task(BaseModel):
    # columns
    id: Optional[int] = Field(
        default=None, primary_key=True, nullable=False, description="Auto-generated primary identifier of a task."
    )
    name: str = Field(description="Name of the task.")
    models: Tuple[str, ...] = Field(
        description="List of models to use when processing the task. Usually, it's one detector and one tracker.",
    )
    output_path: str = Field(description="Output file generated as a result of a task.")
    parameters: Dict[str, Any] = Field(
        description="Parameters of the models. These override the default parameters of the app."
    )
    status: enums.TaskStatus = Field(default=enums.TaskStatus.created, description="Status of the a task.")
    # relationships
    source_file_id: int = Field(foreign_key="source_file.id")


class TaskWithLines(Task):
    lines: List[LinesBase]


class NewTask(BaseModel):
    name: str
    detection_model: enums.DetectionModels
    tracking_model: enums.TrackingModel
    parameters: PARAMETERS_TYPE

    @validator("parameters")
    def correct_parameters(cls, v: PARAMETERS_TYPE) -> PARAMETERS_TYPE:
        diff = set(v.keys()).difference(CONFIGURABLE_VARIABLES)
        if diff:
            raise ValueError(f"Parameters contain unexpected variables: {', '.join(diff)}")
        return v
