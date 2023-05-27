from infra.databases.adapters.PgAdapter import PgAdapter
from infra.databases.scripts.PostgreSqlScripts import PostgreSqlScripts

#PostgreSql Database Manager
class PostgreSqlDatabase:
    #Creates the database structure
    def init(self, settings):
        self._pgAdapter = PgAdapter(settings.postgresql_conn_str)
        if(settings.tests_configure_db_enabled):
            commands = [
                PostgreSqlScripts.CREATE_TABLE_PATENT,
                PostgreSqlScripts.CREATE_TABLE_CITATION,
                PostgreSqlScripts.CREATE_INDEX_PATENT_ID,
                PostgreSqlScripts.CREATE_INDEX_PATENT_AUTHOR,
                PostgreSqlScripts.CREATE_INDEX_PATENT_CLASSIFICATION,
                PostgreSqlScripts.CREATE_INDEX_PATENT_REGISTERED_DATE
            ]
            self._pgAdapter.executeDdls(commands)
    
    #Insert into patent and citation tables
    def setRecords(self, records):
        for record in records:
            self._pgAdapter.executeDml(PostgreSqlScripts.INSERT_INTO_PATENT_IF_NOT_EXIST, (record[0], record[1], record[2], record[3], record[0],))
        
        self._pgAdapter.executeDml(
            PostgreSqlScripts.INSERT_INTO_CITATION_IF_NOT_EXISTS, (records[0][0], records[1][0], records[0][0], records[1][0],))

    #Gets all patents that cite a specific one by id 
    def getPatentCitationsById(self, patentId):
        return self._pgAdapter.executeDql(PostgreSqlScripts.GET_PATENT_CITATIONS_BY_ID, (patentId,))
    
    #Gets all patents that cite an author's patents on a given registration date
    def getPatentCitationsByAuthorAndRegistrationDate(self, author, date):
        return self._pgAdapter.executeDql(PostgreSqlScripts.GET_PATENT_CITATIONS_BY_AUTHOR_AND_REGISTRATION_DATE, (author, date,))
    
    #Gets patent by id
    def getPatentById(self, patentId):
        return self._pgAdapter.executeDql(PostgreSqlScripts.GET_PATENT_BY_ID, (patentId,))

    #Gets author's patents
    def getAuthorPatents(self, author):
        return self._pgAdapter.executeDql(PostgreSqlScripts.GET_PATENTS_BY_AUTHOR, (author,))
  
    #Gets the amount and percentage of citations received and made for the top 1000 most recent patents
    def getTop1000LatestPatentsStatistics(self):
        return self._pgAdapter.executeDql(PostgreSqlScripts.GET_1000_LATEST_PATENTS_STATISTICS)

    #Gets patent citations of the same classification
    def getPatentCitationsOfTheSameClassification(self):
        return self._pgAdapter.executeDql(PostgreSqlScripts.GET_CITATIONS_FROM_THE_SAME_PATENTS_CLASSIFICATION)

    #Gets amount of patents per classification
    def getPatentsCountPerClassification(self):
        return self._pgAdapter.executeDql(PostgreSqlScripts.GET_PATENTS_COUNT_BY_CLASSIFICATION)

    #Close driver's connection    
    def close(self): 
        self._pgAdapter.closeConnection() 