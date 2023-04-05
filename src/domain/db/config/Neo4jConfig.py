import yaml

class Neo4jConfig(object):
    with open("../../../settings.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
    uri = cfg["db"]["neo4j"]["uri"]
    user = cfg["db"]["neo4j"]["user"]
    password = cfg["db"]["neo4j"]["password"]
