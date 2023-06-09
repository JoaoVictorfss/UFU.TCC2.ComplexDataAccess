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
TRIPLE_CITATION_PATH = "Test to identify cases where a patent is cited by another patent, this cited patent is in turn cited by a co-author, and this co-author cites a third patent"
AUTHOR_PATENT_CITATIONS_TEST_DESCRIPTION = "Test to get patents that cite patents of a specific author"
BRAZIL_DATE_FORMAT = "%Y/%m/%d %H:%M"

#Tests handler
class TestsHandler:
    def __init__(self, settings):
        self._settings = settings
        self._csvFieldNames = ["SGBD", "Test Type", "Description", "Start At", "End At", "Executation Time(MS)", "Result"]
        self._csvFileBasePath = settings.results_base_path
        self._pgDatabase = PostgreSqlDatabase()
        self._neo4jDatabase = Neo4jDatabase()
    
    def configureDbs(self):
        self._pgDatabase.createConnection(self._settings)
        self._pgDatabase.configureDb()
        self._pgDatabase.closeConnection()
        
        self._neo4jDatabase.createConnection(self._settings)
        self._neo4jDatabase.configureDb()
        self._neo4jDatabase.closeConnection()
        
    #Executes the data load test for PostgreSql and Neo4j
    def executeDataLoadTests(self, records):
        self._pgDatabase.createConnection(self._settings)
        self._executePgDataLoadTest(records)
        self._pgDatabase.closeConnection()

        self._neo4jDatabase.createConnection(self._settings)
        self._executeNeo4jDataLoadTest(records)
        self._neo4jDatabase.closeConnection()

    #Executes pattern matching queries for PostgreSql and Neo4j
    def executeTestsWithPatternMatchingQueries(self):
        self._pgDatabase.createConnection(self._settings)
        self._executeQueryTest(self._pgDatabase.getPatentCitationsOfTheSameClassification, POSTGRESQL_SGBD, PATTERN_MATCHING_TEST, PATTERN_MATCHING_TEST)   
        self._pgDatabase.closeConnection()

        self._neo4jDatabase.createConnection(self._settings)
        self._executeQueryTest(self._neo4jDatabase.getPatentCitationsOfTheSameClassification, NEO4J_SGBD, PATTERN_MATCHING_TEST, PATTERN_MATCHING_TEST)   
        self._neo4jDatabase.closeConnection()

    #Executes aggregation queries for PostgreSql and Neo4j
    def executeTestsWithAggregationQueries(self):
        self._pgDatabase.createConnection(self._settings)
        self._executeQueryTest(self._pgDatabase.getTop1000LatestPatentsStatistics, POSTGRESQL_SGBD, AGGREGATION_TEST, LATEST_PATENTS_STATISTIC_TEST_DESCRIPTION)   
        self._executeQueryTest(self._pgDatabase.getPatentsCountPerClassification, POSTGRESQL_SGBD, AGGREGATION_TEST, PATENTS_COUNT_BY_CLASSIFICATION_TEST_DESCRIPTION)   
        self._pgDatabase.closeConnection()

        self._neo4jDatabase.createConnection(self._settings)
        self._executeQueryTest(self._neo4jDatabase.getTop1000LatestPatentsStatistics, NEO4J_SGBD, AGGREGATION_TEST, LATEST_PATENTS_STATISTIC_TEST_DESCRIPTION)   
        self._executeQueryTest(self._neo4jDatabase.getPatentsCountPerClassification, NEO4J_SGBD, AGGREGATION_TEST, PATENTS_COUNT_BY_CLASSIFICATION_TEST_DESCRIPTION)   
        self._neo4jDatabase.closeConnection()

    #Executes queries with traversal for PostgreSql and Neo4j
    def executeTestsWithTraversingQueries(self):
        date = datetime.strptime(self._settings.tests_filters_registration_date, "%Y-%m-%d").date()
        
        self._pgDatabase.createConnection(self._settings)
        self._executeQueryTest(self._pgDatabase.getPatentCitationsByAuthorAndRegistrationDate, POSTGRESQL_SGBD, TRAVERSAL_TEST, AUTHOR_PATENT_CITATIONS_TEST_DESCRIPTION, self._settings.tests_filters_author, date)   
        self._executeQueryTest(self._pgDatabase.findTripleCitationPath, POSTGRESQL_SGBD, TRAVERSAL_TEST, TRIPLE_CITATION_PATH)   
        self._pgDatabase.closeConnection()

        self._neo4jDatabase.createConnection(self._settings)
        self._executeQueryTest(self._neo4jDatabase.getPatentCitationsByAuthorAndRegistrationDate, NEO4J_SGBD, TRAVERSAL_TEST, AUTHOR_PATENT_CITATIONS_TEST_DESCRIPTION, self._settings.tests_filters_author, date)   
        self._executeQueryTest(self._neo4jDatabase.findTripleCitationPath, NEO4J_SGBD, TRAVERSAL_TEST, TRIPLE_CITATION_PATH)
        self._neo4jDatabase.closeConnection()

    #Executes queries without traversal for PostgreSql and Neo4j
    def executeTestsWithoutTraversingQueries(self):
        self._pgDatabase.createConnection(self._settings)
        self._executeQueryTest(self._pgDatabase.getPatentById, POSTGRESQL_SGBD, NO_TRAVERSAL_TEST, PATENT_BY_ID_TEST_DESCRIPTION, self._settings.tests_filters_patent_id)   
        self._executeQueryTest(self._pgDatabase.getAuthorPatents, POSTGRESQL_SGBD, NO_TRAVERSAL_TEST, AUTHOR_PATENTS_TEST_DESCRIPTION, self._settings.tests_filters_author)   
        self._pgDatabase.closeConnection()
        
        self._neo4jDatabase.createConnection(self._settings)
        self._executeQueryTest(self._neo4jDatabase.getPatentById, NEO4J_SGBD, NO_TRAVERSAL_TEST, PATENT_BY_ID_TEST_DESCRIPTION, self._settings.tests_filters_patent_id)   
        self._executeQueryTest(self._neo4jDatabase.getAuthorPatents, NEO4J_SGBD, NO_TRAVERSAL_TEST, AUTHOR_PATENTS_TEST_DESCRIPTION, self._settings.tests_filters_author)   
        self._neo4jDatabase.closeConnection()
 
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

    def _executeQueryTest(self, testFunc, sgbd, testType, description, param1=None, param2=None):
        try:
            Log.information(f"[TestsHandler executeQueryTest] try to run test of type {testType} and description {description}")
            
            startAt = datetime.now()
            result = testFunc() if param1 == None else testFunc(param1) if param2 == None else testFunc(param1, param2)  
            endAt = datetime.now()
            
            self._logInCsvFile(sgbd, testType, startAt, endAt, description, len(result))
            
            Log.information(f"[TestsHandler executeQueryTest] test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler executeQueryTest] - an error occurred while trying to execute test ~ Error: {error}")
       
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
