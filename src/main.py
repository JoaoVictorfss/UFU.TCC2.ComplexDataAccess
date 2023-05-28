from utils.FakerUtils import FakerUtils
from infra.io.files.FileHandler import FileHandler
from utils.RandomUtils import RandomUtils
from tests.TestsHandler import TestsHandler
from domain.config.Settings import Settings 
from datetime import timedelta
from infra.io.logs.LogInConsole import LogInConsole as Log
import threading
from concurrent.futures import ThreadPoolExecutor

#Method to handle data pre processing
def dataPreProcessing(settings):
  patentIdentifiers = FileHandler.retrieveData(settings.dataset_file_path, settings.data_max)
  authors = FakerUtils.generateNames(settings.fake_authors_total)
  classifications = FakerUtils.generateUsPatentClassifications(settings.fake_classifications_total)

  records = []
  mappedIds = {}
  lock = threading.Lock() 

  def processBatch(start_index, end_index):
    for i in range(start_index, end_index):
      ids = patentIdentifiers[i][0].split("\t")
      fromNodeData = None
      toNodeData = None

      with lock: 
        if ids[0] not in mappedIds:
          fromNodeRegistrationDate = FakerUtils.generateDateTime(settings.dataset_start_date, settings.dataset_end_date)
          fromNodeData = (ids[0], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], fromNodeRegistrationDate, ids[1])
          mappedIds[ids[0]] = fromNodeData
        else:
          fromNodeData = (mappedIds[ids[0]][0], mappedIds[ids[0]][1], mappedIds[ids[0]][2], mappedIds[ids[0]][3], ids[1])

      with lock: 
        if ids[1] not in mappedIds:
          toNodeRegistrationDate = FakerUtils.generateDateTime((fromNodeData[3] + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), settings.dataset_end_date)
          toNodeData = (ids[1], authors[getIndex(len(authors))], classifications[getIndex(len(classifications))], toNodeRegistrationDate, None)
          mappedIds[ids[1]] = toNodeData
        else:
          toNodeData = mappedIds[ids[1]]

      if fromNodeData is not None and toNodeData is not None:
        with lock:
          records.append((fromNodeData, toNodeData))

  batch_size = settings.fake_batchSize  

  with ThreadPoolExecutor() as executor:
      futures = []
      for i in range(settings.data_max):
        start_index = i * batch_size
        end_index = (i + 1) * batch_size
        future = executor.submit(processBatch, start_index, end_index)
        futures.append(future)

      for future in futures:
        future.result()

  return records

def getIndex(len):
  return RandomUtils.getRandomInt(len - 1)

def main():
  settings = Settings('settings.yml')
  
  records = None
  
  if(settings.tests_data_load_enabled):
    Log.information("Try to generate fake data")
    records = dataPreProcessing(settings)  
    Log.information("Successfully generated data")
  
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

  Log.information("Tests run successfully")

main()