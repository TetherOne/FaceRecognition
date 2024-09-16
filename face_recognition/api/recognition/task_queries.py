from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from face_recognition.core.database.models import Task, TaskImage, ImageFace


async def load_task_relations(stmt):
    return stmt.options(
        selectinload(Task.images)
        .selectinload(TaskImage.faces)
        .selectinload(ImageFace.bbox)
    )


async def get_task_with_images(session, task_id: int):
    task_query = await session.execute(
        select(Task)
        .where(Task.id == task_id)
        .options(
            joinedload(Task.images)
            .joinedload(TaskImage.faces)
            .joinedload(ImageFace.bbox)
        )
    )
    return task_query.scalars().first()
