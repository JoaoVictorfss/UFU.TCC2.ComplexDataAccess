from infra.databases.PostgreSqlDatabase import PostgreSqlDatabase
from infra.databases.Neo4jDatabase import Neo4jDatabase

class Tests:
    def __init__(self):
        self._pgDatabase = PostgreSqlDatabase()
        self._neo4jDatabase = Neo4jDatabase()
    
    def start(self):
        self._pgDatabase.init()
        self._neo4jDatabase.init()

    def dataLoadTest(self, records):
        for record in records:
            self._pgDatabase.setRecords(record)
            self._neo4jDatabase.setRecords(record)
    
    def end(self):
        self._pgDatabase.close()
        self._neo4jDatabase.close()