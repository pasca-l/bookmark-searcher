import os
from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import UUID

import jwt
from fastapi import Response


class AuthUtils:
    def __init__(self) -> None:
        self.jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
        self.jwt_algorithm: str = "HS256"
        self.jwt_expiration_min: int = 30

        self.cookie_name: str = "auth_token"
        self.cookie_httponly: bool = True
        self.cookie_secure: bool = os.getenv("ENVIRONMENT", "dev") == "prod"
        self.cookie_samesite: Literal["lax", "strict", "none"] = "lax"

    def create_access_token(self, user_id: UUID) -> str:
        payload = {
            "user_id": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=self.jwt_expiration_min),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

    def decode_access_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])

    def set_auth_cookie(self, response: Response, token: str) -> Response:
        response.set_cookie(
            key=self.cookie_name,
            value=token,
            httponly=self.cookie_httponly,
            secure=self.cookie_secure,
            samesite=self.cookie_samesite,
            max_age=self.jwt_expiration_min * 60,
        )
        return response

    def delete_auth_cookie(self, response: Response) -> Response:
        response.delete_cookie(
            key=self.cookie_name,
            httponly=self.cookie_httponly,
            secure=self.cookie_secure,
            samesite=self.cookie_samesite,
        )
        return response


def get_auth_utils() -> AuthUtils:
    return AuthUtils()
