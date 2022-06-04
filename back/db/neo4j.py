from neo4j import GraphDatabase
from .models import *

URL= 'bolt://localhost:7687'
USER= 'neo4j'
PASSWORD= '1234'

class Neo4j:
  def __init__(self, url, user, password):
    self.driver= GraphDatabase.driver(url, auth= (user, password))

  def close(self):
    self.driver.close()

  def _get_by_username(self, tx, username):
    query= (f'''
    MATCH (p:Person)
    WHERE p.username = '{username}'
    RETURN p
    ''')
    result= tx.run(query, username= username)
    return result.single()

  def get_by_username(self, username):
    with self.driver.session() as session:
      result= session.read_transaction(self._get_by_username, username)
      if result:
        if "Client" in result['p'].labels:
          return User(username= result['p']['username'], password= result['p']['password'], email= result['p']['email'], full_name= result['p']['full_name'], rol= User_rol.client)
        if "Vendor" in result['p'].labels:
          return User(username= result['p']['username'], password= result['p']['password'], email= result['p']['email'], full_name= result['p']['full_name'], rol= User_rol.vendor)
      return result

  def _get_by_email(self, tx, email):
    query= (f'''
    MATCH (p:Person)
    WHERE p.email = '{email}'
    RETURN p
    ''')
    result= tx.run(query, email= email)
    return result.single()

  def get_by_email(self, email):
    with self.driver.session() as session:
      result= session.read_transaction(self._get_by_email, email)
      return result
  
  def _create_client(self, tx, username, password, email, full_name):
    query= (f'''
    CREATE (c:Person:Client {{username: '{username}', password: '{password}', email: '{email}', full_name: '{full_name}'}})
    RETURN c
    ''')
    result= tx.run(query, username= username, password= password, email= email, full_name= full_name)
    return result.single()

  def create_client(self, username, password, email, full_name):
    with self.driver.session() as session:
      if(self.get_by_username(username= username) == None and self.get_by_email(email= email) == None):
        result= session.write_transaction(self._create_client, username, password, email, full_name)
        return User(username= result['c']['username'], password= result['c']['password'], email= result['c']['email'], full_name= result['c']['full_name'], rol= User_rol.client)
      return False
  
  def _create_vendor(self, tx, username, password, email, full_name):
    query= (f'''
    CREATE (v:Person:Vendor {{username: '{username}', password: '{password}', email: '{email}', full_name: '{full_name}'}})
    RETURN v
    ''')
    result= tx.run(query, username= username, password= password, email= email, full_name= full_name)
    return result.single()

  def create_vendor(self, username, password, email, full_name):
    with self.driver.session() as session:
      if(self.get_by_username(username= username) == None and self.get_by_email(email= email) == None):
        result= session.write_transaction(self._create_vendor, username, password, email, full_name)
        return User(username= result['v']['username'], password= result['v']['password'], email= result['v']['email'], full_name= result['v']['full_name'], rol= User_rol.vendor)
      return False

async def get_neo4j():
  neo4j_ins= Neo4j(url= URL, user= USER, password= PASSWORD) 
  try:
    yield neo4j_ins
  finally:
    neo4j_ins.close()