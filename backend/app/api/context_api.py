from fastapi import APIRouter

from app.context.manager import ContextManager

router = APIRouter()

# In-memory context manager (will be per-session in future)
_context_manager = ContextManager()


def get_context_manager() -> ContextManager:
    return _context_manager


@router.get("/api/context")
async def get_context() -> dict:
    return get_context_manager().snapshot()
