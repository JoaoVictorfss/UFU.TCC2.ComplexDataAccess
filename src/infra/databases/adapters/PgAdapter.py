import psycopg2
from infra.io.logs.LogInConsole import LogInConsole as Log

#Driver for PostgreSql
class PgAdapter:
  def __init__(self, connStr):
    try:
      #Starts a new connection
      self.__conn = psycopg2.connect(connStr)
    except Exception as error:
      Log.error(f"[PgAdapter] - An error occurred while trying to connect ~ Error: {error}")

  #Executes many ddls
  def executeDdls(self, ddls):
    try:
      cur = self.__conn.cursor()
      
      for ddl in ddls:
        Log.debug(f"[PgAdapter executeDdls] - Try to execute ddl {ddl}")
        cur.execute(ddl)
      
      self.__conn.commit()
      Log.information(f"[PgAdapter executeDdls] - the ddls were executed successfully")
    except Exception as error:
      Log.error(f"[PgAdapter executeDdls] - An error occurred while trying to execute ddls ~ Error: {error}")
    finally:
        cur.close()
  
  #Executes a sigle dml
  def executeDml(self, cmd, params=None):
    try:
      Log.debug(f"[PgAdapter executeDml] - Try to execute dml {cmd} with params {params}")
      
      cur = self.__conn.cursor()
      cur.execute(cmd, params)
      self.__conn.commit()
      
      Log.information(f"[PgAdapter executeDml] - The dml was executed successfully")
    except Exception as error:
      Log.error(f"[PgAdapter executeDml] - An error occurred while trying to execute dml ~ Error: {error}")
    finally:
        cur.close()
  
  #Executes a sigle dql
  def executeDql(self, cmd, params=None):
    records = []     
    
    try:
      Log.debug(f"[PgAdapter executeDql] - Try to execute dql {cmd} with params {params}")
      
      cur = self.__conn.cursor()
      cur.execute(cmd, params)
      records = cur.fetchall()
      
      Log.debug(f"[PgAdapter executeDql] - {len(records)} records found")
      Log.information(f"[PgAdapter executeDql] - The dql was executed successfully")
    except Exception as error:
      Log.error(f"[PgAdapter executeDql] - An error occurred while trying to execute dql ~ Error: {error}")
    finally:
        cur.close() 
        return records

  def closeConnection(self):
      self.__conn.close()