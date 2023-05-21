from neo4j import GraphDatabase
from infra.io.logs.LogInConsole import LogInConsole as Log

class Neo4jAdpater:
  def __init__(self, uri, user, password):
    try:
      self.__driver = GraphDatabase.driver(uri, auth=(user, password)) 
    except Exception as error:
      Log.error(f"[Neo4jAdpater] - An error occurred while trying to connect ~ Error: {error}")
  
  def executeQuery(self, query, params=None):
    records = None
    try:
      Log.debug(f"[Neo4jAdpater executeQuery] Try to execute query {query} with params {params}")
      session = self.__driver.session()
      result = session.run(query, params)
      records = result.data()
      Log.debug(f"[Neo4jAdpater executeQuery] - {len(records)} records found")
      Log.information(f"[Neo4jAdpater executeQuery] - The query was executed successfully")
    except Exception as error:
      Log.error(f"[Neo4jAdpater executeQuery] - An error occurred while trying to execute query ~ Error: {error}")
    finally:
      session.close()
      return records
      
  def executeQueries(self, queries):
    try:    
      Log.debug(f"[Neo4jAdpater executeQueries] Try to execute queries {queries}")
      session = self.__driver.session()   
      for query in queries:
        session.run(query)  
      Log.information(f"[Neo4jAdpater executeQueries] - The queries was executed successfully")
    except Exception as error:
      Log.error(f"[Neo4jAdpater executeQueries] - An error occurred while trying to execute queries ~ Error: {error}")
    finally:
      session.close()
    
  def executeTransaction(self, query, rows=None):
    try:    
      Log.debug(f"[Neo4jAdpater executeTransaction] Try to execute transaction {query} with rows {rows}")
      session = self.__driver.session()  
      
      def transaction(tx):
          result = tx.run(query, rows=rows) if rows else tx.run(query)
          return result.single()
        
      session.write_transaction(transaction)
    except Exception as error:
      Log.error(f"[Neo4jAdpater executeTransaction] - An error occurred while trying to execute transaction ~ Error: {error}")  
    finally:
      session.close()
            
  def closeConnection(self):
    self.__driver.close()