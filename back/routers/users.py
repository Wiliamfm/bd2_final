from fastapi import APIRouter, Depends, Form, status, HTTPException
from pydantic import EmailStr
from ..db.neo4j import Neo4j, get_neo4j
from ..security import security

router= APIRouter(
  prefix= "/users"
)

@router.post("/", status_code= status.HTTP_201_CREATED)
async def create(neo4j_ins : Neo4j = Depends(get_neo4j), username: str = Form(min_length= 3), password: str = Form(min_length= 4), email: EmailStr = Form(), full_name: str = Form(max_length= 100, min_length= 1)):
  r= neo4j_ins.create_client(username= username, password= security.get_pwd_hash(password), email= email, full_name= full_name)
  if not r:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f'The username: {username} or email {email} already exists')
  return r