import decimal
from enum import Enum
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"

class User_rol(Enum):
  client= "client"
  vendor= "vendor"

class User(BaseModel):
  username: str
  password: str
  email: EmailStr
  full_name: str
  rol: User_rol

class Product(BaseModel):
  vendor: User
  name: str
  category: str
  price: decimal.Decimal
  description: str

class Variant(BaseModel):
  product: Product
  name: str
  quantity: int
  path_photos: list[str]
  description: str