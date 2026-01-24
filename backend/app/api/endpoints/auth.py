from fastapi import APIRouter, Body, Depends, HTTPException, Response

from app.repositories.user import UserRepository, new_user_repository
from app.utils.auth import AuthUtils, get_auth_utils
from app.utils.google import GoogleUtils, get_google_utils

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def google_auth(
    token: str = Body(..., embed=True),
    response: Response = Response(),
    auth_utils: AuthUtils = Depends(get_auth_utils),
    user_repo: UserRepository = Depends(new_user_repository),
    google_utils: GoogleUtils = Depends(get_google_utils),
):
    try:
        google_user = google_utils.get_google_user(token)

        user = user_repo.get_user(google_user.id)
        if user is None:
            user_id = user_repo.create_user(
                google_id=google_user.id, email=google_user.email
            )
        else:
            user_id = user.id

        jwt_token = auth_utils.create_access_token(user_id=user_id)
        auth_utils.set_auth_cookie(response, jwt_token)

        return {
            "message": "successfully authenticated",
            "user": {"id": str(user_id), "email": google_user.email},
        }

    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"invalid Google token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"authentication failed: {str(e)}")


@router.post("/logout")
async def logout(
    response: Response,
    auth_utils: AuthUtils = Depends(get_auth_utils),
):
    auth_utils.delete_auth_cookie(response)

    return {"message": "successfully logged out"}
