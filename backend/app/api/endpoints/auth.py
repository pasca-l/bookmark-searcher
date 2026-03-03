from fastapi import APIRouter, Body, Depends, HTTPException, Response, status

from app.api.schemas.generated import AuthToken
from app.repositories.user import UserRepository, new_user_repository
from app.utils.auth import AuthUtils, get_auth_utils
from app.utils.password import PasswordUtils, get_password_utils

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    auth_utils: AuthUtils = Depends(get_auth_utils),
    user_repo: UserRepository = Depends(new_user_repository),
    password_utils: PasswordUtils = Depends(get_password_utils),
    response: Response = None,
):
    try:
        existing_user = user_repo.get_user_by_username(username)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username already exists",
            )

        if len(username) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username must be at least 3 characters",
            )
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password must be at least 8 characters",
            )

        print(f"Registering user: {username}")  # Debug log
        print(
            f"Password type: {type(password)}, length: {len(password)}, value: {password!r}"
        )
        print(f"Password bytes length: {len(password.encode('utf-8'))}")

        password_hash = password_utils.hash_password(password)
        print(
            f"Hash type: {type(password_hash)}, length: {len(password_hash)}, value: {password_hash!r}"
        )
        user_id = user_repo.create_user(username=username, password=password_hash)

        jwt_token = auth_utils.create_access_token(user_id=user_id)
        auth_utils.set_auth_cookie(response, jwt_token)

        return AuthToken(token=jwt_token)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"registration failed: {str(e)}",
        )


@router.post("/login")
async def login(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    auth_utils: AuthUtils = Depends(get_auth_utils),
    user_repo: UserRepository = Depends(new_user_repository),
    password_utils: PasswordUtils = Depends(get_password_utils),
    response: Response = None,
):
    try:
        user = user_repo.get_user_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid username or password",
            )

        if not password_utils.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid username or password",
            )

        jwt_token = auth_utils.create_access_token(user_id=user.id)
        auth_utils.set_auth_cookie(response, jwt_token)

        return AuthToken(token=jwt_token)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"authentication failed: {str(e)}",
        )


@router.post("/logout")
async def logout(
    response: Response = None,
    auth_utils: AuthUtils = Depends(get_auth_utils),
):
    auth_utils.delete_auth_cookie(response)

    return None
