class Neo4jScripts:
  CREATE_INDEX_PATENT_ID = "CREATE INDEX IF NOT EXISTS ON :patent(patent_id)"
  CREATE_INDEX_PATENT_AUTHOR = "CREATE INDEX IF NOT EXISTS ON :patent(author)"
  CREATE_INDEX_PATENT_CLASSIFICATION = "CREATE INDEX IF NOT EXISTS ON :patent(classification)"
  CREATE_INDEX_PATENT_REGISTERED_DATE = "CREATE INDEX IF NOT EXISTS ON :patent(registered_at)"
  CREATE_CONSTRAINT_PATENT_ID = "CREATE CONSTRAINT patents IF NOT EXISTS ON (p:patent) ASSERT p.patent_id IS UNIQUE"
  FIND_PATENT_BY_ID = "MATCH (p:patent {patent_id: $patent_id}) RETURN p"
  CREATE_RELATIONSHIP_BETWEEN_NODES = """
                      UNWIND $rows AS row
                      MERGE (p:patent {patent_id: row.patentId})
                      ON CREATE SET p += {
                        author: row.author,
                        classification: row.classification,
                        registered_at: row.registeredAt
                      }
                      WITH p, row
                      WHERE row.relatedPatentId IS NOT NULL
                      MATCH (relatedP:patent {patent_id: row.relatedPatentId})
                      MERGE (p)-[:RELATED_TO]->(relatedP)
                      RETURN count(*) as total
                      """