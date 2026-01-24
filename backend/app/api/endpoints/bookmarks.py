from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.api.middleware.auth import get_current_user_id
from app.api.schemas.generated import Bookmark, Bookmarks
from app.repositories.bookmark import BookmarkRepository, new_bookmark_repository
from app.services.embedding import EmbeddingService, new_embedding_service
from app.services.scraping import ScrapingService, new_scraping_service

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])


@router.get("", response_model=Bookmarks)
async def get_bookmarks(
    user_id: UUID = Depends(get_current_user_id),
    bookmark_repo: BookmarkRepository = Depends(new_bookmark_repository),
):
    try:
        bookmarks = bookmark_repo.get_bookmarks_by_user_id(user_id)
        return Bookmarks(root=bookmarks)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failed to retrieve bookmarks: {str(e)}",
        )


@router.post("", response_model=Bookmark)
async def create_bookmark(
    url: str = Body(..., embed=True),
    user_id: UUID = Depends(get_current_user_id),
    scraping_service: ScrapingService = Depends(new_scraping_service),
    embedding_service: EmbeddingService = Depends(new_embedding_service),
    bookmark_repo: BookmarkRepository = Depends(new_bookmark_repository),
):
    try:
        can_scrape, reason = await scraping_service.can_scrape_url(url)
        if not can_scrape:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"cannot scrape this url: {reason}",
            )

        scraped_data = await scraping_service.extract_content(url)
        title = scraped_data["title"]
        content = scraped_data["content"]

        bookmark = bookmark_repo.create_bookmark(url=url, title=title)

        bookmark_repo.link_bookmark_to_user(user_id=user_id, bookmark_id=bookmark.id)

        embedding_service.store_bookmark_embedding(
            bookmark_id=bookmark.id, content=content
        )

        return bookmark

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failed to create bookmark: {str(e)}",
        )
