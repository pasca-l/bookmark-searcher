from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.middleware.auth import get_current_user_id

router = APIRouter(prefix="", tags=["root"])


@router.get("/")
async def root():
    return {"message": "public root path", "authenticated": False}


@router.get("/private")
async def private_route(user_id: UUID = Depends(get_current_user_id)):
    return {
        "message": "private root path",
        "user_id": str(user_id),
        "authenticated": True,
    }
