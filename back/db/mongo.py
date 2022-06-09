from typing import Union
from decimal import Decimal
from pymongo import MongoClient

from .models import Product, User, Variant
from bson.objectid import ObjectId

URL= "mongodb://mongo:1234@localhost:27017"

class Mongo_db():
  def __init__(self, url):
    self.client= MongoClient(url)
    self.db= self.client['commerce']
    self.collection= self.db['products']
    self.variants_collection= self.db['variants']

  def close(self):
    self.client.close()

  def convert_to_model(self, mongo_p:dict) -> Product:
    mongo_p['id']= str(mongo_p.get('_id'))
    mongo_p.pop('_id')
    mongo_p['price']= Decimal(str(mongo_p.get('price')))
    return Product(**mongo_p)

  def convert_to_variant(self, mongo_v: dict) -> Variant:
    mongo_v['id']= str(mongo_v.get('_id'))
    mongo_v.pop('_id')
    mongo_v['product']= str(mongo_v.get('product'))
    return Variant(**mongo_v)
  
  def get_product_by_title(self, title: str) -> Product:
    p= self.collection.find_one({'title': title})
    if p:
      return self.convert_to_model(p)
  
  def get_product_by_id(self, id: str) -> Union[None, Product]:
    p= self.collection.find_one({'_id': ObjectId(id)})
    if p:
      return self.convert_to_model(p)

  def get_product_by_id_2(self, id: str) -> Union[None, Product]:
    p= self.collection.find_one({'_id': ObjectId(id)})
    vs= self.variants_collection.find({'product': ObjectId(id)})
    if p:
      if vs:
        variants: list[Variant]= []
        for v in vs:
          variants.append(self.convert_to_variant(v))
        product= self.convert_to_model(p)
        product.variants= variants
      return product

  def create_product(self, product: Product) -> Product:
    if self.get_product_by_title(product.title):
      return False
    p_id= self.collection.insert_one(product.convert_to_mongo()).inserted_id
    p= self.collection.find_one({'_id': p_id})
    return self.convert_to_model(p)

  def get_products(self, vendor_id: int) -> list[Product]:
    products= [self.convert_to_model(p) for p in self.collection.find({'vendor': vendor_id})]
    return products

  def update_product(self, product: Product) -> Product:
    p= self.convert_to_model(self.collection.find_one({'_id': product.convert_to_mongo().get('_id')}))
    if p.title != product.title and self.get_product_by_title(product.title):
      return False
    if p.vendor != product.vendor:
      return False
    if self.collection.replace_one(filter= {'_id': ObjectId(product.id)}, replacement= product.convert_to_mongo()).raw_result.get('updatedExisting'):
      return self.convert_to_model(self.collection.find_one({'_id': ObjectId(product.id)}))

  def delete_product(self, id: str, vendor: User) -> Product:
    p= self.collection.find_one({'_id': ObjectId(id)})
    if not p or p.get('vendor') != vendor.id:
      return False
    if self.collection.delete_one({'_id': p.get('_id')}).raw_result.get('ok') != 1:
      return False
    return self.convert_to_model(p)

  def get_all_products(self) -> list[Product]:
    return [self.convert_to_model(p) for p in self.collection.find()]

  def get_variant_by_id(self, id: str) -> Union[None, Variant]:
    v= self.variants_collection.find_one({'_id': ObjectId(id)})
    if v:
      return self.convert_to_variant(v)

  def get_variant_by_name(self, product_id: str, name: str) -> Union[None, Variant]:
    vs= self.variants_collection.find({'product': ObjectId(product_id)})
    for v in vs:
      if v.get('name') == name:
        return self.convert_to_variant(v)

  def create_variant(self, variant: Variant) -> Variant:
    if self.get_variant_by_name(variant.product, variant.name):
      return False
    v_id= self.variants_collection.insert_one(variant.convert_to_mongo()).inserted_id
    return self.get_variant_by_id(v_id)

  def update_variant(self, variant: Variant) -> Variant:
    v= self.variants_collection.find_one({'_id': ObjectId(variant.id)})
    if v and v.get('name') != variant.name and self.get_variant_by_name(product_id= variant.product, name= variant.name):
      return False
    if v.get('product') != ObjectId(variant.product):
      print(variant.convert_to_mongo())
      return False
    if self.variants_collection.replace_one(filter= {'_id': ObjectId(variant.id)}, replacement= variant.convert_to_mongo()).raw_result.get('updatedExisting'):
      print(self.variants_collection.find_one({'_id': ObjectId(variant.id)}))
      return self.convert_to_variant(self.variants_collection.find_one({'_id': ObjectId(variant.id)}))

async def get_mongo():
  mongo_ins= Mongo_db(url= URL) 
  try:
    yield mongo_ins
  finally:
    mongo_ins.close()