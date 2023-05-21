from domain.config.Settings import Settings
from adapters.PgAdapter import PgAdapter
from scripts.PostgreSqlScripts import PostgreSqlScripts

class PostgreSqlDatabase:
    def init(self):
        self.__pgAdapter = PgAdapter(Settings.DB_POSTGRESQL_CONN_STR)
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
            self.__pgAdapter.executeDml(
                PostgreSqlScripts.INSERT_INTO_PATENT, (record[0], record[1], record[2], record[3],))
        self.__pgAdapter.executeDml(
            PostgreSqlScripts.INSERT_INTO_CITATION, (records[0][0], records[1][0],))
    
    def close(self): 
        self.__pgAdapter.closeConnection() 