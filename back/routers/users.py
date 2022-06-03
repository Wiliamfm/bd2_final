from fastapi import APIRouter, Form, status, HTTPException
from pydantic import EmailStr
from ..db.neo4j import PASSWORD, URL, USER, Neo4j

router= APIRouter(
  prefix= "/users"
)

neo4j_ins= Neo4j(url= URL, user= USER, password= PASSWORD)

@router.post("/", status_code= status.HTTP_201_CREATED)
async def create(username: str = Form(min_length= 3), password: str = Form(min_length= 4), email: EmailStr = Form(), full_name: str = Form(max_length= 100, min_length= 1)):
  r= neo4j_ins.create_client(username= username, password= password, email= email, full_name= full_name)
  if not r:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f'The username: {username} or email {email} already exists')
  return r