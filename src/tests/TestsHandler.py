from datetime import datetime
from infra.databases.PostgreSqlDatabase import PostgreSqlDatabase
from infra.databases.Neo4jDatabase import Neo4jDatabase
from infra.io.logs.LogInCsvFile import LogInCsvFile
from domain.config.Settings import Settings

NEO4J_SGBD = "Neo4j"
POSTGRESQL_SGBD = "PostgreSql"
DATA_LOAD_TEST = "Data Load"

class TestsHandler:
    def __init__(self):
        self._csvFieldNames = ["SGBD", "Test Type", "Start At", "End At", "Executation Time"]
        self._csvFilePath = f"{Settings.RESULTS_BASE_PATH}/metrics.csv"
        self._pgDatabase = PostgreSqlDatabase()
        self._neo4jDatabase = Neo4jDatabase()
    
    def startTests(self):
        self._pgDatabase.init()
        self._neo4jDatabase.init()
 
    def executeDataLoadTest(self, records):
        self._executePgDataLoadTest(records)
        self._executeNeo4jDataLoadTest(records)
        
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
        data = [{
            "SGBD": sgbd,
            "Test Type": testType,
            "Start At": startAt,
            "End At": endAt,
            "Executation Time": startAt - endAt
        }]
        LogInCsvFile.write(self._csvFilePath, self._csvFieldNames, data)