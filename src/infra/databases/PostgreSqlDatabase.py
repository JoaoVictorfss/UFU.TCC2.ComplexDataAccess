from infra.databases.adapters.PgAdapter import PgAdapter
from infra.databases.scripts.PostgreSqlScripts import PostgreSqlScripts

#PostgreSql Database Manager
class PostgreSqlDatabase:
    #Creates the database structure
    def init(self, settings):
        self.__pgAdapter = PgAdapter(settings.postgresql_conn_str)
        if(settings.tests_configure_db_enabled):
            commands = [
                PostgreSqlScripts.CREATE_TABLE_PATENT,
                PostgreSqlScripts.CREATE_TABLE_CITATION,
                PostgreSqlScripts.CREATE_INDEX_PATENT_ID,
                PostgreSqlScripts.CREATE_INDEX_PATENT_AUTHOR,
                PostgreSqlScripts.CREATE_INDEX_PATENT_CLASSIFICATION,
                PostgreSqlScripts.CREATE_INDEX_PATENT_REGISTERED_DATE
            ]
            self.__pgAdapter.executeDdls(commands)
    
    #Insert into patent and citation tables
    def setRecords(self, records):
        for record in records:
            self.__pgAdapter.executeDml(PostgreSqlScripts.INSERT_INTO_PATENT_IF_NOT_EXIST, (record[0], record[1], record[2], record[3], record[0],))
        
        self.__pgAdapter.executeDml(
            PostgreSqlScripts.INSERT_INTO_CITATION_IF_NOT_EXISTS, (records[0][0], records[1][0], records[0][0], records[1][0],))

    #Gets all patents that cite a specific one by id 
    def getPatentCitationsById(self, patentId):
        self.__pgAdapter.executeDql(PostgreSqlScripts.GET_PATENT_CITATIONS_BY_ID, (patentId,))
    
    #Gets all patents that cite an author's patents on a given registration date
    def getPatentCitationsByAuthorAndRegistrationDate(self, author, date):
        self.__pgAdapter.executeDql(PostgreSqlScripts.GET_PATENT_CITATIONS_BY_AUTHOR_AND_REGISTRATION_DATE, (author, date,))
    
    #Close driver's connection    
    def close(self): 
        self.__pgAdapter.closeConnection() 