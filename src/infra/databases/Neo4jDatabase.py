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
        for record in records:
           self.__neo4jAdapter.executeQuery(
               Neo4jScripts.CREATE_NODE_PATENT, 
               [
                   {
                        'patentId': records[0][0],
                        'author': records[0][1],
                        'classification': records[0][2],
                        'registeredAt': records[0][3],
                        'relatedPatentId': records[0][4]
                    },
                    {
                        'patentId': records[1][0],
                        'author': records[1][1],
                        'classification': records[1][2],
                        'registeredAt': records[1][3],
                        'relatedPatentId': records[1][4]
                    }
                ])
             
    def close(self): 
        self.__neo4jAdapter.closeConnection()
 