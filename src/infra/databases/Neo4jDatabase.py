from domain.db.adapters.Neo4jAdpater import Neo4jAdpater
from domain.config.Settings import Settings
from domain.db.scripts.Neo4jScripts import Neo4jScripts

class Neo4jDatabase:
    def init(self):
        self.__neo4jAdapter = Neo4jAdpater(Settings.NEO4J_URI, Settings.NEO4J_USER, Settings.NEO4J_PASSWORD)
        commands = ()
        #self.__neo4jAdapter.executeDdls(commands)
    
    def setRecords(self, records):
        for record in records:
            #if not self.__neo4jAdapter.executeDql(PostgreSqlScripts.FIND_PATENT_BY_ID, (record[0])):
                #self.__insertPatentRecord(record[0], record[1], record[2], record[3])
        #self.__insertCitationRecord(records[0][0], records[1][0])  
  
    def close(self): 
        self.__neo4jAdapter.closeConnection() 
                  
    #def __insertPatentRecord(self, id, author, classification, registeredAt):
        #self.__neo4jAdapter.executeDml(PostgreSqlScripts.INSERT_INTO_PATENT, (id, author, classification, registeredAt))  
    
    #def __insertCitationRecord(self, fromId, toId):
        #self.__neo4jAdapter.executeDml(PostgreSqlScripts.INSERT_INTO_CITATION, (fromId, toId))
 