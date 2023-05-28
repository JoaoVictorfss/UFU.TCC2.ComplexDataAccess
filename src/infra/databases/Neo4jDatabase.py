from infra.databases.adapters.Neo4jAdpater import Neo4jAdpater
from infra.databases.scripts.Neo4jScripts import Neo4jScripts
from datetime import datetime

#Neo4j Database Manager
class Neo4jDatabase:
    #Creates a new connection
    def createConnection(self, settings):
        self._neo4jAdapter = Neo4jAdpater(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)
    
    def configureDb(self):
        commands = [
            Neo4jScripts.CREATE_INDEX_PATENT_ID,
            Neo4jScripts.CREATE_INDEX_PATENT_AUTHOR,
            Neo4jScripts.CREATE_INDEX_PATENT_CLASSIFICATION,
            Neo4jScripts.CREATE_INDEX_PATENT_REGISTERED_DATE
        ]
        self._neo4jAdapter.executeQueries(commands)
        
    #Creates patent's nodes and relationships
    def setRecords(self, records):
        rows = list(map(lambda record: {
            'patentId': record[0],
            'author': record[1],
            'classification': record[2],
            'registeredAt': record[3],
            'toNodeId': record[4]
        }, records))
        self._neo4jAdapter.executeTransaction(Neo4jScripts.CREATE_NODES_AND_RELATIONSHIP, rows)

    #Function to find triple citation paths. The goal is to identify cases where a patent is cited by another patent, this cited patent is in turn cited by a co-author, and this co-author cites a third patent.
    def findTripleCitationPath(self):
        return self._neo4jAdapter.executeQuery(Neo4jScripts.FIND_TRIPLE_CITATION_PATH)

    #Gets all patents that cite an author's patents on a given registration date
    def getPatentCitationsByAuthorAndRegistrationDate(self, author, date):
        return self._neo4jAdapter.executeQuery(Neo4jScripts.GET_PATENT_CITATIONS_BY_AUTHOR_AND_REGISTRATION_DATE, {"author": author, "registration_date": date})
    
    #Gets patent by id
    def getPatentById(self, patentId):
        return self._neo4jAdapter.executeQuery(Neo4jScripts.GET_PATENT_BY_ID, {"patentId": patentId})

    #Gets author's patents
    def getAuthorPatents(self, author):
        return self._neo4jAdapter.executeQuery(Neo4jScripts.GET_PATENTS_BY_AUTHOR, {"author": author})
  
    #Gets the amount and percentage of citations received and made for the top 1000 most recent patents
    def getTop1000LatestPatentsStatistics(self):
        return self._neo4jAdapter.executeQuery(Neo4jScripts.GET_1000_LATEST_PATENTS_STATISTICS)

    #Gets patent citations of the same classification
    def getPatentCitationsOfTheSameClassification(self):
        return self._neo4jAdapter.executeQuery(Neo4jScripts.GET_CITATIONS_FROM_THE_SAME_PATENTS_CLASSIFICATION)

    #Gets amount of patents per classification
    def getPatentsCountPerClassification(self):
        return self._neo4jAdapter.executeQuery(Neo4jScripts.GET_PATENTS_COUNT_BY_CLASSIFICATION)

    #Close driver's connection
    def closeConnection(self): 
        self._neo4jAdapter.closeConnection()
 