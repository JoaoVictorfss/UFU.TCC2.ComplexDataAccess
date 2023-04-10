from domain.db.adapters.PgAdapter import PgAdapter
from domain.db.scripts.PostgreSqlScripts import PostgreSqlScripts
from domain.config.Settings import Settings
from utils.FakerUtils import FakerUtils

settings = Settings()

def main():
 createPostgreSqlDatabase()
 #createNeo4jDatabase()
 dataLoad()

def createPostgreSqlDatabase():
  commands = (
      PostgreSqlScripts.CREATE_TABLE_PATENT,
      PostgreSqlScripts.CREATE_TABLE_CITATION,
      PostgreSqlScripts.CREATE_INDEX_PATENT_ID,
      PostgreSqlScripts.CREATE_INDEX_PATENT_AUTHOR,
      PostgreSqlScripts.CREATE_INDEX_PATENT_CLASSIFICATION,
      PostgreSqlScripts.CREATE_INDEX_PATENT_REGISTERED_DATE
  )
  pgAdapter = PgAdapter()
  pgAdapter.executeDdlScripts(commands)
  pgAdapter.closeConnection()

def dataLoad():  
  #TO DO deixar de forma paralela
  
  authors = FakerUtils.generateUniqueFirstNames(settings.DATA_TOTAL)
  classifications = FakerUtils.generateUsPatentClassifications(settings.DATA_TOTAL)
  descriptions = FakerUtils.generateDescriptions(settings.DATA_TOTAL)
  registratiionDatetimes = FakerUtils.generateDateTimes(settings.DATA_TOTAL)
  
  #TO DO popular bancos
    
main()