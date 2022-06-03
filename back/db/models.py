import decimal
from pydantic import BaseModel, EmailStr

class User(BaseModel):
  username: str
  password: str
  email: EmailStr
  full_name: str
  rol: str

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