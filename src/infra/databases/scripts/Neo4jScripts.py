class Neo4jScripts:
  CREATE_INDEX_PATENT_ID = "CREATE INDEX IF NOT EXISTS FOR (p:patent) ON (p.patent_id)"
  CREATE_INDEX_PATENT_AUTHOR = "CREATE INDEX IF NOT EXISTS FOR (p:patent) ON (p.author)"
  CREATE_INDEX_PATENT_CLASSIFICATION = "CREATE INDEX IF NOT EXISTS FOR (p:patent) ON (p.classification)"
  CREATE_INDEX_PATENT_REGISTERED_DATE = "CREATE INDEX IF NOT EXISTS FOR (p:patent) ON (p.registered_at)"
  CREATE_NODES_AND_RELATIONSHIP = """
    UNWIND $rows AS row
    MERGE (p:patent {patent_id: row.patentId})
    ON CREATE SET p += {
      author: row.author,
      classification: row.classification,
      registered_at: row.registeredAt
    }
    WITH p, row
    WHERE row.toNodeId IS NOT NULL
    MATCH (relatedP:patent {patent_id: row.toNodeId})
    MERGE (p)-[:CITE]->(relatedP)
    RETURN count(*) as total
  """
  GET_PATENT_BY_ID = "MATCH (p:patent {patent_id: $patent_id}) RETURN p"
  GET_PATENTS_BY_AUTHOR = ""
  GET_PATENT_CITATIONS_BY_ID = """

  """
  GET_PATENT_CITATIONS_BY_AUTHOR_AND_REGISTRATION_DATE = """

  """
  GET_PATENTS_COUNT_BY_CLASSIFICATION = ""
  GET_1000_LATEST_PATENTS_STATISTICS = ""
  GET_CITATIONS_FROM_THE_SAME_PATENTS_CLASSIFICATION = ""