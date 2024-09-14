from datetime import datetime

from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    faces: int | None
    men: int | None
    women: int | None
    average_male_age: float | None
    average_female_age: float | None


class TaskSchema(TaskBaseSchema):
    id: int
    created_at: datetime
