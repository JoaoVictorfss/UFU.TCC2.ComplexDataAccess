from neo4j import GraphDatabase

class Neo4jAdpater:
  def __init__(self, uri, user, password):
    self.__driver = GraphDatabase.driver(
      uri, auth=(user, password))
  
  def executeQueries(self, queries):
    session = self.__driver.session()   
    for query in queries:
       session.run(query)   
    session.close()
    
  def executeTransaction(self, query, rows=None):
    session = self.__driver.session()    
    results = list(session.write_transaction(query, rows))
    session.close()
    
    return results
        
  def closeConnection(self):
    self.__driver.close()