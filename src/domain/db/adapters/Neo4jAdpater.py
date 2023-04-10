from neo4j import GraphDatabase

class Neo4jAdpater:
  def __init__(self, uri, user, password):
    self.__driver = GraphDatabase.driver(
      uri, auth=(user, password))
  
  def closeConnection(self):
    self.__driver.close()
