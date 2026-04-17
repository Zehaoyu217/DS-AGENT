from fastapi import APIRouter

router = APIRouter(prefix="/items")


@router.get("/list")
def list_items():
    return []


@router.post("/create")
def create_item(payload: dict):
    return payload


@router.delete("/{item_id}")
async def delete_item(item_id: str):
    return None
