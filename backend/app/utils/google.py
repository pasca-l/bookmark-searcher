import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from google.auth.transport import requests
from google.oauth2 import id_token


@dataclass
class GoogleUser:
    id: str
    email: str


class GoogleUtils:
    def __init__(self) -> None:
        load_dotenv()
        self.GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")

    def get_google_user(self, token: str) -> GoogleUser:
        verification = id_token.verify_oauth2_token(
            token, requests.Request(), self.GOOGLE_CLIENT_ID
        )
        return self._parse_google_user(verification)

    def _parse_google_user(self, data: dict[str, Any]) -> GoogleUser:
        return GoogleUser(
            id=data["sub"],
            email=data["email"],
        )


def get_google_utils() -> GoogleUtils:
    return GoogleUtils()
