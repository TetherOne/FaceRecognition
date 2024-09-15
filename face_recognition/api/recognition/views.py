import os
from typing import Annotated, List

import httpx
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from face_recognition.api.recognition import crud
from face_recognition.api.recognition.dependencies import task_by_id
from face_recognition.api.recognition.schemas import TaskSchema
from face_recognition.core.database.models import (
    Task,
    TaskImage,
    ImageFace,
    BoundingBoxFace,
)
from face_recognition.core.database.models.choices import GenderEnum
from face_recognition.core.helpers.db_helper import db_helper
from face_recognition.core.settings.config import settings, MEDIA_DIR

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
    response_model=TaskSchema,
)
async def create_task(files: list[UploadFile]):
    async with httpx.AsyncClient() as client:
        responses = []
        file_paths = []
        file_names = []

        for file in files:
            file_bytes = await file.read()
            file_name = file.filename
            file_path = os.path.join(MEDIA_DIR, file_name)

            with open(file_path, "wb") as f:
                f.write(file_bytes)

            headers = {
                "Authorization": f"Bearer {settings.service.token}",
                "Content-Type": file.content_type,
            }
            response = await client.post(
                settings.service.url, headers=headers, content=file_bytes
            )
            responses.append(response.json())
            file_paths.append(file_path)
            file_names.append(file_name)

    total_faces = 0
    total_men = 0
    total_women = 0
    total_male_age = 0
    total_female_age = 0

    task_images = []

    for i, (response, file_path, file_name) in enumerate(
        zip(responses, file_paths, file_names)
    ):
        image_faces = []

        for face_data in response["data"]:
            age = face_data["demographics"]["age"]["mean"]
            gender = face_data["demographics"]["gender"].lower()

            gender_enum = GenderEnum.MALE if gender == "male" else GenderEnum.FEMALE

            image_face = ImageFace(
                age=age,
                gender=gender_enum,
                bbox=BoundingBoxFace(
                    height=face_data["bbox"]["height"],
                    width=face_data["bbox"]["width"],
                    x=face_data["bbox"]["x"],
                    y=face_data["bbox"]["y"],
                ),
            )
            image_faces.append(image_face)

            total_faces += 1
            if gender_enum == GenderEnum.MALE:
                total_men += 1
                total_male_age += age
            elif gender_enum == GenderEnum.FEMALE:
                total_women += 1
                total_female_age += age

        task_image = TaskImage(name=file_name, image=file_path, faces=image_faces)
        task_images.append(task_image)

    avg_male_age = total_male_age / total_men if total_men > 0 else None
    avg_female_age = total_female_age / total_women if total_women > 0 else None

    task = Task(
        faces=total_faces,
        men=total_men,
        women=total_women,
        average_male_age=avg_male_age,
        average_female_age=avg_female_age,
        images=task_images,
    )

    async for db in db_helper.session_getter():
        db.add(task)
        await db.commit()

        result = await db.execute(
            select(Task)
            .options(
                joinedload(Task.images)
                .joinedload(TaskImage.faces)
                .joinedload(ImageFace.bbox)
            )
            .filter(Task.id == task.id)
        )

        task = result.unique().scalar_one()

    return task


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
