import datetime
from xmlrpc.client import Boolean
from passlib.context import CryptContext
from jose import jwt
from .config import ACCESS_TOKEN_EXPIRE_TIME, SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

def create_access_token(data: dict) -> str:
    token_encode = data.copy()
    token_encode.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)})
    token = jwt.encode(token_encode,SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str):
    try:
        decoded_jwt = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
    except:
        return None
    return decoded_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid auth token')
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.credentials is None:
                raise exp
            return credentials.credentials
        else:
            raise exp