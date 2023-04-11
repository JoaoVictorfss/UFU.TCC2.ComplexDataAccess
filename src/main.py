from domain.config.Settings import Settings
from utils.FakerUtils import FakerUtils
from utils.FileUtils import FileUtils
from utils.RandomUtils import RandomUtils
from infra.databases.PostgreSqlDatabase import PostgreSqlDatabase
from infra.databases.Neo4jDatabase import Neo4jDatabase

pgDatabase = PostgreSqlDatabase()
neo4jDatabase = Neo4jDatabase()

def dataLoad():  
  records = FileUtils.retrieveData(Settings.DATASET_FILE_PATH)

  randomDataTotal = Settings.RANDOM_DATA_TOTAL
  authors = FakerUtils.generateUniqueFirstNames(randomDataTotal)
  classifications = FakerUtils.generateUsPatentClassifications(randomDataTotal)
  datetimes = FakerUtils.generateDateTimes(Settings.DATASET_START_DATE, Settings.DATASET_END_DATE, randomDataTotal)
  
  for i in range(Settings.DATASET_MIN_COUNT):
    fromNodeData = (records[i][0], authors[RandomUtils.getRandomInt(randomDataTotal)], classifications[RandomUtils.getRandomInt(randomDataTotal)], datetimes[RandomUtils.getRandomInt(randomDataTotal)])
    toNodeData = (records[i][1], authors[RandomUtils.getRandomInt(randomDataTotal)], classifications[RandomUtils.getRandomInt(randomDataTotal)], datetimes[RandomUtils.getRandomInt(randomDataTotal)])   
    setRecords(fromNodeData, toNodeData)


def setRecords(fromNodeData, toNodeData):
  data = (fromNodeData, toNodeData)
  pgDatabase.setRecords(data)
  neo4jDatabase.setRecords(data)
  
def main():
 pgDatabase.init()
 neo4jDatabase.init()
 dataLoad()
 pgDatabase.close()
 neo4jDatabase.close()
 
main()