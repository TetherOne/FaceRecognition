import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from face_recognition.core.database.models import TaskImage


async def delete_images_from_task_images(task_images: list["TaskImage"]) -> None:
    """
    Удаляет изображения с локального диска, связанные с Task.
    """
    for task_image in task_images:
        image_path = task_image.image
        if os.path.exists(image_path):
            os.remove(image_path)
