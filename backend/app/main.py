import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Bookmark Searcher API",
    description="A personal search engine for bookmarked webpages using RAG",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Bookmark Searcher API", "status": "running"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
