from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from face_recognition.api.recognition import crud
from face_recognition.api.recognition.dependencies import task_by_id
from face_recognition.api.recognition.schemas import TaskSchema
from face_recognition.core.helpers.db_helper import db_helper

router = APIRouter(tags=["Tasks"])


@router.get(
    "/tasks",
    response_model=List[TaskSchema],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.get_tasks(session=session)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    task: TaskSchema = Depends(task_by_id),
):
    return task
