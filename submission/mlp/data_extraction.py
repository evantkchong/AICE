#!/usr/bin/python3
import os
import pyodbc
import pandas as pd
from sqlalchemy import MetaData, Table, create_engine

def show_all(df):
    '''
    Convenience function for printing entire content of a dataframe
    '''
    with pd.option_context('display.max_rows',
                            None,
                            'display.max_columns',
                            None):
        print(df)

class SQLHandler(object):
    def __init__(self,
                 server='aice.database.windows.net',
                 database='aice',
                 username='aice_candidate',
                 password='@ic3_a3s0c1at3',
                 table_name='rental_data'):
        self.df = None
        self.server = server
        self.database = database 
        self.username = username
        self.password = password
        self.table_name = table_name
        driver = 'ODBC+Driver+17+for+SQL+Server'

        # dialect+driver://username:password@host:port/database
        connection_str = 'mssql+pyodbc://{}:{}@{}:1433/{}?driver={}'.format(self.username,
                                                                            self.password,
                                                                            self.server,
                                                                            self.database,
                                                                            driver)
        print('Connecting to {}'.format(connection_str))

        # Create engine
        try:
            self.engine = create_engine(connection_str)
            print('Successfully connected.')
        except Exception as err:
            print('Database connection failed with error {}. Please check connection arguments'.format(err))
            raise err

    def extract(self,
                year_from=2011,
                year_to=2012,
                exclude_fields=['guest_bike', 'registered_bike']):
        '''
        Method for reading an SQL query on our engine into a DataFrame.
        '''
        # Obtain table metadata so that we can dynamically select
        # only the desired fields from the table
        metadata = MetaData()
        table = Table(self.table_name,
                      metadata,
                      autoload=True,
                      autoload_with=self.engine)
        columns = table.c

        print('Excluding the following columns: {}'.format(exclude_fields))
        include_list = [col.name for col in columns if col.name not in exclude_fields]

        # Dynamically construct query based on arguments and metadata
        # Construct select statement
        select_statement = ''
        for x in include_list:
            select_statement += ' {},'.format(x)
        select_statement = select_statement[:-1]

        # Construct filter by date range
        filter_statement = ''
        if 'date' in include_list and year_from and year_to:
            filter_statement = " WHERE date BETWEEN '{}' AND '{}'".format(year_from,
                                                                          year_to)
        else:
            # If there is no date in the columns list,
            # or no value is give for year_from and year_to,
            # we do not filter by year
            print('Ignoring filtering by year.')

        query = 'SELECT {} FROM {}{}'.format(select_statement,
                                             self.table_name,
                                             filter_statement)
        
        print('Using query `{}`'.format(query))
        # Pass query and engine to pandas
        self.df = pd.read_sql_query(query,
                               self.engine)
        return self.df

    def export(self,
               path=None):
        '''
        Convenience function for exporting the extracted dataframe to a csv file
        '''
        if path is None:
            path = os.path.join('..', '{}.csv'.format(self.table_name))

        print('Exporting data to {}'.format(path))
        self.df.to_csv(path)

if __name__ == "__main__":
    # If running this as a script, we use the default values in
    # the defined functions to extract the required dataset as specified
    # in the test document ie. data recorded between 2011 and 2012 inclusive, 
    # extracting all columns except guest_bike and registered_bike.
    # We then save the extracted values in `rental_data.csv` in the project root

    handle = SQLHandler()
    handle.extract()
    handle.export()
