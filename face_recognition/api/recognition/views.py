from typing import Annotated, List
from decimal import Decimal

import httpx
from fastapi import APIRouter, Depends, UploadFile, HTTPException
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
    BoundingBoxFace,
)
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


def map_gender(gender: str) -> str:
    return gender.upper()


@router.post(
    "/tasks/{task_id}/add-image",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_image_to_task(
    task_id: int,
    image_file: UploadFile,
    image_name: str,
    session: AsyncSession = Depends(db_helper.session_getter),
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
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    image_path = f"media/{image_file.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(await image_file.read())

    task_image = TaskImage(name=image_name, image=image_path, task_id=task_id)
    session.add(task_image)
    await session.commit()

    external_api_url = (
        "https://backend.facecloud.tevian.ru/api/v1/detect?demographics=true"
    )
    headers = {
        "Authorization": f"Bearer {settings.service.token}",
        "Content-Type": "image/jpeg",
    }

    async with httpx.AsyncClient() as client:
        with open(image_path, "rb") as img_file:
            file_content = img_file.read()
            response = await client.post(
                external_api_url, headers=headers, content=file_content
            )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to analyze image"
        )

    response_data = response.json()
    faces_data = response_data.get("data", [])

    total_faces = Decimal(task.faces or 0)
    total_men = Decimal(task.men or 0)
    total_women = Decimal(task.women or 0)
    total_male_age = Decimal(task.average_male_age or 0) * total_men
    total_female_age = Decimal(task.average_female_age or 0) * total_women

    for face in faces_data:
        bbox = face.get("bbox", {})
        age = Decimal(face.get("demographics", {}).get("age", {}).get("mean", 0))
        gender = map_gender(face.get("demographics", {}).get("gender", "unknown"))

        if gender == "MALE":
            total_men += 1
            total_male_age += age
        elif gender == "FEMALE":
            total_women += 1
            total_female_age += age

        total_faces += 1

        face_data = ImageFace(
            age=age,
            gender=gender,
            image_id=task_image.id,
            bbox=BoundingBoxFace(
                height=Decimal(bbox.get("height", 0)),
                width=Decimal(bbox.get("width", 0)),
                x=Decimal(bbox.get("x", 0)),
                y=Decimal(bbox.get("y", 0)),
            ),
        )
        session.add(face_data)

    avg_male_age = total_male_age / total_men if total_men > 0 else None
    avg_female_age = total_female_age / total_women if total_women > 0 else None

    task.faces = int(total_faces)
    task.men = int(total_men)
    task.women = int(total_women)
    task.average_male_age = float(avg_male_age) if avg_male_age is not None else None
    task.average_female_age = (
        float(avg_female_age) if avg_female_age is not None else None
    )

    await session.commit()

    await session.refresh(task)
    task_schema = TaskSchema.from_orm(task)
    return task_schema
