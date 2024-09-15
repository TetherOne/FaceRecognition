from typing import Annotated, List

import httpx
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from face_recognition.api.recognition import crud
from face_recognition.api.recognition.dependencies import task_by_id
from face_recognition.api.recognition.schemas import TaskSchema
from face_recognition.core.database.models import Task
from face_recognition.core.helpers.db_helper import db_helper
from face_recognition.core.settings.config import settings

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


@router.post(
    "/create-task",
    status_code=status.HTTP_201_CREATED,
)
async def create_task(files: list[UploadFile]):
    async with httpx.AsyncClient() as client:
        responses = []
        for file in files:
            file_bytes = await file.read()
            headers = {
                "Authorization": f"Bearer {settings.service.token}",
                "Content-Type": file.content_type,
            }
            response = await client.post(
                settings.service.url, headers=headers, content=file_bytes
            )
            responses.append(response.json())

        return responses


@router.delete(
    "/delete/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    task: Task = Depends(task_by_id),
) -> None:
    await crud.delete_task(session=session, task=task)
