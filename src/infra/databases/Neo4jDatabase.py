from domain.config.Settings import Settings
from adapters.Neo4jAdpater import Neo4jAdpater
from scripts.Neo4jScripts import Neo4jScripts

class Neo4jDatabase:
    def init(self):
        self.__neo4jAdapter = Neo4jAdpater(Settings.DB_NEO4J_URI, Settings.DB_NEO4J_USER, Settings.DB_NEO4J_PASSWORD)
        commands = (
            Neo4jScripts.CREATE_INDEX_PATENT_ID,
            Neo4jScripts.CREATE_INDEX_PATENT_AUTHOR,
            Neo4jScripts.CREATE_INDEX_PATENT_CLASSIFICATION,
            Neo4jScripts.CREATE_INDEX_PATENT_REGISTERED_DATE,
            Neo4jScripts.CREATE_CONSTRAINT_PATENT_ID
        )
        self.__neo4jAdapter.executeQueries(commands)
        
    def setRecords(self, records):
        rows = list(map(lambda record: {
            'patentId': record[0],
            'author': record[1],
            'classification': record[2],
            'registeredAt': record[3],
            'relatedPatentId': record[4]
        }, records))
        self.__neo4jAdapter.executeTransaction(
            Neo4jScripts.CREATE_RELATIONSHIP_BETWEEN_NODES, rows)
                    
    def close(self): 
        self.__neo4jAdapter.closeConnection()
 