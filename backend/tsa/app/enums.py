from enum import Enum


class SourceFileStatus(Enum):
    new = "new"
    processing = "processing"
    processed = "processed"
    deleted = "deleted"


class TaskStatus(Enum):
    created = "created"
    processing = "processing"
    completed = "completed"
    failed = "failed"
