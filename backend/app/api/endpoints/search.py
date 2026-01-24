from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel

from app.api.middleware.auth import get_current_user_id
from app.api.schemas.generated import Bookmark
from app.services.embedding import EmbeddingService, new_embedding_service

router = APIRouter(prefix="/search", tags=["search"])


class SearchResult(BaseModel):
    bookmark: Bookmark
    similarity: float
    chunk_content: str


@router.post("", response_model=list[SearchResult])
async def search_bookmarks(
    query: str = Body(..., embed=True),
    user_id: UUID = Depends(get_current_user_id),
    embedding_service: EmbeddingService = Depends(new_embedding_service),
):
    try:
        if not query or not query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="query cannot be empty",
            )

        search_results = embedding_service.search_bookmark_embedding(
            user_id=user_id, query=query.strip(), limit=10
        )

        results = [
            SearchResult(
                bookmark=Bookmark(
                    id=result["id"],
                    url=result["url"],
                    title=result["title"],
                ),
                similarity=result["similarity"],
                chunk_content=result["content"],
            )
            for result in search_results
        ]

        return results

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failed to search bookmarks: {str(e)}",
        )
