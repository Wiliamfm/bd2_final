from fastapi import APIRouter, Depends, Form, status, HTTPException
from ..security import security
from ..db.mongo import Mongo_db, get_mongo

router= APIRouter(
  prefix= "/products"
)

@router.get("/")
async def get_all(mongo: Mongo_db = Depends(get_mongo)):
  return mongo.get_all_products()