from utils.FakerUtils import FakerUtils
from infra.io.files.FileHandler import FileHandler
from utils.RandomUtils import RandomUtils
from tests.TestsHandler import TestsHandler
from domain.config.Settings import Settings 

def dataPreProcessing(settings):
  #retrieves data from dataset file
  patentIdentifiers = FileHandler.retrieveData(settings.dataset_file_path)
  
  #generates fake data for testing with filters
  authors = FakerUtils.generateUniqueFirstNames(settings.fake_authors_total)
  classifications = FakerUtils.generateUsPatentClassifications(settings.fake_classifications_total)
  datetimes = FakerUtils.generateDateTimes(settings.dataset_start_date, settings.dataset_end_date, settings.fake_datetimes_total)
  
  records = [] 
  
  for i in range((settings.data_max - 1)):
    ids = (patentIdentifiers[i][0]).split("\t")
    fromNodeData = (ids[0], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], datetimes[getIndex(len(datetimes))], ids[1])
    toNodeData = (ids[1], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], datetimes[getIndex(len(datetimes))], None)
    records.append((fromNodeData, toNodeData))
  
  return records

def getIndex(len):
  return RandomUtils.getRandomInt(len - 1)

def main():
  settings = Settings('settings.yml')
  records = dataPreProcessing(settings)
  
  testsHandler = TestsHandler(settings)
  testsHandler.startTests() 
  testsHandler.executeDataLoadTest(records)
  testsHandler.executePatentTraversalTest(settings.traversal_patent_id)
  testsHandler.endTests()

main()