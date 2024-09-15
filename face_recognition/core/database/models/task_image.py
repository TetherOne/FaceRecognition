from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from face_recognition.core.database.models import Base
from face_recognition.core.database.models.mixins import IdIntPkMixin


if TYPE_CHECKING:
    from face_recognition.core.database.models import Task
    from face_recognition.core.database.models import ImageFace


class TaskImage(
    Base,
    IdIntPkMixin,
):
    name: Mapped[str] = mapped_column(String(256))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped["Task"] = relationship(back_populates="images")
    faces: Mapped[list["ImageFace"]] = relationship(
        back_populates="image",
        cascade="all, delete-orphan",
    )
