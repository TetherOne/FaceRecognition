from typing import TYPE_CHECKING
from sqlalchemy import Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from face_recognition.core.database.models import Base
from face_recognition.core.database.models.choices import GenderEnum
from face_recognition.core.database.models.mixins import IdIntPkMixin


if TYPE_CHECKING:
    from face_recognition.core.database.models import TaskImage
    from face_recognition.core.database.models import BoundingBoxFace


class ImageFace(
    Base,
    IdIntPkMixin,
):
    age: Mapped[int] = mapped_column(DECIMAL(precision=4, scale=1))
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum, name="gender_enum"))
    image_id: Mapped[int] = mapped_column(ForeignKey("task_images.id"))
    image: Mapped["TaskImage"] = relationship(back_populates="faces")
    bbox: Mapped["BoundingBoxFace"] = relationship(
        back_populates="face",
        uselist=False,
        cascade="all, delete-orphan",
    )
