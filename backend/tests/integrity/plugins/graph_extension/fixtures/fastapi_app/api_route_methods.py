from fastapi import APIRouter, FastAPI

router = APIRouter(prefix="/multi")
app = FastAPI()


@router.api_route("/both", methods=["GET", "POST"])
def both_methods():
    return {}


def programmatic_handler():
    return {}


app.add_api_route("/programmatic", programmatic_handler, methods=["PUT"])
