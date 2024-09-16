import os
from decimal import Decimal
from typing import TYPE_CHECKING

import aiofiles
import httpx
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from face_recognition.core.database.models import ImageFace, BoundingBoxFace
from face_recognition.core.settings.config import settings

if TYPE_CHECKING:
    from face_recognition.core.database.models import TaskImage
    from face_recognition.core.database.models import Task


async def delete_images_from_task_images(task_images: list["TaskImage"]) -> None:
    """
    Удаляет изображения с локального диска, связанные с Task.
    """
    for task_image in task_images:
        image_path = task_image.image
        if os.path.exists(image_path):
            os.remove(image_path)


async def save_image_locally(image_file: UploadFile, image_path: str) -> None:
    """
    Сохранение изображения локально на диск.
    """
    with open(image_path, "wb") as buffer:
        buffer.write(await image_file.read())


async def send_image_to_external_api(image_path: str, token: str) -> dict:
    """
    Запрос на сервис Tevian.ru для распознавания лица.
    """
    external_api_url = settings.service.url
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "image/jpeg",
    }

    async with httpx.AsyncClient() as client:
        async with aiofiles.open(image_path, "rb") as img_file:
            file_content = await img_file.read()
            response = await client.post(
                external_api_url, headers=headers, content=file_content
            )

    return response.json()


async def process_faces_data(
    faces_data: list,
    task: "Task",
    task_image_id: int,
    session: AsyncSession,
) -> None:
    """
    Вычисление кол-ва лиц, среднего возраста мужчин/женщин, кол-ва мужчин/женщин.
    """
    total_faces = Decimal(task.faces or 0)
    total_men = Decimal(task.men or 0)
    total_women = Decimal(task.women or 0)
    total_male_age = Decimal(task.average_male_age or 0) * total_men
    total_female_age = Decimal(task.average_female_age or 0) * total_women

    for face in faces_data:
        bbox = face.get("bbox", {})
        age = Decimal(face.get("demographics", {}).get("age", {}).get("mean", 0))
        gender = (face.get("demographics", {}).get("gender", "unknown")).upper()

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
            image_id=task_image_id,
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
