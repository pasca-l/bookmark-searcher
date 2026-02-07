from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup


class ScrapingService:
    def __init__(self, timeout: float = 30.0, user_agent: str | None = None):
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.headers = {"User-Agent": self.user_agent}

        self._robots_cache: dict[str, RobotFileParser] = {}

    async def can_scrape_url(self, url: str) -> tuple[bool, str]:
        try:
            parsed_url = urlparse(url)

            if not parsed_url.scheme or parsed_url.scheme not in ["http", "https"]:
                return False, "invalid url: only http and https are supported"

            if not parsed_url.netloc:
                return False, "invalid url: no domain found"

            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            robots_url = urljoin(base_url, "/robots.txt")

            if base_url not in self._robots_cache:
                rp = RobotFileParser()
                rp.set_url(robots_url)

                try:
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        response = await client.get(robots_url, follow_redirects=True)

                        if response.status_code == 200:
                            rp.parse(response.text.splitlines())

                # if robots.txt is not accessible, assume scraping is allowed
                except httpx.HTTPError, httpx.TimeoutException:
                    pass

                self._robots_cache[base_url] = rp

            rp = self._robots_cache[base_url]
            if not rp.can_fetch(self.user_agent, url):
                return False, "scraping is disallowed by robots.txt for this url"

            return True, "url is scrapable"

        except Exception as e:
            return False, f"error validating url: {str(e)}"

    async def extract_content(self, url: str) -> dict[str, str]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url, headers=self.headers, follow_redirects=True
            )
            response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, "lxml")

        # get title from <title> tag or og:title
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        if not title:
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                content_attr = og_title["content"]
                if isinstance(content_attr, list):
                    title = content_attr[0].strip() if content_attr else ""
                else:
                    title = content_attr.strip()

        # remove non-visible elements (scripts, styles, etc.)
        for element in soup(["script", "style", "noscript", "meta", "link", "head"]):
            element.decompose()

        # get all visible text from the page
        content = soup.get_text(separator=" ", strip=True)

        # clean up whitespace (multiple spaces, newlines, tabs -> single space)
        content = " ".join(content.split())

        return {"title": title, "content": content}


def new_scraping_service() -> ScrapingService:
    return ScrapingService()
