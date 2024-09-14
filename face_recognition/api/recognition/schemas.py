from datetime import datetime

from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    pass


class TaskSchema(TaskBaseSchema):
    id: int
    created_at: datetime
