from typing import Annotated, List

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from face_recognition.api.recognition import crud
from face_recognition.api.recognition.dependencies import task_by_id
from face_recognition.api.recognition.schemas import TaskSchema, CreateTaskSchema
from face_recognition.core.database.models import (
    Task,
    TaskImage,
    ImageFace,
)
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


@router.post(
    "/tasks/create",
    response_model=CreateTaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.create_task(session=session)


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


@router.post(
    "/tasks/{task_id}/add-image",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_image_to_task(
    task_id: int,
    image_file: UploadFile,
    image_name: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    task_query = await session.execute(
        select(Task)
        .where(Task.id == task_id)
        .options(
            joinedload(Task.images)
            .joinedload(TaskImage.faces)
            .joinedload(ImageFace.bbox)
        )
    )
    task = task_query.scalars().first()

    image_path = f"media/{image_file.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(await image_file.read())

    task_image = TaskImage(name=image_name, image=image_path, task_id=task_id)
    session.add(task_image)
    await session.commit()
    await session.refresh(task)

    task_query = await session.execute(
        select(Task)
        .where(Task.id == task_id)
        .options(
            joinedload(Task.images)
            .joinedload(TaskImage.faces)
            .joinedload(ImageFace.bbox)
        )
    )
    task = task_query.scalars().first()

    task_schema = TaskSchema.from_orm(task)
    return task_schema
