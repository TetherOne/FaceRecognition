from sqlalchemy import DECIMAL, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from face_recognition.core.database.models.base import Base
from face_recognition.core.database.models.mixins import IdIntPkMixin, CreateTimeMixin


class Task(
    Base,
    IdIntPkMixin,
    CreateTimeMixin,
):
    faces: Mapped[int | None]
    men: Mapped[int | None]
    women: Mapped[int | None]
    average_male_age: Mapped[float | None] = mapped_column(
        DECIMAL(precision=10, scale=1)
    )
    average_female_age: Mapped[float | None] = mapped_column(
        DECIMAL(precision=10, scale=1)
    )

    __table_args__ = (
        CheckConstraint("faces >= 0"),
        CheckConstraint("men >= 0"),
        CheckConstraint("women >= 0"),
        CheckConstraint("average_male_age >= 0"),
        CheckConstraint("average_female_age >= 0"),
    )
    # task_images: Mapped[list["TaskImage"]] = relationship(back_populates="task")


# class TaskImage(
#     Base,
#     IdIntPkMixin,
# ):
#     name: Mapped[str] = mapped_column(String(256))
#     age: Mapped[int]
#     gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum))
#     task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
#     task: Mapped[Task] = relationship("Task", back_populates="task_images")
