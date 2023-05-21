import psycopg2
from infra.io.logs.LogInConsole import LogInConsole as Log

class PgAdapter:
  def __init__(self, connStr):
    try:
      self.__conn = psycopg2.connect(connStr)
    except psycopg2.Error as error:
      Log.error(f"[PgAdapter] - An error occurred while trying to connect ~ Error: {error}")

  def executeDdls(self, ddls):
    try:
      cur = self.__conn.cursor()
      for ddl in ddls:
        Log.debug(f"[PgAdapter executeDdls] - Try to execute ddl {ddl}")
        cur.execute(ddl)
      self.__conn.commit()
      Log.information(f"[PgAdapter executeDdls] - the ddls were executed successfully")
    except psycopg2.Error as error:
      Log.error(f"[PgAdapter executeDdls] - An error occurred while trying to execute ddls ~ Error: {error}")
    finally:
        cur.close()
  
  def executeDml(self, cmd, params=None):
    try:
      Log.debug(f"[PgAdapter executeDml] - Try to execute dml {cmd} with params {params}")
      cur = self.__conn.cursor()
      cur.execute(cmd, params)
      self.__conn.commit()
      Log.information(f"[PgAdapter executeDml] - The dml was executed successfully")
    except psycopg2.Error as error:
      Log.error(f"[PgAdapter executeDml] - An error occurred while trying to execute dml ~ Error: {error}")
    finally:
        cur.close()
        
  def executeDql(self, cmd, params=None): 
    results = None
    
    try:
      Log.debug(f"[PgAdapter executeDql] - Try to execute dql {cmd} with params {params}")
      cur = self.__conn.cursor()
      cur.execute(cmd, params)
      results = cur.fetchall()
      Log.information(f"[PgAdapter executeDql] - The dql was executed successfully")
    except psycopg2.Error as error:
      Log.error(f"[PgAdapter executeDql] - An error occurred while trying to execute dql ~ Error: {error}")
    finally:
        cur.close()     
        return results

  def closeConnection(self):
      self.__conn.close()