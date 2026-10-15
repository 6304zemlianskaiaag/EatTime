# app/api/auth.py
# HTTP-роутер для регистрации и логина

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_user_service
from app.services.user import UserService
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import Token
from app.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register", response_model=UserRead, status_code=201)
def register(data: UserCreate, service: UserService = Depends(get_user_service),):
    try:
        return service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    user = service.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )
    token = create_access_token({"sub": str(user.id), "log": str(user.email)})
    return {"access_token": token, "token_type": "bearer", "log": str(user.email)}