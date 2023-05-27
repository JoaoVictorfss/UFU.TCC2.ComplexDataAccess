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
  INSERT_INTO_PATENT_IF_NOT_EXIST = """
      INSERT INTO patent (patent_id, author, classification, registered_at)
      SELECT %s, %s, %s, %s
      WHERE NOT EXISTS (
        SELECT 1 FROM patent WHERE patent_id = %s
      )
  """
  INSERT_INTO_CITATION_IF_NOT_EXISTS = """
    INSERT INTO citation (from_id, to_id) 
    SELECT %s, %s
    WHERE NOT EXISTS (
      SELECT 1 FROM citation WHERE from_id = %s AND to_id = %s
    )
  """
  GET_PATENT_BY_ID = "SELECT * FROM patent WHERE patent_id = %s"
  GET_PATENTS_BY_AUTHOR = "SELECT * FROM patent WHERE author = %s"
  GET_PATENT_CITATIONS_BY_ID = """
      SELECT p.*
      FROM citation c
      INNER JOIN patent p ON c.from_id = p.patent_id
      WHERE c.to_id = %s
  """
  GET_PATENT_CITATIONS_BY_AUTHOR_AND_REGISTRATION_DATE = """
      SELECT p.*
      FROM citation c
      INNER JOIN patent p ON c.from_id = p.patent_id
      WHERE c.to_id IN (
          SELECT patent_id
          FROM patent
          WHERE author = %s
          AND registered_at >= %s
      )
  """
  GET_PATENTS_COUNT_BY_CLASSIFICATION = """
      SELECT classification, COUNT(*) AS Total FROM patent 
      GROUP BY classification
  """
  GET_1000_LATEST_PATENTS_STATISTICS = """
  		SELECT TOP 1000
			patent_id, 
			p.registered_at, 
			COUNT(c1) AS GivenTotal,
			ROUND(CAST(COUNT(c1) AS NUMERIC) / (SELECT COUNT(DISTINCT from_id) FROM citation) * 100, 2) AS GivenPercentage,
			COUNT(c2) AS ReceivedTotal,
			ROUND(CAST(COUNT(c2) AS NUMERIC) / (SELECT COUNT(DISTINCT to_id) FROM citation) * 100, 2) AS ReceivedPercentage
			FROM patent p
			LEFT JOIN citation as c1
				ON c1.from_id = p.patent_Id
			LEFT JOIN citation c2
				ON c2.to_id = p.patent_Id
			GROUP BY p.patent_id
			ORDER BY p.registered_at DESC
  """
  GET_CITATIONS_FROM_THE_SAME_PATENTS_CLASSIFICATION = """
      SELECT 
        p1.patent_id AS citerId,
        p1.author AS citerAuthor,
        p1.classification AS citerClassification,
        p2.patent_id AS citedPatentId,
        p2.author AS citedPatentAuthor,
        p2.classification AS citedClassification
			FROM patent p1 
			JOIN citation c ON p1.patent_id = c.from_id
			JOIN patent p2 ON c.to_id = p2.patent_id 
			WHERE p1.classification = p2.classification
"""