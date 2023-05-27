import concurrent.futures
from datetime import datetime
from infra.databases.PostgreSqlDatabase import PostgreSqlDatabase
from infra.databases.Neo4jDatabase import Neo4jDatabase
from infra.io.logs.LogInCsvFile import LogInCsvFile
from infra.io.logs.LogInConsole import LogInConsole as Log

NEO4J_SGBD = "Neo4j"
POSTGRESQL_SGBD = "PostgreSql"
DATA_LOAD_TEST = "Data Load"
TRAVERSAL_TEST = "Traversal"
NO_TRAVERSAL_TEST = "No Traversal"
PATTERN_MATCHING_TEST = "Pattern Matching"
AGGREGATION_TEST = "Aggregation"
DATA_LOAD_TEST_DESCRIPTION = "Data load test"
PATENT_BY_ID_TEST_DESCRIPTION = "Test to get a patent by id"
AUTHOR_PATENTS_TEST_DESCRIPTION = "Test to get author's patents"
LATEST_PATENTS_STATISTIC_TEST_DESCRIPTION = "Test to get the number and percentage of citations made and received per patent of the 1000 most recent patents"
PATENTS_COUNT_BY_CLASSIFICATION_TEST_DESCRIPTION = "Test to get patents count per classification"
PATENT_CITATIONS_TEST_DESCRIPTION = "Test to get patents that cite a specific one"
AUTHOR_PATENT_CITATIONS_TEST_DESCRIPTION = "Test to get patents that cite patents of a specific author"
BRAZIL_DATE_FORMAT = "%Y/%m/%d %H:%M"

#Tests handler
class TestsHandler:
    def __init__(self, settings):
        self._settings = settings
        self._csvFieldNames = ["SGBD", "Test Type", "Start At", "End At", "Executation Time(MS)"]
        self._csvFileBasePath = settings.results_base_path
        self._pgDatabase = PostgreSqlDatabase()
        self._neo4jDatabase = Neo4jDatabase()
    
    #Start tests: Creates the databases structure and configuration
    def startTests(self):
        Log.information("[TestsHandler] try to run tests")
        self._pgDatabase.init(self._settings)
        self._neo4jDatabase.init(self._settings)
    
    #Executes the data load test for PostgreSql and Neo4j
    def executeDataLoadTests(self, records):
        self._executePgDataLoadTest(records)
        self._executeNeo4jDataLoadTest(records)
    
    #Executes pattern matching queries for PostgreSql and Neo4j
    def executeTestsWithPatternMatchingQueries(self):
        self._getPatentCitationsOfTheSameClassificationFromPgDb()
        self._getPatentCitationsOfTheSameClassificationFromNeo4jDb()
    
    #Executes aggregation queries for PostgreSql and Neo4j
    def executeTestsWithAggregationQueries(self):
        self._getTop1000LatestPatentsStatisticsFromPgDb()
        self._getTop1000LatestPatentsStatisticsFromNeo4jDb()
        self._getPatentsCountPerClassificationFromPgDb() 
        self._getPatentsCountPerClassificationFromNeo4jDb() 

    #Executes queries with traversal for PostgreSql and Neo4j
    def executeTestsWithTraversingQueries(self):
        self._getPatentCitationsByIdFromPgDb(self._settings.tests_filters_patent_id)
        self._getPatentCitationsByIdFromNeo4jDb(self._settings.tests_filters_patent_id)
        
        date = datetime.strptime(self._settings.tests_filters_registration_date, "%Y-%m-%d").date()
        author = self._settings.tests_filters_author 
             
        self._getPatentCitationsByAuthorAndRegistrationDateFromPgDb(author, date)
        self._getPatentCitationsByAuthorAndRegistrationDateFromNeo4jDb(author, date)     
 
    #Executes queries without traversal for PostgreSql and Neo4j
    def executeTestsWithoutTraversingQueries(self):
        self._getPatentByIdFromPgDb()
        self._getPatentByIdFromNeo4jDb()
        self._getAuthorPatentsFromPgDb()
        self._getAuthorPatentsFromNeo4jDb()
        
    #Finishes the tests and close driver's connections   
    def endTests(self):
        self._pgDatabase.close()
        self._neo4jDatabase.close()
        Log.information("[TestsHandler] Tests run successfully")   
    
    #Region of private methods
    
    #Executes the data load test for PostgreSql
    def _executePgDataLoadTest(self, records):
        try:
            Log.information("[TestsHandler executePgDataLoadTest] try to run test")

            startAt = datetime.now()           
            self._executeUsingMultithread(self._pgDatabase.setRecords, records, self._settings.tests_data_load_threads_max)                  
            endAt = datetime.now()          
            self._logInCsvFile(POSTGRESQL_SGBD, DATA_LOAD_TEST, startAt, endAt, DATA_LOAD_TEST_DESCRIPTION)
            
            Log.information("[TestsHandler executePgDataLoadTest] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler executePgDataLoadTest] - an error occurred while trying to execute test ~ Error: {error}")
            
    #Gets patents that cite a specific one from pg db
    def _getPatentCitationsByIdFromPgDb(self, patentId):
        try:
            Log.information("[TestsHandler getPatentCitationsByIdFromPgDb] try to run test")

            startAt = datetime.now()         
            result = self._pgDatabase.getPatentCitationsById(patentId)            
            endAt = datetime.now()  
            self._logInCsvFile(POSTGRESQL_SGBD, TRAVERSAL_TEST, startAt, endAt, PATENT_CITATIONS_TEST_DESCRIPTION, len(result))
                    
            Log.information("[TestsHandler getPatentCitationsByIdFromPgDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentCitationsByIdFromPgDb] - an error occurred while trying to execute test ~ Error: {error}")

    #Gets patents that cite an author's patents from pg db
    def _getPatentCitationsByAuthorAndRegistrationDateFromPgDb(self, author, date):
        try:
            Log.information("[TestsHandler getPatentCitationsByAuthorAndRegistrationDateFromPgDb] try to run test")

            startAt = datetime.now()
            result = self._pgDatabase.getPatentCitationsByAuthorAndRegistrationDate(author, date)
            endAt = datetime.now()
            self._logInCsvFile(POSTGRESQL_SGBD, TRAVERSAL_TEST, startAt, endAt, AUTHOR_PATENT_CITATIONS_TEST_DESCRIPTION, len(result))
            
            Log.information("[TestsHandler getPatentCitationsByAuthorAndRegistrationDateFromPgDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentCitationsByAuthorAndRegistrationDateFromPgDb] - an error occurred while trying to execute test ~ Error: {error}")
    
    #Gets the number and percentage of citations made and received per patent of the 1000 most recent patents from pg db
    def _getTop1000LatestPatentsStatisticsFromPgDb(self):
        try:
            Log.information("[TestsHandler getTop1000LatestPatentsStatisticsFromPgDb] try to run test")

            startAt = datetime.now()
            result = self._pgDatabase.getTop1000LatestPatentsStatistics()
            endAt = datetime.now()
            self._logInCsvFile(POSTGRESQL_SGBD, AGGREGATION_TEST, startAt, endAt, LATEST_PATENTS_STATISTIC_TEST_DESCRIPTION, len(result))
           
            Log.information("[TestsHandler getTop1000LatestPatentsStatisticsFromPgDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getTop1000LatestPatentsStatisticsFromPgDb] - an error occurred while trying to execute test ~ Error: {error}")
    
    #Gets patents count per classification from pg db
    def _getPatentsCountPerClassificationFromPgDb(self):
        try:
            Log.information("[TestsHandler getPatentsCountPerClassificationFromPgDb] try to run test")

            startAt = datetime.now()
            result = self._pgDatabase.getPatentsCountPerClassification()
            endAt = datetime.now()
            self._logInCsvFile(POSTGRESQL_SGBD, AGGREGATION_TEST, startAt, endAt, PATENTS_COUNT_BY_CLASSIFICATION_TEST_DESCRIPTION, len(result))
            
            Log.information("[TestsHandler getPatentsCountPerClassificationFromPgDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentsCountPerClassificationFromPgDb] - an error occurred while trying to execute test ~ Error: {error}")
        
    #Gets patent by id from pg db
    def _getPatentByIdFromPgDb(self, patentId):
        try:
            Log.information("[TestsHandler getPatentByIdFromPgDb] try to run test")

            startAt = datetime.now()
            result = self._pgDatabase.getPatentById(patentId)
            endAt = datetime.now()
            self._logInCsvFile(POSTGRESQL_SGBD, NO_TRAVERSAL_TEST, startAt, endAt, PATENT_BY_ID_TEST_DESCRIPTION, len(result))
            
            Log.information("[TestsHandler getPatentByIdFromPgDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentByIdFromPgDb] - an error occurred while trying to execute test ~ Error: {error}")
    
    #Gets author's patents from pg neo4j db
    def _getAuthorPatentsFromPgDb(self, author):
        try:
            Log.information("[TestsHandler getAuthorPatentsFromPgDb] try to run test")

            startAt = datetime.now()
            result = self._pgDatabase.getAuthorPatents(author)
            endAt = datetime.now()
            self._logInCsvFile(POSTGRESQL_SGBD, NO_TRAVERSAL_TEST, startAt, endAt, AUTHOR_PATENTS_TEST_DESCRIPTION, len(result))
            
            Log.information("[TestsHandler getAuthorPatentsFromPgDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getAuthorPatentsFromPgDb] - an error occurred while trying to execute test ~ Error: {error}")
   
    #Gets patents that cite patents of the same classification from pg db
    def _getPatentCitationsOfTheSameClassificationFromPgDb(self):
        try:
            Log.information("[TestsHandler getPatentCitationsOfTheSameClassificationFromPgDb] try to run test")

            startAt = datetime.now()
            result = self._pgDatabase.getPatentCitationsOfTheSameClassification()
            endAt = datetime.now()
            self._logInCsvFile(POSTGRESQL_SGBD, PATTERN_MATCHING_TEST, startAt, endAt, PATTERN_MATCHING_TEST, len(result))
            
            Log.information("[TestsHandler getPatentCitationsOfTheSameClassificationFromPgDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentCitationsOfTheSameClassificationFromPgDb] - an error occurred while trying to execute test ~ Error: {error}")
      
    #Executes the data load test for Neo4j
    def _executeNeo4jDataLoadTest(self, records):
        try:
            Log.information("[TestsHandler executeNeo4jDataLoadTest] try to run test")
            
            startAt = datetime.now()
            self._executeUsingMultithread(self._neo4jDatabase.setRecords, records, self._settings.tests_data_load_threads_max)      
            endAt = datetime.now()        
            self._logInCsvFile(NEO4J_SGBD, DATA_LOAD_TEST, startAt, endAt, DATA_LOAD_TEST_DESCRIPTION)
            
            Log.information("[TestsHandler executeNeo4jDataLoadTest] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler executePgDataLoadTest] - an error occurred while trying to execute test ~ Error: {error}")

    #Gets patents that cite a specific one from neo4j db
    def _getPatentCitationsByIdFromNeo4jDb(self, patentId):
        try:
            Log.information("[TestsHandler getPatentCitationsByIdFromNeo4jDb] try to run test")

            startAt = datetime.now()
            result = self._neo4jDatabase.getPatentCitationsById(patentId)
            endAt = datetime.now()
            self._logInCsvFile(NEO4J_SGBD, TRAVERSAL_TEST, startAt, endAt, PATENT_CITATIONS_TEST_DESCRIPTION, len(result))
            
            Log.information("[TestsHandler getPatentCitationsByIdFromNeo4jDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentCitationsByIdFromNeo4jDb] - an error occurred while trying to execute test ~ Error: {error}")

    #Gets patents that cite an author's patents from neo4j db
    def _getPatentCitationsByAuthorAndRegistrationDateFromNeo4jDb(self, author, date):
        try:
            Log.information("[TestsHandler getPatentCitationsByAuthorAndRegistrationDateFromNeo4jDb] try to run test")

            startAt = datetime.now()
            result = self._neo4jDatabase.getPatentCitationsByAuthorAndRegistrationDate(author, date)
            endAt = datetime.now()
            self._logInCsvFile(NEO4J_SGBD, TRAVERSAL_TEST, startAt, endAt, AUTHOR_PATENT_CITATIONS_TEST_DESCRIPTION, len(result))
           
            Log.information("[TestsHandler getPatentCitationsByAuthorAndRegistrationDateFromNeo4jDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentCitationsByAuthorAndRegistrationDateFromNeo4jDb] - an error occurred while trying to execute test ~ Error: {error}")
    
    #Gets the number and percentage of citations made and received per patent of the 1000 most recent patents from n3o4j db
    def _getTop1000LatestPatentsStatisticsFromNeo4jDb(self):
        try:
            Log.information("[TestsHandler getTop1000LatestPatentsStatisticsFromNeo4jDb] try to run test")

            startAt = datetime.now()
            result = self._neo4jDatabase.getTop1000LatestPatentsStatistics()
            endAt = datetime.now()
            self._logInCsvFile(NEO4J_SGBD, AGGREGATION_TEST, startAt, endAt, LATEST_PATENTS_STATISTIC_TEST_DESCRIPTION, len(result))
           
            Log.information("[TestsHandler getTop1000LatestPatentsStatisticsFromNeo4jDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getTop1000LatestPatentsStatisticsFromNeo4jDb] - an error occurred while trying to execute test ~ Error: {error}")

    #Gets patents count per classification from neo4j db
    def _getPatentsCountPerClassificationFromNeo4jDb(self):
        try:
            Log.information("[TestsHandler getPatentsCountPerClassificationFromNeo4jDb] try to run test")

            startAt = datetime.now()
            result = self._neo4jDatabase.getPatentsCountPerClassification()
            endAt = datetime.now()
            self._logInCsvFile(NEO4J_SGBD, AGGREGATION_TEST, startAt, endAt, PATENTS_COUNT_BY_CLASSIFICATION_TEST_DESCRIPTION, len(result))
           
            Log.information("[TestsHandler getPatentsCountPerClassificationFromNeo4jDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentsCountPerClassificationFromNeo4jDb] - an error occurred while trying to execute test ~ Error: {error}")
      
    #Gets author's patents from pg neo4j db
    def _getAuthorPatentsFromNeo4jDb(self, author):
        try:
            Log.information("[TestsHandler getAuthorPatentsFromNeo4jDb] try to run test")

            startAt = datetime.now()
            result = self._neo4jDatabase.getAuthorPatents(author)
            endAt = datetime.now()
            self._logInCsvFile(NEO4J_SGBD, NO_TRAVERSAL_TEST, startAt, endAt, AUTHOR_PATENTS_TEST_DESCRIPTION, len(result))
            
            Log.information("[TestsHandler getAuthorPatentsFromNeo4jDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getAuthorPatentsFromNeo4jDb] - an error occurred while trying to execute test ~ Error: {error}")
     
    #Gets patent by id from pg neo4j db
    def _getPatentByIdFromNeo4jDb(self, patentId):
        try:
            Log.information("[TestsHandler getPatentByIdFromNeo4jDb] try to run test")

            startAt = datetime.now()
            result = self._neo4jDatabase.getPatentById(patentId)
            endAt = datetime.now()
            self._logInCsvFile(NEO4J_SGBD, NO_TRAVERSAL_TEST, startAt, endAt, PATENT_BY_ID_TEST_DESCRIPTION, len(result))
            
            Log.information("[TestsHandler getPatentByIdFromNeo4jDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentByIdFromNeo4jDb] - an error occurred while trying to execute test ~ Error: {error}")
 
    #Gets patents that cite patents of the same classification from neo4j
    def _getPatentCitationsOfTheSameClassificationFromNeo4jDb(self):
        try:
            Log.information("[TestsHandler getPatentCitationsOfTheSameClassificationFromNeo4jDb] try to run test")

            startAt = datetime.now()
            result = self._neo4jDatabase.getPatentCitationsOfTheSameClassification()
            endAt = datetime.now()
            self._logInCsvFile(NEO4J_SGBD, PATTERN_MATCHING_TEST, startAt, endAt, PATTERN_MATCHING_TEST, len(result))
           
            Log.information("[TestsHandler getPatentCitationsOfTheSameClassificationFromNeo4jDb] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler getPatentCitationsOfTheSameClassificationFromNeo4jDb] - an error occurred while trying to execute test ~ Error: {error}")
      
    #Executes a function using multithread
    def _executeUsingMultithread(self, func, data, maxWorkers):
        with concurrent.futures.ThreadPoolExecutor(max_workers=maxWorkers) as executor:
            executor.map(func, data)  
             
    #Log test's results in csv file
    def _logInCsvFile(self, sgbd, testType, startAt, endAt, description, result = "N/A"):
        #TO DO adicionar descrição do teste
        data = [{
            "SGBD": sgbd,
            "Test Type": testType,
            "Description": description,
            "Start At": startAt.strftime(BRAZIL_DATE_FORMAT),
            "End At": endAt.strftime(BRAZIL_DATE_FORMAT),
            "Executation Time(MS)": (endAt - startAt).total_seconds() * 1000,
            "Result": result
        }]
        LogInCsvFile.write(f"{self._csvFileBasePath}/metrics.csv", self._csvFieldNames, data)
