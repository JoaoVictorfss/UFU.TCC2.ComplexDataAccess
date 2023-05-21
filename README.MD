# About
Complex data access performance analysis between PostgreSql and Neo4j

# Start 
 - pip3 install faker
 - pip3 install psycopg2
 - pip3 install neo4j

## Dataset
 - https://snap.stanford.edu/data/cit-Patents.html 
 - https://www.nber.org/research/data/us-patents
 
## Db Conectors
 - Neo4j: https://snap.stanford.edu/data/roadNet-CA.html 
 - PostgreSql: https://www.psycopg.org/docs/

## Anaconda
 - https://www.anaconda.com/products/distribution

## Links
 - https://towardsdatascience.com/create-a-graph-database-in-neo4j-using-python-4172d40f89c4
 - PostgreSql Database: https://api.elephantsql.com/console/10e20769-a11f-44b8-9721-a8304dcca3eb/details
 - https://www.elephantsql.com/plans.html
 - https://workspace-preview.neo4j.io/workspace/query

## Scripts
 - Clean Envirommet
    - MATCH (n) DETACH DELETE n
    - drop table patent, citation
 - Count 
    - select count(*) from patent
    - select count(*) from citation