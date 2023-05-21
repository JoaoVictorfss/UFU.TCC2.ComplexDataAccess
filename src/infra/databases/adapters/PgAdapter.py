import psycopg2

class PgAdapter:
  def __init__(self, connStr):
    self.__conn = psycopg2.connect(connStr)

  def executeDdls(self, ddls):
    cur = self.__conn.cursor()
    for ddl in ddls:
      cur.execute(ddl)    
    self.__conn.commit()
    cur.close()

  def executeDml(self, cmd, params=None):
    cur = self.__conn.cursor()
    cur.execute(cmd, params)
    self.__conn.commit()
    cur.close()

  def executeDql(self, cmd, params=None): 
    cur = self.__conn.cursor()
    cur.execute(cmd, params)  
    results = cur.fetchall()
    cur.close()

    return results

  def closeConnection(self):
      self.__conn.close()