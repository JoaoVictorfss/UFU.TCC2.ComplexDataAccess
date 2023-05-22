from utils.FakerUtils import FakerUtils
from infra.io.files.FileHandler import FileHandler
from utils.RandomUtils import RandomUtils
from tests.TestsHandler import TestsHandler
from domain.config.Settings import Settings 

#Method to handle data pre processing
def dataPreProcessing(settings):
  #retrieves data from dataset file
  patentIdentifiers = FileHandler.retrieveData(settings.dataset_file_path)
  
  #Generates fake author names, US patent classifications and registration date for testing with filters
  authors = FakerUtils.generateUniqueFirstNames(settings.fake_authors_total)
  classifications = FakerUtils.generateUsPatentClassifications(settings.fake_classifications_total)
  datetimes = FakerUtils.generateDateTimes(settings.dataset_start_date, settings.dataset_end_date, settings.fake_datetimes_total)
  
  records = [] 
  
  #Generates fake data for each patent's id in dataset file
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

  #Start test
  testsHandler = TestsHandler(settings)
  testsHandler.startTests() 
  
  #Executes tests
  testsHandler.executeDataLoadTest(records)
  testsHandler.executePatentCitationsTraversalTest()
  testsHandler.executeAuthorPatentCitationsTraversalTest()
  
  #End tests
  testsHandler.endTests()

main()