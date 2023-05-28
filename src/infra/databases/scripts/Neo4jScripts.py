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
  GET_PATENT_BY_ID = "MATCH (p:patent {patent_id: $patentId}) RETURN p"
  GET_PATENTS_BY_AUTHOR = "MATCH (p:patent {author: $author}) RETURN p"
  FIND_TRIPLE_CITATION_PATH = """
    MATCH (p:patent)-[:CITE]->(relatedP:patent)<-[:CITE]-(coAuthor:patent)-[:CITE]->(otherP:patent)
    RETURN p.patent_id AS patentId,
          p.author AS author,
          collect(DISTINCT relatedP.patent_id) AS relatedPatents,
          collect(DISTINCT coAuthor.author) AS coAuthors,
          collect(DISTINCT otherP.patent_id) AS otherPatents
  """
  GET_PATENT_CITATIONS_BY_AUTHOR_AND_REGISTRATION_DATE = """
    MATCH (author:patent {author: $author})<-[:CITE]-(citingP:patent)
    WHERE citingP.registered_at >= $registration_date
    RETURN citingP
  """
  GET_PATENTS_COUNT_BY_CLASSIFICATION = """
    MATCH (p:patent)
    RETURN p.classification AS classification, count(*) AS count
  """
  GET_1000_LATEST_PATENTS_STATISTICS = """
    MATCH (:patent)-[:CITE]->(relatedP:patent)
    WITH COUNT(*) AS TotalGiven

    MATCH (relatedP:patent)-[:CITE]->(:patent)
    WITH TotalGiven, COUNT(*) AS TotalReceived

    MATCH (p:patent)
    OPTIONAL MATCH (p)-[:CITE]->(given:patent)
    WITH p,
        COUNT(DISTINCT given) AS GivenTotal,
        TotalGiven,
      TotalReceived

    OPTIONAL MATCH (received:patent)-[:CITE]->(p)
    WITH p,
        GivenTotal,
      TotalGiven,
        TotalReceived,
        COUNT(DISTINCT received) AS ReceivedTotal

    RETURN p.patent_id AS patentId,
          GivenTotal,
        ReceivedTotal,
          ROUND(toFloat(GivenTotal) / TotalGiven, 2) AS GivenPercentage,
          ROUND(toFloat(ReceivedTotal) / TotalReceived, 2) AS ReceivedPercentage
    ORDER BY p.registered_at DESC
    LIMIT 1000
  """
  GET_CITATIONS_FROM_THE_SAME_PATENTS_CLASSIFICATION = """
    MATCH (p:patent)-[:CITE]->(relatedP:patent)
    WHERE p.classification = relatedP.classification
    RETURN p.author AS citerPatentAuthor, p.patent_id AS citerPatentId, relatedP.author AS citedPatentAuthor, relatedP.patent_id AS citedPatentId, p.classification AS classification
  """