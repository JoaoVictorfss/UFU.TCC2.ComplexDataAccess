from neo4j import GraphDatabase
from config import Neo4jConfig

class Neo4jAdpater:
  def __init__(self):
    #TO DO recuperar user, uri e password do settings.json
    self.__driver = GraphDatabase.driver(
        Neo4jConfig.uri, auth=(Neo4jConfig.user, Neo4jConfig.password))
  
  def closeConnection(self):
    self.__driver.close()
