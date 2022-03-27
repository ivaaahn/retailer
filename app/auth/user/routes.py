from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .deps import get_current_active_user
from .schemas import SignupSchema, SignupRespSchema, TokenSchema, UserSchema
from .services import AuthUserService


router = APIRouter(
    prefix="/auth.",
    tags=["auth", "user"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post("signup", response_model=SignupRespSchema)
async def signup_user(body: SignupSchema, auth_service: AuthUserService = Depends()):
    email = await auth_service.signup_user(
        email=body.email,
        pwd=body.password,
    )

    return {"email": email}


@router.post("login", response_model=TokenSchema)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthUserService = Depends(),
):
    access_token, token_type = await auth_service.login_user(
        email=form_data.username,
        pwd=form_data.password,
    )

    return {"access_token": access_token, "token_type": token_type}


@router.get("me", response_model=UserSchema)
async def current_user(curr_user: UserSchema = Depends(get_current_active_user)):
    return curr_user


# @router.post("/auth.login", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
