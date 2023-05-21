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
BRAZIL_DATE_FORMAT = "%Y/%m/%d %H:%M"
class TestsHandler:
    def __init__(self, settings):
        self._settings = settings
        self._csvFieldNames = ["SGBD", "Test Type", "Start At", "End At", "Executation Time(MS)"]
        self._csvFileBasePath = settings.results_base_path
        self._pgDatabase = PostgreSqlDatabase()
        self._neo4jDatabase = Neo4jDatabase()
    
    def startTests(self):
        Log.information("[TestsHandler] Try to run tests")
        self._pgDatabase.init(self._settings)
        #self._neo4jDatabase.init(self._settings)
        Log.information("[TestsHandler] Tests run successfully")

    def executeDataLoadTest(self, records):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_pg = executor.submit(self._executePgDataLoadTest, records)
            future_pg = executor.submit(self._executePgDataLoadTest, records)

            #future_neo4j = executor.submit(self._executeNeo4jDataLoadTest, records)

            future_pg.result()
            #future_neo4j.result()

    def executePatentTraversalTest(self, patentId):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_pg = executor.submit(self._executePgPatentTraversalTest, patentId)
            #future_neo4j = executor.submit(self._executeNeo4jDataLoadTest, records)

            future_pg.result()
            #future_neo4j.result()
            
    def endTests(self):
        self._pgDatabase.close()
        # self._neo4jDatabase.close()
    
    def _executePgPatentTraversalTest(self, patentId):
        try:
            Log.information("[TestsHandler executePgPatentTraversalTest] Try to run pg patent traversal test")

            startAt = datetime.now()
            
            self._pgDatabase.getReferencingPatents(patentId)
                
            endAt = datetime.now()
            
            self._logInCsvFile(POSTGRESQL_SGBD, TRAVERSAL_TEST, startAt, endAt)
            
            Log.information("[TestsHandler executePgPatentTraversalTest] PG patent traversal test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler executePgPatentTraversalTest] - An error occurred while trying to execute pg patent traversal test ~ Error: {error}")

    def _executePgDataLoadTest(self, records):
        try:
            Log.information("[TestsHandler executePgDataLoadTest] Try to run pg patent traversal test")

            startAt = datetime.now()
            
            for record in records:
                self._pgDatabase.setRecords(record)
                
            endAt = datetime.now()
            
            self._logInCsvFile(POSTGRESQL_SGBD, DATA_LOAD_TEST, startAt, endAt)
            
            Log.information("[TestsHandler executePgDataLoadTest] PG data load test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler executePgDataLoadTest] - An error occurred while trying to execute pg data load test ~ Error: {error}")
    
    def _executeNeo4jDataLoadTest(self, records):
        try:
            Log.information("[TestsHandler executeNeo4jDataLoadTest] Try to run Neo4j data load test")

            startAt = datetime.now()

            for record in records:
                self._neo4jDatabase.setRecords(record)

            endAt = datetime.now()

            self._logInCsvFile(NEO4J_SGBD, DATA_LOAD_TEST, startAt, endAt)
            
            Log.information("[TestsHandler executeNeo4jDataLoadTest] Neo4j data load test run successfully")
        except Exception as error:
            Log.error(f"[TestsHandler executePgDataLoadTest] - An error occurred while trying to execute pg data load test ~ Error: {error}")
    
    def _logInCsvFile(self, sgbd, testType, startAt, endAt):
        fileName = testType.lower().replace(" ", "_")
        filePath = f"{self._csvFileBasePath}/{sgbd.lower()}/{fileName}.csv"
        data = [{
            "SGBD": sgbd,
            "Test Type": testType,
            "Start At": startAt.strftime(BRAZIL_DATE_FORMAT),
            "End At": endAt.strftime(BRAZIL_DATE_FORMAT),
            "Executation Time(MS)": (endAt - startAt).total_seconds() * 1000
        }]
        LogInCsvFile.write(filePath, self._csvFieldNames, data)
