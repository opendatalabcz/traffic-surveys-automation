from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from tsa import enums

router = APIRouter(prefix="/task", tags=["tasks"])


class NewTask(BaseModel):
    detection_model: enums.DetectionModels
    output_method: enums.TaskOutputMethod
    parameters: Dict[str, Any]
    source_file: int
    tracking_model: enums.TrackingModel


@router.post("")
async def create(new_task: NewTask):
    print(new_task)
