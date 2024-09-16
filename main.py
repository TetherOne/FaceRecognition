from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from face_recognition.api import router

app = FastAPI(
    default_response_class=ORJSONResponse,
)

app.mount(
    "/media",
    StaticFiles(directory="media"),
)

app.include_router(router)
