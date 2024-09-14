from fastapi import APIRouter
from face_recognition.api.recognition import router as recognition_router
from face_recognition.core.settings.config import settings

router = APIRouter(
    prefix=settings.api.full_prefix,
)

router.include_router(recognition_router)
