
import psycopg2
from configparser import ConfigParser

class AmaDB:
    """ Utility to connect to the database configured in database.ini """
    def __init__(self):
        self.connection =  None
        parser = ConfigParser()
        parser.read('database.ini')
        self.dbParameters = {}
        if parser.has_section('postgresql'):
            params = parser.items('postgresql')
            for param in params:
                self.dbParameters[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format('postgresql', 'database.ini'))

    def connect(self):
        """ Connect to Postgresql database"""
        self.connection = psycopg2.connect(**self.dbParameters)
        self.connection.autocommit = True