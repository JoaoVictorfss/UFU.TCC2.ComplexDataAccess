import psycopg2

class PgAdapter:
  def __init__(self):
    self.__driver = psycopg2.connect("")

  def executeDdlScripts(self, ddls):
    cur = self.__driver.cursor()
    for ddl in ddls:
      cur.execute(ddl)    
    cur.close()
    self.__driver.commit()

  def executeDmlScripts(self, cmd, params=None):
    self.__execute(cmd, False, params)

  def executeDqlScripts(self, cmd, params=None):
    return self.__execute(cmd, True, params)

  def closeConnection(self):
      self.__driver.close()
      
  def __execute(self, cmd, shouldReturn=False, params=None):
    results = None

    cur = self.__driver.cursor()
    cur.execute(cmd, params)

    if shouldReturn:
      results = cur.fetchall()

    cur.close()

    return results
