from domain.config.Settings import Settings
from utils.FakerUtils import FakerUtils
from utils.FileUtils import FileUtils
from utils.RandomUtils import RandomUtils
from tests.TestsHandler import TestsHandler

def dataPreProcessing(): 
  #retrieves data from dataset file
  patentIdentifiers = FileUtils.retrieveData(Settings.DATASET_FILE_PATH)
  
  #generates fake data for testing with filters
  authors = FakerUtils.generateUniqueFirstNames(Settings.RANDOM_DATA_TOTAL)
  classifications = FakerUtils.generateUsPatentClassifications(Settings.RANDOM_DATA_TOTAL)
  datetimes = FakerUtils.generateDateTimes(Settings.DATASET_START_DATE, Settings.DATASET_END_DATE,  Settings.RANDOM_DATA_TOTAL)
  
  records = [] 
  
  for i in range(Settings.DATASET_MIN_COUNT):
    fromNodeData = (patentIdentifiers[i][0], authors[RandomUtils.getRandomInt( Settings.RANDOM_DATA_TOTAL)], classifications[RandomUtils.getRandomInt( Settings.RANDOM_DATA_TOTAL)], datetimes[RandomUtils.getRandomInt( Settings.RANDOM_DATA_TOTAL)])
    toNodeData = (patentIdentifiers[i][1], authors[RandomUtils.getRandomInt( Settings.RANDOM_DATA_TOTAL)], classifications[RandomUtils.getRandomInt( Settings.RANDOM_DATA_TOTAL)], datetimes[RandomUtils.getRandomInt( Settings.RANDOM_DATA_TOTAL)])   
    records.append((fromNodeData, toNodeData))
  
  return records
  
def main():
  records = dataPreProcessing()
  
  testsHandler = TestsHandler()
  testsHandler.startTests() 
  testsHandler.executeDataLoadTest(records)
  testsHandler.endTests()
 
main()