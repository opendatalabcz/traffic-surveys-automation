from typing import List, Optional, Tuple

from pydantic import BaseModel
from sqlmodel import Column, Field, JSON

from .base import SQLModel


class Point(BaseModel):
    x: float
    y: float

    def as_tuple(self) -> Tuple[float, float]:
        return self.x, self.y


class Line(BaseModel):
    name: str = Field(description="Name of a single line. This helps to users to identify lines in the result matrix.")
    start: Point
    end: Point


class LinesResponse(BaseModel):
    names: List[str]
    counts: List[List[int]]


class Lines(SQLModel):
    lines: List[Line] = Field(
        sa_column=Column(JSON, nullable=False, default={}), description="JSON data describing the lines."
    )


class LinesBase(Lines):
    # columns
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        description="Auto-incremented identifier of single lines definition.",
    )
    # relationships
    task_id: int = Field(
        foreign_key="task.id", nullable=False, description="Reference to the task the lines belong to."
    )

    @classmethod
    def from_db_dict(cls, db_data):
        return cls(
            id=db_data.id,
            task_id=db_data.task_id,
            lines=[Line(**line_data) for line_data in db_data.lines],
        )


class LinesModel(LinesBase, table=True):
    __tablename__ = "lines"
