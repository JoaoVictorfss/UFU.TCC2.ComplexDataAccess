import yaml

# Configuration class to retrieve all data of the settings.yml
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
        return self.db_config['postgresql']['connStr']

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
    def fake_batchSize(self):
        return self.data_config['fake']['batchSize']
    
    @property
    def dataset_start_date(self):
        return self.data_config['dataset']['startDate']

    @property
    def dataset_end_date(self):
        return self.data_config['dataset']['endDate']

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
    def tests_filters_patent_id(self):
        return self.tests_config['filters']['patentId']
    
    @property
    def tests_filters_author(self):
        return self.tests_config['filters']['author']
    
    @property
    def tests_filters_registration_date(self):
        return self.tests_config['filters']['registrationDate']
    
    @property
    def tests_configure_db_enabled(self):
        return self.tests_config['configureDb']['enabled'] 
    
    @property
    def tests_data_load_enabled(self):
        return self.tests_config['dataLoad']['enabled']
    
    @property
    def tests_traversal_enabled(self):
        return self.tests_config['traversal']['enabled']  
    
    @property
    def tests_aggregation_enabled(self):
        return self.tests_config['aggregation']['enabled']
    
    @property
    def tests_patternMatching_enabled(self):
        return self.tests_config['patternMatching']['enabled']
    
    @property
    def tests_simple_enabled(self):
        return self.tests_config['simple']['enabled']       

    @property
    def tests_data_load_threads_max(self):
        return self.tests_config['dataLoad']['threadsMax']