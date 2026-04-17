from fastapi import APIRouter

inner = APIRouter(prefix="/inner")


@inner.get("/leaf")
def leaf():
    return {}
