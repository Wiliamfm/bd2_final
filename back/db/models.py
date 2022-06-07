import decimal
from enum import Enum
from typing import Union
from bson import ObjectId
from pydantic import BaseModel, EmailStr
from bson.decimal128 import Decimal128

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"

class User_rol(Enum):
  client= "client"
  vendor= "vendor"

class User(BaseModel):
  id: Union[int, None]
  username: str
  password: str
  email: EmailStr
  full_name: str
  rol: User_rol

class Product(BaseModel):
  id: Union[str, None]
  vendor: int
  title: str
  category: str
  price: decimal.Decimal
  description: str

  def convert_to_mongo(self) -> dict:
    p= self.dict()
    p['price']= Decimal128(str(self.price))
    p['_id']= ObjectId(p.get('id'))
    p.pop('id')
    return p

class Variant(BaseModel):
  id: Union[None, str]
  product: str
  name: str
  quantity: int
  path_photos: Union[None, list[str]]
  description: str

  def convert_to_mongo(self) -> dict:
    v= self.dict()
    v['_id']= ObjectId(v.get('id'))
    v.pop('id')
    v['product']= ObjectId(v.get('product'))
    return v