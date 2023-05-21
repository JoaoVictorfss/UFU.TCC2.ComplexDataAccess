from infra.databases.adapters.Neo4jAdpater import Neo4jAdpater
from infra.databases.scripts.Neo4jScripts import Neo4jScripts
from datetime import datetime
class Neo4jDatabase:
    def init(self, settings):
        self.__neo4jAdapter = Neo4jAdpater(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)
        commands = [
            Neo4jScripts.CREATE_INDEX_PATENT_ID,
            Neo4jScripts.CREATE_INDEX_PATENT_AUTHOR,
            Neo4jScripts.CREATE_INDEX_PATENT_CLASSIFICATION,
            Neo4jScripts.CREATE_INDEX_PATENT_REGISTERED_DATE
        ]
        self.__neo4jAdapter.executeQueries(commands)
        
    def setRecords(self, records):
        rows = list(map(lambda record: {
            'patentId': record[0],
            'author': record[1],
            'classification': record[2],
            'registeredAt': record[3],
            'toNodeId': record[4]
        }, records))
        self.__neo4jAdapter.executeTransaction(Neo4jScripts.CREATE_NODES_AND_RELATIONSHIP, rows)

    def getPatentCitationsById(self, patentId):
        self.__neo4jAdapter.executeQuery(Neo4jScripts.GET_PATENT_CITATIONS_BY_ID, {"patent_id": patentId})

    def getPatentCitationsByAuthorAndRegisterDate(self, author, date):
        self.__neo4jAdapter.executeQuery(Neo4jScripts.GET_PATENT_CITATIONS_BY_AUTHOR_AND_REGISTER_DATE, {"author": author, "registered_at": date})
    
    def close(self): 
        self.__neo4jAdapter.closeConnection()
 