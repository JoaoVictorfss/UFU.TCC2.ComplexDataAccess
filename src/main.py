from domain.config.Settings import Settings
from utils.FakerUtils import FakerUtils
from infra.io.files.FileHandler import FileHandler
from utils.RandomUtils import RandomUtils
from tests.TestsHandler import TestsHandler

def dataPreProcessing(): 
  #retrieves data from dataset file
  patentIdentifiers = FileHandler.retrieveData(Settings.DATA_DATASET_FILE_PATH)
  
  #generates fake data for testing with filters
  authors = FakerUtils.generateUniqueFirstNames(Settings.DATA_FAKE_TOTAL)
  classifications = FakerUtils.generateUsPatentClassifications(Settings.DATA_FAKE_TOTAL)
  datetimes = FakerUtils.generateDateTimes(Settings.DATA_DATASET_START_DATE, Settings.DATA_DATASET_END_DATE,  Settings.DATA_FAKE_TOTAL)
  
  records = [] 
  
  for i in range(Settings.DATA_MIN):
    fromNodeData = (patentIdentifiers[i][0], authors[RandomUtils.getRandomInt( Settings.DATA_FAKE_TOTAL)], classifications[RandomUtils.getRandomInt( Settings.DATA_FAKE_TOTAL)], datetimes[RandomUtils.getRandomInt( Settings.DATA_FAKE_TOTAL)])
    toNodeData = (patentIdentifiers[i][1], authors[RandomUtils.getRandomInt( Settings.DATA_FAKE_TOTAL)], classifications[RandomUtils.getRandomInt( Settings.DATA_FAKE_TOTAL)], datetimes[RandomUtils.getRandomInt( Settings.DATA_FAKE_TOTAL)])   
    records.append((fromNodeData, toNodeData))
  
  return records
  
def main():
  records = dataPreProcessing()
  
  testsHandler = TestsHandler()
  testsHandler.startTests() 
  testsHandler.executeDataLoadTest(records)
  testsHandler.endTests()
 
main()