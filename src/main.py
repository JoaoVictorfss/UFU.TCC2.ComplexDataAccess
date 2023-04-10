from domain.db.adapters.PgAdapter import PgAdapter
from domain.db.scripts.PostgreSqlScripts import PostgreSqlScripts

def main():
 configurePostgreSqlDatabase()

def configurePostgreSqlDatabase():
  commands = (
      PostgreSqlScripts.CREATE_TABLE_PATENT,
      PostgreSqlScripts.CREATE_TABLE_CITATION,
      PostgreSqlScripts.CREATE_INDEX_PATENT_ID,
      PostgreSqlScripts.CREATE_INDEX_PATENT_AUTHOR,
      PostgreSqlScripts.CREATE_INDEX_PATENT_NAME,
      PostgreSqlScripts.CREATE_INDEX_PATENT_REGISTERED_DATE
  )
  pgAdapter = PgAdapter()
  pgAdapter.executeDdlScripts(commands)
  pgAdapter.closeConnection()
  
main()