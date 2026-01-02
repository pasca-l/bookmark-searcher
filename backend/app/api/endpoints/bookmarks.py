from fastapi import APIRouter, Body

from app.api.schemas.generated import Bookmark, Bookmarks

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])


@router.get("", response_model=Bookmarks)
async def get_bookmarks():
    return Bookmarks()


@router.post("", response_model=Bookmark)
async def create_bookmark(url: str = Body(...)):
    return Bookmark.model_validate({"id": 1, "url": "https://example.com"})
