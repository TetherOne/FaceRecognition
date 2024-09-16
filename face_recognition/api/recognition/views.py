from typing import Annotated, List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from face_recognition.api.recognition import crud
from face_recognition.api.recognition.dependencies import task_by_id
from face_recognition.api.recognition.schemas import TaskSchema, CreateTaskSchema
from face_recognition.api.recognition.task_queries import get_task_with_images
from face_recognition.core.database.models import (
    Task,
    TaskImage,
)
from face_recognition.core.helpers.db_helper import db_helper
from face_recognition.core.settings.config import settings
from face_recognition.tools.utils import (
    send_image_to_external_api,
    save_image_locally,
    process_faces_data,
)

router = APIRouter(tags=["Tasks"])


@router.get(
    "/tasks",
    response_model=List[TaskSchema],
    status_code=status.HTTP_200_OK,
    summary="Getting a list of tasks",
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
    summary="Getting a task by id",
)
async def get_task(
    task: TaskSchema = Depends(task_by_id),
):
    return task


@router.post(
    "/tasks/create",
    response_model=CreateTaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
)
async def create_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.create_task(session=session)


@router.delete(
    "/{task_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task by id",
)
async def delete_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    task: Task = Depends(task_by_id),
) -> None:
    await crud.delete_task(session=session, task=task)


@router.post(
    "/tasks/{task_id}/add-image",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add an image to a task",
)
async def add_image_to_task(
    task_id: int,
    image_name: str,
    image_file: UploadFile,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    task = await get_task_with_images(session, task_id)

    image_path = f"media/{image_file.filename}"
    await save_image_locally(image_file, image_path)

    task_image = TaskImage(name=image_name, image=image_path, task_id=task_id)
    session.add(task_image)
    await session.commit()

    response_data = await send_image_to_external_api(image_path, settings.service.token)
    faces_data = response_data.get("data", [])

    await process_faces_data(faces_data, task, task_image.id, session)

    await session.refresh(task)
    task_schema = TaskSchema.from_orm(task)
    return task_schema
