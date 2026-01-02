from fastapi import APIRouter

from app.api.schemas.generated import BookmarkQuery, Bookmarks

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=Bookmarks)
async def search_bookmarks(query: BookmarkQuery):
    return Bookmarks(root=[])
