# Complex Data Access Test Application

## Overview
This application aims to automate complex data access tests between Neo4j and PostgreSQL DBMSs and return the results. It provides a streamlined process for setting up the databases, generating fake data, establishing relationships, and executing performance tests.

## Functionality
The application performs the following steps based on the provided configuration:

1. Database Setup: Using the settings.yml file, the application structures the databases by creating tables, indexes, constraints, nodes, and relationships.

2. Data Preprocessing: After the database structure is created, the application preprocesses the data by generating fake data according to the parameters specified in the settings.yml file. It establishes relationships between patents using a tuple based on the IDs provided in the dataset.txt file.

3. Performance Tests: With the database structure and preprocessed data in place, the application performs three tests from two categories:

   - Data Loading Test: This test measures the performance of loading the preprocessed data into the databases.

   - Traversal Test: This test measures the performance of traversing the databases. It consists of two subtests:
     - Subtest 1: Retrieve all patents that mention a specific patent based on its ID.
     - Subtest 2: Retrieve all patents that mention patents from a specific author on a particular date.

4. Results: The performance results are stored in CSV files, with one file generated for each test type and DBMS. The output path for the result files is specified in the settings.yml file.

## Usage
Follow these steps to use the application:

1. Clone the repository and navigate to the project directory.
2. Update the settings.yml file with the desired configuration parameters.
3. Place the dataset.txt file with the required IDs for establishing relationships between patents.
4. Run the application
   - Install all dependencies
    ```
    $ pip3 install faker psycopg2 neo4j pyyaml python-csv
    ```
   - Run the program
    ```
    $ cd src
    $ python3 main.py
    ```
5. Once the tests are complete, check the specified output path for the generated CSV result files.

## Dependencies
- [Neo4j Driver](https://neo4j.com/docs/api/python-driver/current/)
- [PostgreSQL Driver](https://www.psycopg.org/)
- [Faker](https://pypi.org/project/Faker/)
- [PyYAML](https://pypi.org/project/PyYAML/)
- [CSV](https://docs.python.org/3/library/csv.html)


## Links
 - [Console Elephant](https://api.elephantsql.com/console/10e20769-a11f-44b8-9721-a8304dcca3eb/details)
 - [Console Neo4j](https://workspace-preview.neo4j.io/workspace/query)
 - [Stanford Cit Patents Dataset](https://snap.stanford.edu/data/cit-Patents.html)

## Scripts
 - Delete
    - MATCH (n) DETACH DELETE n
    - drop table patent, citation

## License
This application is released under the [MIT License](LICENSE).
