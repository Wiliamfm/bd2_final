from decimal import Decimal
from fastapi import APIRouter, Depends, Form, status, HTTPException
from pydantic import EmailStr

from ..db.postgres import Postgres, get_postgres
from ..db.neo4j import Neo4j, get_neo4j
from ..db.mongo import Mongo_db, get_mongo
from ..security import security
from ..db.models import Bill, Bill_detail, Items, Item, Variant

router= APIRouter(
  prefix= "/users"
)

@router.post("/", status_code= status.HTTP_201_CREATED)
async def create(neo4j_ins : Neo4j = Depends(get_neo4j), username: str = Form(min_length= 3), password: str = Form(min_length= 4), email: EmailStr = Form(), full_name: str = Form(max_length= 100, min_length= 1)):
  r= neo4j_ins.create_client(username= username, password= security.get_pwd_hash(password), email= email, full_name= full_name)
  if not r:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f'The username: {username} or email {email} already exists')
  return r

@router.post("/buy", status_code= status.HTTP_202_ACCEPTED)
async def buy_product(items: Items, neo4j: Neo4j = Depends(get_neo4j), mongo: Mongo_db = Depends(get_mongo), token: str = Depends(security.oatuh2_scheme), postgres: Postgres = Depends(get_postgres)):
  user= neo4j.get_by_username(security.decode_token(token))
  if not user:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f"The user do not exists!")
  variants: list[Variant]= []
  total_price: Decimal= 0
  bills: list[Bill_detail]= []
  for item in items.items:
    v= mongo.get_variant_by_id(item.variant_id)
    if v and v.quantity >= item.quantity and item.quantity > 0:
      product= mongo.get_product_by_id(v.product)
      if product:
        variants.append(v)
        price= product.price * item.quantity
        total_price= total_price + price
        bills.append(Bill_detail(variant= item.variant_id, quantity= item.quantity, unit_price= product.price, price= price, vendor= product.vendor))
      else:
        pass #Variant not associated to a product
    else:
      pass #Variant not found or has a greather qty
  bill= Bill(client= user.id, address= "", total_price= total_price)
  if not postgres.create_bill(bill):
    raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"The bill could not be create :c")
  return variants