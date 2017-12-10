#!/usr/bin/python
import psycopg2
import pandas as pd
from Common.config import config


def insert_data(cursor, insert_command, dengai_data):
    """ insert multiple vendors into the vendors table  """

    try:
        cursor.executemany(insert_command, dengai_data)
        print('Finished Inserting Data...')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
 
 
def create_tables(cursor, columns_command):
    """ create tables in the PostgreSQL database"""
    try:
        # create table one by one
        print('Creating Table...')
        cursor.execute(columns_command) 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

            
def database_connection(ini_path, columns_command, insert_command, dengai_data):
    """ create tables in the PostgreSQL database"""
    conn = None
    try:
        # read the connection parameters
        params = config(filename=ini_path)
        print('Connecting to the PostgreSQL database...')
        # connect to the PostgreSQL server
		  #
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        create_tables(cur, columns_command)
        # Insert data
        insert_data(cur, insert_command, dengai_data)

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

 
def main():
    table_command = ("CREATE TABLE training_labels" \
        "(city VARCHAR(2) NOT NULL," \
        "year INTEGER NOT NULL," \
        "weekofyear INTEGER NOT NULL," \
        "total_cases INTEGER NOT NULL)")
    datafilepath = ("D:\Analytics\GitHub\DengAI-Predicting Disease Spread" \
                    "\Data\dengue_labels_train.csv")
    data = pd.read_csv(datafilepath)
    values_command = ("INSERT INTO training_labels(city, year, weekofyear, total_cases) VALUES(%s, %s, %s, %s)")
    ini_filepath = 'database.ini'
    database_connection(ini_path=ini_filepath,
                        columns_command=table_command, 
                        insert_command=values_command, 
                        dengai_data=data.values)

    
if __name__ == '__main__':
    main()
