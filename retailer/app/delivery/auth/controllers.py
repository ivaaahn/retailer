from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.dto.signup import (
    SignupReqDTO,
    SignupRespDTO,
    TokenRespDTO,
    VerifyCodeReqDTO,
    VerifyCodeRespSchema,
    ResendCodeRespDTO,
    ResendCodeReqDTO,
)
from app.dto.user import UserRespDTO
from app.services import AuthService
from .deps import get_current_active_user

router = APIRouter(
    prefix="/auth",
    tags=["auth", "user"],
)


@router.post("/signup", response_model=SignupRespDTO)
async def signup_user(body: SignupReqDTO, auth_service: AuthService = Depends()):
    return await auth_service.signup_user(
        email=body.email,
        pwd=body.password,
    )


@router.post("/login", response_model=TokenRespDTO)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    access_token, token_type = await auth_service.login_user(
        email=form_data.username,
        pwd=form_data.password,
    )

    return {"access_token": access_token, "token_type": token_type}


@router.get("/me", response_model=UserRespDTO)
async def current_user(curr_user: UserRespDTO = Depends(get_current_active_user)):
    return curr_user


@router.post("/verify_code", status_code=200, response_model=VerifyCodeRespSchema)
async def verify_code(
    body: VerifyCodeReqDTO,
    auth_service: AuthService = Depends(),
):
    email = await auth_service.verify_code(
        email=body.email,
        code=body.code,
    )

    return {"email": email}


@router.post("/resend_code", status_code=200, response_model=ResendCodeRespDTO)
async def resend_code(
    body: ResendCodeReqDTO,
    auth_service: AuthService = Depends(),
):
    return await auth_service.resend_code(body.email)
