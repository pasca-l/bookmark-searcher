import uvicorn
from fastapi import FastAPI

from app.api.endpoints import bookmarks, root

app = FastAPI(
    title="Bookmark Searcher API",
    description="A personal search engine for bookmarked webpages using RAG",
    version="0.1.0",
)

app.include_router(root.router)
app.include_router(bookmarks.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
