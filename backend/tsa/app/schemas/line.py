from typing import List, Optional, Tuple

from pydantic import BaseModel, Field


class Point(BaseModel):
    x: float
    y: float

    def as_tuple(self) -> Tuple[float, float]:
        return self.x, self.y


class Line(BaseModel):
    name: str = Field(description="Name of a single line. This helps to users to identify lines in the result matrix.")
    start: Point
    end: Point


class Lines(BaseModel):
    lines: List[Line] = Field(description="JSON data describing the lines.")


class LinesBase(Lines):
    # columns
    id: Optional[int] = Field(default=None, description="Auto-incremented identifier of single lines definition.")
    # relationships
    task_id: int = Field(description="Reference to the task the lines belong to.")

    @classmethod
    def from_db_dict(cls, db_data):
        return cls(
            id=db_data.id,
            task_id=db_data.task_id,
            lines=[Line(**line_data) for line_data in db_data.lines],
        )


class LinesResponse(BaseModel):
    names: List[str]
    counts: List[List[int]]
