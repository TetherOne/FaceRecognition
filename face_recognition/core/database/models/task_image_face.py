# from typing import TYPE_CHECKING
#
# from sqlalchemy import DECIMAL, Enum, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from face_recognition.core.database.models import Base
# from face_recognition.core.database.models.choices import GenderEnum
# from face_recognition.core.database.models.mixins import IdIntPkMixin
#
# if TYPE_CHECKING:
#     from face_recognition.core.database.models import TaskImage
#     from face_recognition.core.database.models import BoundingBoxFace
#
#
# class TaskImageFace(
#     Base,
#     IdIntPkMixin,
# ):
#     age: Mapped[int] = mapped_column(DECIMAL(precision=4, scale=1))
#     gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum))
#     image_id: Mapped[int] = mapped_column(ForeignKey("task_images.id"))
#     image: Mapped["TaskImage"] = relationship("TaskImage", back_populates="faces")
#     bbox: Mapped["BoundingBoxFace"] = relationship(
#         "BoundingBoxFace",
#         back_populates="task_image_face",
#         uselist=False,
#     )
