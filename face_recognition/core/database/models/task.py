from face_recognition.core.database.models.base import Base
from face_recognition.core.database.models.mixins import IdIntPkMixin, CreateTimeMixin


class Task(
    Base,
    IdIntPkMixin,
    CreateTimeMixin,
):
    pass
