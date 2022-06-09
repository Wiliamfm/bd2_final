from decimal import Decimal
from peewee import *
from .models import Bill as Bill_model, Bill_detail as Bill_detail_model 

db= PostgresqlDatabase(database= 'commerce', host='localhost', port="5432", user="postgres", password="1234")

class Bill(Model):
  id= AutoField(primary_key= True)
  client= IntegerField()
  total_price= DecimalField()
  address: CharField()

  class Meta:
    database= db

class Bill_detail(Model):
  id= AutoField(primary_key= True)
  bill= ForeignKeyField(model= Bill)
  variant= CharField()
  quantity= IntegerField()
  unit_price= DecimalField()
  price= DecimalField()

  class Meta:
    database= db

class Postgres():
  def __init__(self, db: PostgresqlDatabase) -> None:
    self.db= db
    self.db.connect()
    self.create_tables()

  def create_tables(self): 
    with self.db:
      self.db.create_tables([Bill, Bill_detail])
  
  def close(self) -> None:
    self.db.close()

  def create_bill(self, bill: Bill_model) -> Bill_model:
    try:
      b= Bill(client= bill.client, total_price= bill.total_price, address= bill.address)
      b.save()
      return True
    except:
      return False

  def create_bill_detail(self, bill_detail: Bill_detail_model) -> Bill_detail_model:
    pass

def get_postgres() -> Postgres:
  postgres= Postgres(db)
  try:
    yield postgres
  finally:
    postgres.close()