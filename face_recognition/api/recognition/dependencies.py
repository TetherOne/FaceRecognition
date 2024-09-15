from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from face_recognition.api.recognition import crud
from face_recognition.api.recognition.schemas import TaskSchema
from face_recognition.core.helpers.db_helper import db_helper
from face_recognition.tools.errors import NotFound


async def task_by_id(
    task_id: Annotated[int, Path],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> TaskSchema:
    """
    Вспомогательная функция для
    получения Task по id
    """
    task = await crud.get_task(
        session=session,
        task_id=task_id,
    )
    if task is not None:
        return task
    raise NotFound()
