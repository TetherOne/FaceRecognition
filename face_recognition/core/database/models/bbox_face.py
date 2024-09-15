from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from face_recognition.core.database.models import Base
from face_recognition.core.database.models.mixins import IdIntPkMixin


if TYPE_CHECKING:
    from face_recognition.core.database.models import ImageFace


class BoundingBoxFace(
    Base,
    IdIntPkMixin,
):
    height: Mapped[int]
    width: Mapped[int]
    x: Mapped[int]
    y: Mapped[int]
    face_id: Mapped[int] = mapped_column(ForeignKey("image_faces.id"))
    face: Mapped["ImageFace"] = relationship(back_populates="bbox")

    __table_args__ = (
        CheckConstraint("height >= 0 and height <= 1079"),
        CheckConstraint("width >= 0 and width <= 1919"),
        CheckConstraint("x >= 0 and x <= 1919"),
        CheckConstraint("y >= 0 and y <= 1079"),
        UniqueConstraint("face_id"),
    )
