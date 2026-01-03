import pytest

from app.services.scraping import ScrapingService


@pytest.fixture
def scraping_service():
    return ScrapingService()


class TestScrapingService:
    @pytest.mark.parametrize(
        ["url", "expected"],
        [
            pytest.param(
                # simple page
                "https://example.com",
                None,
            ),
            pytest.param(
                # page with scripts and styles
                "https://github.com",
                None,
            ),
            pytest.param(
                # redirecting page
                "https://httpbin.dev/absolute-redirect/1",
                None,
            ),
            pytest.param(
                # non-existing page
                "https://this-domain-definitely-does-not-exist-12345.com",
                None,
                marks=pytest.mark.xfail,
            ),
        ]
    )
    @pytest.mark.anyio
    async def test__extract_content(self, scraping_service, url, expected):
        result = await scraping_service.extract_content(url)

        # verify object structure
        assert "title" in result
        assert "content" in result

        # verify content is cleaned
        assert "<script" not in result["content"]
        assert "<style" not in result["content"]
