from utils.FakerUtils import FakerUtils
from infra.io.files.FileHandler import FileHandler
from utils.RandomUtils import RandomUtils
from tests.TestsHandler import TestsHandler
from domain.config.Settings import Settings 
from datetime import timedelta
from infra.io.logs.LogInConsole import LogInConsole as Log

#Method to handle data pre processing
def dataPreProcessing(settings):
  #retrieves data from dataset file  
  patentIdentifiers = FileHandler.retrieveData(settings.dataset_file_path, settings.data_max)
  authors = FakerUtils.generateNames(settings.fake_authors_total)
  classifications = FakerUtils.generateUsPatentClassifications(settings.fake_classifications_total)
  
  records = [] 
  mappedIds = {}
  
  #Generates fake data for each patent's id in dataset file
  for i in range((settings.data_max)):
    Log.information(f"Index {i}")

    ids = (patentIdentifiers[i][0]).split("\t")
    fromNodeData = None
    toNodeData = None
    
    Log.information(f"Generating fake data for patentId {ids[0]}")
    if(ids[0] not in mappedIds):
      fromNodeRegistrationDate = FakerUtils.generateDateTime(settings.dataset_start_date, settings.dataset_end_date)
      fromNodeData = (ids[0], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], fromNodeRegistrationDate, ids[1])
      mappedIds[ids[0]] = fromNodeData
    else: fromNodeData = (mappedIds[ids[0]][0], mappedIds[ids[0]][1], mappedIds[ids[0]][2], mappedIds[ids[0]][3], ids[1])
      
    Log.information(f"Generating fake data for patentId {ids[1]}")
    if(ids[1] not in mappedIds):
      toNodeRegistrationDate = FakerUtils.generateDateTime((fromNodeData[3] + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), settings.dataset_end_date)
      toNodeData = (ids[1], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], toNodeRegistrationDate, None)
      mappedIds[ids[1]] = toNodeData
    else: toNodeData = mappedIds[ids[1]]
    
    if(fromNodeData != None and toNodeData != None):
      records.append((fromNodeData, toNodeData))
  
  return records

def getIndex(len):
  return RandomUtils.getRandomInt(len - 1)

def main():
  settings = Settings('settings.yml')
  
  records = None
  
  if(settings.tests_data_load_enabled):
    records = dataPreProcessing(settings)  
  
  #Start test
  testsHandler = TestsHandler(settings)
  
  #Configure Db
  if(settings.tests_configure_db_enabled):
    testsHandler.configureDbs()
    
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

main()