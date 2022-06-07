from decimal import Decimal
from pymongo import MongoClient

from .models import Product, User
from bson.objectid import ObjectId

URL= "mongodb://mongo:1234@localhost:27017"

class Mongo_db():
  def __init__(self, url):
    self.client= MongoClient(url)
    self.db= self.client['commerce']
    self.collection= self.db['products']

  def close(self):
    self.client.close()

  def convert_to_model(self, mongo_p:dict) -> Product:
    mongo_p['id']= str(mongo_p.get('_id'))
    mongo_p.pop('_id')
    mongo_p['price']= Decimal(str(mongo_p.get('price')))
    return Product(**mongo_p)
  
  def get_product_by_title(self, title: str):
    return self.collection.find_one({'title': title})

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

async def get_mongo():
  mongo_ins= Mongo_db(url= URL) 
  try:
    yield mongo_ins
  finally:
    mongo_ins.close()