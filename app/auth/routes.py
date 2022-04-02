from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from .deps import get_current_active_user
from .schemas import (
    SignupSchema,
    SignupRespSchema,
    TokenSchema,
    UserSchema,
    VerifyCodeRequestSchema,
    VerifyCodeRespSchema,
    ResendCodeRespSchema,
    ResendCodeSchema,
)
from .services import AuthService

router = APIRouter(
    prefix="/auth.",
    tags=["auth", "user"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post("signup", response_model=SignupRespSchema)
async def signup_user(body: SignupSchema, auth_service: AuthService = Depends()):
    email = await auth_service.signup_user(
        email=body.email,
        pwd=body.password,
    )

    return {"email": email}


@router.post("login", response_model=TokenSchema)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    access_token, token_type = await auth_service.login_user(
        email=form_data.username,
        pwd=form_data.password,
    )

    return {"access_token": access_token, "token_type": token_type}


@router.get("me", response_model=UserSchema)
async def current_user(curr_user: UserSchema = Depends(get_current_active_user)):
    return curr_user


@router.post("verify_code", status_code=200, response_model=VerifyCodeRespSchema)
async def verify_code(
    body: VerifyCodeRequestSchema,
    auth_service: AuthService = Depends(),
):
    email = await auth_service.verify_code(
        email=body.email,
        code=body.code,
    )

    return {"email": email}


@router.post("resend_code", status_code=200, response_model=ResendCodeRespSchema)
async def resend_code(
    body: ResendCodeSchema,
    auth_service: AuthService = Depends(),
):
    email = await auth_service.resend_code(body.email)
    return {"email": email}
