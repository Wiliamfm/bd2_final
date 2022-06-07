from datetime import timedelta
from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .db.models import Token
from .routers import users, vendors, products
from .db.neo4j import Neo4j, get_neo4j
from .security import security

app = FastAPI()

oatuh2_scheme= OAuth2PasswordBearer(tokenUrl='login')

app.include_router(users.router)
app.include_router(vendors.router)
app.include_router(products.router)

@app.post("/login", status_code= status.HTTP_202_ACCEPTED)
async def login(neo4j_ins: Neo4j = Depends(get_neo4j), form_data : OAuth2PasswordRequestForm = Depends()):
  user= neo4j_ins.get_by_username(form_data.username)
  if not user:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The username {form_data.username} do not exists!")
  if not security.verify_pwd(form_data.password, user.password):
    raise HTTPException(status_code= status.HTTP_200_OK, detail= "The password is wrong!")
  access_token_expires= timedelta(minutes= security.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token= security.create_token(data= {'sub': user.username}, expires_delta= access_token_expires)
  return Token(access_token= access_token)

@app.get("/me")
async def me(token: str = Depends(oatuh2_scheme), neo4j: Neo4j = Depends(oatuh2_scheme)):
  user= neo4j.get_by_username(security.decode_token(token= token))
  if not user:
    raise HTTPException(status_code= status.HTTP_200_OK, detail='The credential are wrong!')
  return user