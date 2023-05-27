from utils.FakerUtils import FakerUtils
from infra.io.files.FileHandler import FileHandler
from utils.RandomUtils import RandomUtils
from tests.TestsHandler import TestsHandler
from domain.config.Settings import Settings 

#Method to handle data pre processing
def dataPreProcessing(settings):
  mappedIds = {}

  #retrieves data from dataset file
  patentIdentifiers = FileHandler.retrieveData(settings.dataset_file_path)
  
  #Generates fake author names and US patent classifications for testing with filters
  authors = FakerUtils.generateUniqueFirstNames(settings.fake_authors_total)
  classifications = FakerUtils.generateUsPatentClassifications(settings.fake_classifications_total)
  
  #Generates fake data for each patent's id in dataset file
  for i in range((settings.data_max - 1)):
    fromNodeData = None
    ids = (patentIdentifiers[i][0]).split("\t")
    
    if(ids[0] not in mappedIds):
      fromNodeRegistrationDate = FakerUtils.generateDateTime(settings.dataset_start_date, settings.dataset_end_date)
      fromNodeData = (ids[0], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], fromNodeRegistrationDate, ids[1])
      mappedIds[ids[0]] = fromNodeData
    else: fromNodeData = mappedIds[ids[0]]
    
    if(ids[1] not in mappedIds):
      toNodeRegistrationDate = FakerUtils.generateDateTime(fromNodeData[3], settings.dataset_end_date)
      toNodeData = (ids[1], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], toNodeRegistrationDate, None)
      mappedIds[ids[1]] = toNodeData
      
  return list(mappedIds.values())

def getIndex(len):
  return RandomUtils.getRandomInt(len - 1)

def main():
  settings = Settings('settings.yml')
  records = dataPreProcessing(settings)

  #Start test
  testsHandler = TestsHandler(settings)
  testsHandler.startTests() 
  
  #Executes tests
  if(settings.tests_data_load_enabled):
    testsHandler.executeDataLoadTests(records)
  if(settings.tests_traversal_enabled):
    testsHandler.executeTestsWithTraversingQueries()
  if(settings.tests_patternMatching_enabled):
    testsHandler.executeTestsWithPatternMatchingQueries()
  if(settings.tests_aggregation_enabled):
    testsHandler.executeTestsWithAggregationQueries()
  if(settings.tests_simple_enabled):
    testsHandler.executeTestsWithoutTraversingQueries()
    
  #End tests
  testsHandler.endTests()

main()