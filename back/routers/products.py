from fastapi import APIRouter, Depends, Form, status, HTTPException
from ..security import security
from ..db.mongo import Mongo_db, get_mongo

router= APIRouter(
  prefix= "/products"
)

@router.post("/", status_code= status.HTTP_201_CREATED)
async def create(mongo: Mongo_db = Depends(get_mongo)):
  pass