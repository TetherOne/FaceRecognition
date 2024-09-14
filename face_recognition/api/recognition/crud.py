from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from face_recognition.api.recognition.schemas import TaskSchema
from face_recognition.core.database.models import Task


async def get_tasks(
    session: AsyncSession,
) -> Sequence[Task]:
    stmt = select(Task).order_by(Task.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_task(
    session: AsyncSession,
    task_id: int,
) -> TaskSchema | None:
    return await session.get(Task, task_id)
