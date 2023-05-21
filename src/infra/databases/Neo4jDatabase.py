from infra.databases.adapters.Neo4jAdpater import Neo4jAdpater
from infra.databases.scripts.Neo4jScripts import Neo4jScripts
    
class Neo4jDatabase:
    def init(self, settings):
        self.__neo4jAdapter = Neo4jAdpater(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)
        commands = [
            Neo4jScripts.CREATE_INDEX_PATENT_ID,
            Neo4jScripts.CREATE_INDEX_PATENT_AUTHOR,
            Neo4jScripts.CREATE_INDEX_PATENT_CLASSIFICATION,
            Neo4jScripts.CREATE_INDEX_PATENT_REGISTERED_DATE,
            Neo4jScripts.CREATE_CONSTRAINT_PATENT_ID
        ]
        self.__neo4jAdapter.executeQueries(commands)
        
    def setRecords(self, records):
        rows = list(map(lambda record: {
            'patentId': record[0],
            'author': record[1],
            'classification': record[2],
            'registeredAt': record[3],
            'relatedPatentId': record[4]
        }, records))
        self.__neo4jAdapter.executeTransaction(Neo4jScripts.CREATE_NODES_AND_RELATIONSHIP, rows)
                    
    def close(self): 
        self.__neo4jAdapter.closeConnection()
 