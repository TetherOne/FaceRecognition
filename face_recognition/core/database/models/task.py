from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from face_recognition.core.database.models.base import Base
from face_recognition.core.database.models.mixins import IdIntPkMixin, CreateTimeMixin


if TYPE_CHECKING:
    from face_recognition.core.database.models import TaskImage


class Task(
    Base,
    IdIntPkMixin,
    CreateTimeMixin,
):
    faces: Mapped[int | None]
    men: Mapped[int | None]
    women: Mapped[int | None]
    average_male_age: Mapped[float | None] = mapped_column(
        DECIMAL(precision=4, scale=1),
    )
    average_female_age: Mapped[float | None] = mapped_column(
        DECIMAL(precision=4, scale=1),
    )
    images: Mapped[list["TaskImage"]] = relationship(back_populates="task")

    __table_args__ = (
        CheckConstraint("faces >= 0"),
        CheckConstraint("men >= 0"),
        CheckConstraint("women >= 0"),
        CheckConstraint("average_male_age >= 0"),
        CheckConstraint("average_female_age >= 0"),
    )
