from decimal import Decimal
from fastapi import APIRouter, Depends, Form, status, HTTPException
from pydantic import EmailStr

from ..db.neo4j import Neo4j, get_neo4j
from ..db.mongo import Mongo_db, get_mongo
from ..security import security
from ..db.models import Product, User_rol, Variant

router= APIRouter(
  prefix= "/vendors"
)

@router.post("/", status_code= status.HTTP_201_CREATED)
async def create(neo4j_ins : Neo4j = Depends(get_neo4j), username: str = Form(min_length= 3), password: str = Form(min_length= 4), email: EmailStr = Form(), full_name: str = Form(max_length= 100, min_length= 1)):
  r= neo4j_ins.create_vendor(username= username, password= security.get_pwd_hash(password), email= email, full_name= full_name)
  if not r:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f'The username: {username} or email {email} already exists')
  return r

@router.post("/{username}/products", status_code= status.HTTP_201_CREATED)
async def create_product(username: str, neo4j: Neo4j = Depends(get_neo4j), mongo: Mongo_db= Depends(get_mongo), title: str = Form(min_length= 5), category: str = Form(), price: Decimal= Form(gt= 0), description: str = Form()):
  vendor= neo4j.get_by_username(username= username)
  if not vendor:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The username: {username} do not exists!")
  if vendor.rol != User_rol.vendor:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f'The user {username} is not a Vendor')
  product= Product(vendor= vendor.id, title= title, category= category, price= price, description= description)
  product= mongo.create_product(product)
  if not product:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The product {title} already exists!")
  return product

@router.get("/{username}/products")
async def get_products(username: str, neo4j: Neo4j = Depends(get_neo4j), mongo: Mongo_db= Depends(get_mongo)):
  vendor= neo4j.get_by_username(username)
  if not vendor:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The username: {username} do not exists!")
  if vendor.rol != User_rol.vendor:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f'The user {username} is not a Vendor')
  products= mongo.get_products(vendor.id)
  return products
  
@router.put("/{username}/products", status_code= status.HTTP_202_ACCEPTED)
async def create_product(username: str, neo4j: Neo4j = Depends(get_neo4j), mongo: Mongo_db= Depends(get_mongo), id: str = Form(), title: str = Form(min_length= 5), category: str = Form(), price: Decimal= Form(gt= 0), description: str = Form()):
  vendor= neo4j.get_by_username(username= username)
  if not vendor:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The username: {username} do not exists!")
  if vendor.rol != User_rol.vendor:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f'The user {username} is not a Vendor')
  product= Product(id= id,vendor= vendor.id, title= title, category= category, price= price, description= description)
  product= mongo.update_product(product)
  if not product:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The product {title} already exists! or you do not have the right permissions")
  return product

@router.delete("/{username}/products", status_code= status.HTTP_202_ACCEPTED)
async def delete_product(username: str, neo4j: Neo4j = Depends(get_neo4j), mongo: Mongo_db = Depends(get_mongo), id: str = Form()):
  vendor= neo4j.get_by_username(username)
  if not vendor:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The username: {username} do not exists!")
  if vendor.rol != User_rol.vendor:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f'The user {username} is not a Vendor')
  product= mongo.delete_product(id, vendor)
  if not product:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The product was not delete")
  return product

@router.post("/{username}/products/{product_id}", status_code= status.HTTP_201_CREATED)
async def create_variant(username: str, product_id: str, neo4j: Neo4j = Depends(get_neo4j), mongo: Mongo_db = Depends(get_mongo), name: str = Form(min_length= 5), quantity: int = Form(gt= 0), description: str = Form()):
  vendor= neo4j.get_by_username(username)
  product= mongo.get_product_by_id(product_id)
  if not vendor:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The username: {username} do not exists!")
  if vendor.rol != User_rol.vendor:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f'The user {username} is not a Vendor')
  if not product:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The product {product_id} do not exists!")
  if product.vendor != vendor.id:
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f'The vendor {vendor.username} do not own the product {product.title}')
  variant= Variant(product= product.id, name= name, quantity= quantity, description= description)
  variant= mongo.create_variant(variant)
  if not variant:
    raise HTTPException(status_code= status.HTTP_200_OK, detail= f"The variant {name} already exists!")
  return variant