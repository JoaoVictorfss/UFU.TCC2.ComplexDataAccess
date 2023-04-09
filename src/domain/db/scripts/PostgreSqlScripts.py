class PostgreSqlScripts:
  CREATE_TABLE_CITATION = "CREATE TABLE IF NOT EXISTS citation(from_id INT NOT NULL, to_id INT NOT NULL)"
  CREATE_TABLE_PATENT = "CREATE TABLE IF NOT EXISTS patent(patent_id INT PRIMARY KEY NOT NULL, author VARCHAR(20) NOT NULL, name VARCHAR(20) NOT NULL, registered_at TIMESTAMP NOT NULL)"
  CREATE_INDEX_PATENT_ID = "CREATE INDEX IF NOT EXISTS idx_patent_id on patent USING btree (patent_id)"
  CREATE_INDEX_PATENT_AUTHOR = "CREATE INDEX IF NOT EXISTS idx_patent_author on patent(author)"
  CREATE_INDEX_PATENT_NAME = "CREATE INDEX IF NOT EXISTS idx_patent_name on patent(name)"
  CREATE_INDEX_PATENT_REGISTERED_DATE = "CREATE INDEX IF NOT EXISTS idx_patent_registered on patent(registered_at)"