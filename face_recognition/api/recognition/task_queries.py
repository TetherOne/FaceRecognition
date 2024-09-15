from sqlalchemy.orm import selectinload

from face_recognition.core.database.models import Task, TaskImage, ImageFace


async def load_task_relations(stmt):
    return stmt.options(
        selectinload(Task.images)
        .selectinload(TaskImage.faces)
        .selectinload(ImageFace.bbox)
    )
