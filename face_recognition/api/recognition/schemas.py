from datetime import datetime

from pydantic import BaseModel


class BoundingBoxFaceSchema(BaseModel):
    height: int
    width: int
    x: int
    y: int

    class Config:
        from_attributes = True


class ImageFaceSchema(BaseModel):
    id: int
    age: float
    gender: str
    bbox: BoundingBoxFaceSchema

    class Config:
        from_attributes = True


class TaskImageSchema(BaseModel):
    name: str
    image: str
    faces: list[ImageFaceSchema]

    class Config:
        from_attributes = True


class TaskBaseSchema(BaseModel):
    faces: int | None
    men: int | None
    women: int | None
    average_male_age: float | None
    average_female_age: float | None

    class Config:
        from_attributes = True


class TaskSchema(TaskBaseSchema):
    id: int
    created_at: datetime
    images: list[TaskImageSchema]

    class Config:
        from_attributes = True


class CreateTaskSchema(TaskBaseSchema):
    id: int
    created_at: datetime
