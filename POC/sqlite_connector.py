# Create SQLite database and connect using sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import os

# Create a method which creates SQLite database and connect using sqlalchemy
def create_sqlite_db():
    # Create SQLite database
    # check if data folder exists and create if not
    if not os.path.exists('../data'):
        os.makedirs('../data')
    # check if database exists and create if not
    if not os.path.exists('../data/stock_1506.db'):
        open('../data/stock_1506.db', 'w').close()
    engine = create_engine('sqlite:///../data/stock_1506.db', echo=True)
    # Connect to SQLite database
    sqlite_connection = engine.connect()
    return sqlite_connection

# Create a method which creates a table in SQLite database
def create_sqlite_table(sqlite_connection, table_name, df):
    # Create a table in SQLite database
    sqlite_table = table_name
    # Convert dataframe to SQL table
    df.to_sql(sqlite_table, sqlite_connection, if_exists='append')

# Create a method which reads a table from SQLite database
def read_sqlite_table(sqlite_connection, table_name):
    # Read table from SQLite database
    sqlite_table = table_name
    # Convert SQL table to dataframe
    df = pd.read_sql_table(sqlite_table, sqlite_connection)
    return df

# Create a method which deletes a table from SQLite database
def delete_sqlite_table(sqlite_connection, table_name):
    # Delete table from SQLite database
    sqlite_table = table_name
    # Delete SQL table
    sqlite_connection.execute(f'DROP TABLE {sqlite_table}')

# Create a method which updates a table in SQLite database
def update_sqlite_table(sqlite_connection, table_name, df):
    # Update table in SQLite database
    sqlite_table = table_name
    # Update SQL table
    df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')