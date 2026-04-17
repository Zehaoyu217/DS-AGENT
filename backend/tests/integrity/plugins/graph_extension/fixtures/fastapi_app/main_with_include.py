from fastapi import FastAPI

from . import composed_router

app = FastAPI()
app.include_router(composed_router.inner, prefix="/v1")
