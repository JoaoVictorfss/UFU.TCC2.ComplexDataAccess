from neo4j import GraphDatabase
class Neo4jAdpater:
  def __init__(self):
    self.__driver = GraphDatabase.driver(
      "", auth=("", ""))
  
  def closeConnection(self):
    self.__driver.close()
