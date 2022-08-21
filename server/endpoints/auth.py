from fastapi import APIRouter, Depends, HTTPException, status
from models.token import Token, Login
from repositories.users import UserRepository
from .depends import get_user_repository
from core.security import verify_password, create_access_token

router = APIRouter()

#Авторизация пользователя
@router.post('/', response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(login.email)
    if user is None and verify_password(login.password, user.hashed_password) == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')
    return Token(
        access_token=create_access_token({'sub': user.email}),
        token_type='Bearer'
    )