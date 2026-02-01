import json
import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = time.time()
        response = await call_next(request)
        response_time = time.time() - start

        log_message = (
            f'"{request.method} {request.url.path}" {response.status_code}'
            f" in {response_time:.4f}s"
        )

        # extract error detail from response body
        if response.status_code >= 400:
            response_body = b""
            async for chunk in response.body_iterator:  # type: ignore[attr-defined]
                response_body += chunk

            try:
                error_data = json.loads(response_body.decode())
                error_detail = error_data.get("detail", "")
                if error_detail:
                    log_message += f" - {error_detail}"
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

            # recreate response as it is iterated and exhausted
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        logger.info(log_message)
        return response
