from datetime import datetime

from pydantic import BaseModel

from face_recognition.core.database.models.choices import GenderEnum


class BoundingBoxFaceSchema(BaseModel):
    height: int
    width: int
    x: int
    y: int


class ImageFaceSchema(BaseModel):
    id: int
    age: float
    gender: GenderEnum
    bbox: BoundingBoxFaceSchema | None


class TaskImageSchema(BaseModel):
    name: str
    image: str
    faces: list[ImageFaceSchema]


class TaskBaseSchema(BaseModel):
    faces: int | None
    men: int | None
    women: int | None
    average_male_age: float | None
    average_female_age: float | None


class TaskSchema(TaskBaseSchema):
    id: int
    created_at: datetime
    images: list[TaskImageSchema]
