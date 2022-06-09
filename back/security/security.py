from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY= "62119020c607b830f8662605e312f4cc080e2dffc6ea874e9c0088f45af32d71"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 60

pwd_context= CryptContext(schemes= ["bcrypt"], deprecated= "auto")
oatuh2_scheme= OAuth2PasswordBearer(tokenUrl='login')

def verify_pwd(plain_pwd: str, hashed_pwd: str):
  return pwd_context.verify(plain_pwd, hashed_pwd)

def get_pwd_hash(pwd: str):
  return pwd_context.hash(pwd)

def create_token(data: dict, expires_delta: timedelta):
  to_encode = data.copy()
  expire = datetime.utcnow() + expires_delta
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def decode_token(token: str):
  payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  return payload.get('sub')