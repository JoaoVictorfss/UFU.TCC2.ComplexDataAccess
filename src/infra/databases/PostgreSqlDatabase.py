from domain.db.adapters.PgAdapter import PgAdapter
from domain.config.Settings import Settings
from domain.db.scripts.PostgreSqlScripts import PostgreSqlScripts

class PostgreSqlDatabase:
    def init(self):
        self.__pgAdapter = PgAdapter(Settings.POSTGRESQL_CONN_STR)
        commands = (
            PostgreSqlScripts.CREATE_TABLE_PATENT,
            PostgreSqlScripts.CREATE_TABLE_CITATION,
            PostgreSqlScripts.CREATE_INDEX_PATENT_ID,
            PostgreSqlScripts.CREATE_INDEX_PATENT_AUTHOR,
            PostgreSqlScripts.CREATE_INDEX_PATENT_CLASSIFICATION,
            PostgreSqlScripts.CREATE_INDEX_PATENT_REGISTERED_DATE
        )
        self.__pgAdapter.executeDdls(commands)
    
    def setRecords(self, records):
        for record in records:
            if not self.__pgAdapter.executeDql(PostgreSqlScripts.FIND_PATENT_BY_ID, (record[0],)):
                self._insertPatentRecord(record[0], record[1], record[2], record[3])
        self._insertCitationRecord(records[0][0], records[1][0])  
  
    def close(self): 
        self.__pgAdapter.closeConnection() 
                  
    def _insertPatentRecord(self, id, author, classification, registeredAt):
        self.__pgAdapter.executeDml(PostgreSqlScripts.INSERT_INTO_PATENT, (id, author, classification, registeredAt,))  
    
    def _insertCitationRecord(self, fromId, toId):
        self.__pgAdapter.executeDml(PostgreSqlScripts.INSERT_INTO_CITATION, (fromId, toId,))
 