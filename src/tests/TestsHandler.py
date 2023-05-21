import concurrent.futures
from datetime import datetime
from infra.databases.PostgreSqlDatabase import PostgreSqlDatabase
from infra.databases.Neo4jDatabase import Neo4jDatabase
from infra.io.logs.LogInCsvFile import LogInCsvFile

NEO4J_SGBD = "Neo4j"
POSTGRESQL_SGBD = "PostgreSql"
DATA_LOAD_TEST = "Data Load"

class TestsHandler:
    def __init__(self, settings):
        self._settings = settings
        self._csvFieldNames = ["SGBD", "Test Type", "Start At", "End At", "Executation Time"]
        self._csvFileBasePath = settings.results_base_path
        self._pgDatabase = PostgreSqlDatabase()
        self._neo4jDatabase = Neo4jDatabase()
    
    def startTests(self):
        self._pgDatabase.init(self._settings)
        self._neo4jDatabase.init(self._settings)
 
    def executeDataLoadTest(self, records):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_pg = executor.submit(self._executePgDataLoadTest, records)
            future_neo4j = executor.submit(self._executeNeo4jDataLoadTest, records)

            future_pg.result()
            future_neo4j.result()
        
    def endTests(self):
        self._pgDatabase.close()
        self._neo4jDatabase.close()
    
    def _executePgDataLoadTest(self, records):
        startAt = datetime.utcnow()
        
        for record in records:
            self._pgDatabase.setRecords(record)
            
        endAt = datetime.utcnow()
        
        self._logInCsvFile(POSTGRESQL_SGBD, DATA_LOAD_TEST, startAt, endAt)
    
    def _executeNeo4jDataLoadTest(self, records):
        startAt = datetime.utcnow()
        
        for record in records:
            self._neo4jDatabase.setRecords(record)
            
        endAt = datetime.utcnow()
        
        self._logInCsvFile(NEO4J_SGBD, DATA_LOAD_TEST, startAt, endAt)
    
    def _logInCsvFile(self, sgbd, testType, startAt, endAt):
        file = f"{self._csvFileBasePath}/{sgbd.lower()}/{testType.lower()}.csv"
        data = [{
            "SGBD": sgbd,
            "Test Type": testType,
            "Start At": startAt,
            "End At": endAt,
            "Executation Time": startAt - endAt
        }]
        LogInCsvFile.write(file, self._csvFieldNames, data)