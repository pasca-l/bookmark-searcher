import httpx
from bs4 import BeautifulSoup
from readability import Document  # type: ignore


class ScrapingService:
    def __init__(self, timeout: float = 30.0, user_agent: str | None = None):
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.headers = {"User-Agent": self.user_agent}

    async def extract_content(self, url: str) -> dict[str, str]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url, headers=self.headers, follow_redirects=True
            )
            response.raise_for_status()

        doc = Document(response.text)
        title = doc.title()
        summary = doc.summary()

        soup = BeautifulSoup(summary, "lxml")
        for element in soup(["script", "style", "nav", "footer", "aside"]):
            element.decompose()
        content = soup.get_text(separator=" ", strip=True)

        return {"title": title, "content": content}
