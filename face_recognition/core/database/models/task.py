from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum
from face_recognition.core.database.models.base import Base
from face_recognition.core.database.models.choices import GenderEnum
from face_recognition.core.database.models.mixins import IdIntPkMixin, CreateTimeMixin


class Task(
    Base,
    IdIntPkMixin,
    CreateTimeMixin,
):
    task_images: Mapped[list["TaskImage"]] = relationship(back_populates="task")


class TaskImage(
    Base,
    IdIntPkMixin,
):
    name: Mapped[str] = mapped_column(String(256))
    age: Mapped[int]
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped[Task] = relationship("Task", back_populates="task_images")
