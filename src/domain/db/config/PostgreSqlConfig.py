import yaml

class PostgreSqlConfig(object):
    with open("../../../settings.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
    connStr = cfg["db"]["postgresql"]["connStr"]
