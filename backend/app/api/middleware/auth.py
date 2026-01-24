from uuid import UUID

import jwt
from fastapi import Cookie, Depends, HTTPException, status

from app.utils.auth import AuthUtils, get_auth_utils


def get_current_user_id(
    auth_token: str | None = Cookie(None, alias="auth_token"),
    auth_utils: AuthUtils = Depends(get_auth_utils),
) -> UUID:
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )

    try:
        payload = auth_utils.decode_access_token(auth_token)
        user_id_str = payload.get("user_id")

        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token payload",
            )

        return UUID(user_id_str)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid user ID in token",
        )
