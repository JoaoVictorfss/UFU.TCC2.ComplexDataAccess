class PostgreSqlScripts:
  CREATE_TABLE_CITATION = """
                             CREATE TABLE IF NOT EXISTS citation(
                               from_id INT NOT NULL, 
                               to_id INT NOT NULL, 
                               CONSTRAINT fk_from_patent_id FOREIGN KEY(from_id)                   
                               REFERENCES patent(patent_id), 
                                  CONSTRAINT fk_to_patent_id FOREIGN KEY(to_id) 
                               REFERENCES patent(patent_id))
                          """
  CREATE_TABLE_PATENT = """
                           CREATE TABLE IF NOT EXISTS patent(
                             patent_id INT PRIMARY KEY NOT NULL UNIQUE, 
                             author VARCHAR(60) NOT NULL, 
                             classification VARCHAR(50) NOT NULL, 
                             registered_at TIMESTAMP NOT NULL)
                        """
  CREATE_INDEX_PATENT_ID = "CREATE INDEX IF NOT EXISTS idx_patent_id on patent USING btree (patent_id)"
  CREATE_INDEX_PATENT_AUTHOR = "CREATE INDEX IF NOT EXISTS idx_patent_author on patent(author)"
  CREATE_INDEX_PATENT_CLASSIFICATION = "CREATE INDEX IF NOT EXISTS idx_patent_classification on patent(classification)"
  CREATE_INDEX_PATENT_REGISTERED_DATE = "CREATE INDEX IF NOT EXISTS idx_patent_registered on patent(registered_at)"
  INSERT_INTO_PATENT = """
                          INSERT INTO patent (patent_id, author, classification, registered_at)
                          SELECT %s, %s, %s, %s
                          WHERE NOT EXISTS (
                            SELECT 1 FROM patent WHERE patent_id = %s
                          )
                       """
  INSERT_INTO_CITATION = "INSERT INTO citation (from_id, author, to_id) VALUES(%s,%s)"
  FIND_PATENT_BY_ID = "SELECT * FROM patent WHERE patent_id = %s"