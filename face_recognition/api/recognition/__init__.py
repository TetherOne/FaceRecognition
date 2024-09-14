from fastapi import APIRouter

from face_recognition.api.recognition.views import router as recognition_router

router = APIRouter()

router.include_router(
    recognition_router,
)
