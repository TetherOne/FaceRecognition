from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from face_recognition.api.recognition.task_queries import load_task_relations
from face_recognition.core.database.models import Task


async def get_tasks(
    session: AsyncSession,
) -> Sequence[Task]:
    stmt = select(Task).order_by(Task.created_at.desc())
    stmt = await load_task_relations(stmt)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_task(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    stmt = select(Task).filter(Task.id == task_id)
    stmt = await load_task_relations(stmt)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_task(
    session: AsyncSession,
    task: Task,
) -> None:
    await session.delete(task)
    await session.commit()
