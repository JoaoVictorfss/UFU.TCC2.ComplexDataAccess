from domain.config.Settings import Settings
from utils.FakerUtils import FakerUtils
from utils.FileUtils import FileUtils
from utils.RandomUtils import RandomUtils
from infra.databases.PostgreSqlDatabase import PostgreSqlDatabase

pgDatabase = PostgreSqlDatabase()

def dataLoad():  
  records = FileUtils.retrieveData(Settings.DATASET_FILE_PATH)
  
  randomDataTotal = Settings.RANDOM_DATA_TOTAL
  authors = FakerUtils.generateUniqueFirstNames(randomDataTotal)
  classifications = FakerUtils.generateUsPatentClassifications(randomDataTotal)
  datetimes = FakerUtils.generateDateTimes(Settings.DATA_START_DATE, Settings.DATA_END_DATE, randomDataTotal)
  
  for i in range(Settings.DATA_MIN):
    firstRecordData = (records[i][0], authors[RandomUtils.getRandomInt(randomDataTotal)], classifications[RandomUtils.getRandomInt(randomDataTotal)], datetimes[RandomUtils.getRandomInt(randomDataTotal)])
    secondRecordData = (records[i][1], authors[RandomUtils.getRandomInt(randomDataTotal)], classifications[RandomUtils.getRandomInt(randomDataTotal)], datetimes[RandomUtils.getRandomInt(randomDataTotal)]) 
    pgDatabase.setRecords((firstRecordData, secondRecordData))

def main():
 pgDatabase.init()
 #createNeo4jDatabase()
 dataLoad()
 pgDatabase.close()
 
main()