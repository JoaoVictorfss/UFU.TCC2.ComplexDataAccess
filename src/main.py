from utils.FakerUtils import FakerUtils
from infra.io.files.FileHandler import FileHandler
from utils.RandomUtils import RandomUtils
# from tests.TestsHandler import TestsHandler
from domain.config.Settings import Settings 

def dataPreProcessing(config):
  #retrieves data from dataset file
  patentIdentifiers = FileHandler.retrieveData(config.dataset_file_path)
  
  #generates fake data for testing with filters
  authors = FakerUtils.generateUniqueFirstNames(config.fake_authors_total)
  classifications = FakerUtils.generateUsPatentClassifications(config.fake_classifications_total)
  datetimes = FakerUtils.generateDateTimes(config.dataset_start_date, config.dataset_end_date, config.fake_datetimes_total)
  
  records = [] 
  
  for i in range((config.data_max - 1)):
    ids = (patentIdentifiers[i][0]).split("\t")
    fromNodeData = (ids[0], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], datetimes[getIndex(len(datetimes))], ids[1])
    toNodeData = (ids[1], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], datetimes[getIndex(len(datetimes))], None)
    records.append((fromNodeData, toNodeData))
  
  return records

def getIndex(len):
  return RandomUtils.getRandomInt(len - 1)

def main():
  config = Settings('settings.yml')
  records = dataPreProcessing(config)
  
  # testsHandler = TestsHandler(config.results_base_path)
  # testsHandler.startTests() 
  # testsHandler.executeDataLoadTest(records)
  # testsHandler.endTests()

main()