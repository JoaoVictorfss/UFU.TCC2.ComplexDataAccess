import yaml
class Settings:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.db_config = self.config['db']
        self.data_config = self.config['data']
        self.results_config = self.config['results']
        self.tests_config = self.config['tests']

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config

    @property
    def postgresql_conn_str(self):
        return self.db_config['postgresql']['conn_str']

    @property
    def neo4j_uri(self):
        return self.db_config['neo4j']['uri']

    @property
    def neo4j_user(self):
        return self.db_config['neo4j']['user']

    @property
    def neo4j_password(self):
        return self.db_config['neo4j']['password']
    
    @property
    def fake_authors_total(self):
        return self.data_config['fake']['authorsTotal']

    @property
    def fake_classifications_total(self):
        return self.data_config['fake']['classificationsTotal']
    
    @property
    def fake_datetimes_total(self):
        return self.data_config['fake']['datetimesTotal']
    
    @property
    def dataset_start_date(self):
        return self.data_config['dataset']['start_date']

    @property
    def dataset_end_date(self):
        return self.data_config['dataset']['end_date']

    @property
    def dataset_total(self):
        return self.data_config['dataset']['total']

    @property
    def dataset_file_path(self):
        return self.data_config['dataset']['filePath']

    @property
    def data_max(self):
        return self.data_config['max']
    
    @property
    def results_base_path(self):
        return self.results_config['basePath']

    @property
    def tests_traversal_filters_patent_id(self):
        return self.tests_config['traversal']['filters']['patentId']
    
    @property
    def tests_traversal_filters_author(self):
        return self.tests_config['traversal']['filters']['author']
    
    @property
    def tests_traversal_filters_register_date(self):
        return self.tests_config['traversal']['filters']['registerDate']