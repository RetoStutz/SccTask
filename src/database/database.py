import pandas as pd
import sqlite3
import re

excel_file_path_tracker_list = "data/workitemsExport.xlsx"
excel_file_path_sap = "data/export.xlsx"


def drop_all_tables(cursor):
    # Get a list of all table names in the database
    query = """SELECT name FROM sqlite_master WHERE type='table';"""
    cursor.execute(query)
    tables = cursor.fetchall()

    # Drop each table
    for table in tables:
        table_name = table[0]
        if table_name != 'sqlite_sequence':  # sqlite_sequence is used for autoincrement and can not be removed from DB
            drop_query = f"DROP TABLE IF EXISTS {table_name};"
            cursor.execute(drop_query)


def import_data_from_polarion_task(con, cursor, file_path):
    try:
        # read data from excel
        excel_data = pd.read_excel(file_path, sheet_name=None)

        for sheet_name, data in excel_data.items():
            # Iterate over rows and insert into SQLite table
            for index, row in data.iterrows():

                # Insert into database based on 'Type'
                if row.get('Type') == 'User Story':
                    parent_id = find_number_in_string(row.get('Linked Work Items'), "specifies:")
                    cursor.execute(
                        "INSERT INTO Story (sccId, name, parentSccId) VALUES (?, ?, ?)",
                        (row['ID'], row['Title'], parent_id))

                elif row.get('Type') == 'Epic':
                    cursor.execute(
                        "INSERT INTO Epic (sccId, name) VALUES (?, ?)",
                        (row['ID'], row['Title']))

                elif row.get('Type') == 'Task':
                    parent_id = find_number_in_string(row.get('Linked Work Items'), "implements:")
                    cursor.execute(
                        "INSERT INTO Task (sccId, name, parentSccId) VALUES (?, ?, ?)",
                        (row['ID'], row['Title'], parent_id))
                else:
                    print(f"{row.get('Type')} is not part of database")

            con.commit()
    except Exception as e:
        print(f"Error during import data from {file_path}: {str(e)}")


def find_number_in_string(searchable_string, key_word):
    if isinstance(searchable_string, str):
        # Using regular expression to find numbers after the specified keyword
        pattern = re.compile(fr'{key_word} (\S+)', re.IGNORECASE)
        matches = pattern.findall(searchable_string)

        # Extracting the numbers
        if matches:
            return int(re.findall(r'\d+', matches[0])[0])  # Use \d+ to find all digits
        else:
            return 0
    else:
        return 0


class Database:

    def __init__(self, db_name):

        # switch for development, possibility to switch of import data for fast app start
        IMPORT_DATA_FROM_FILE = True

        # Connect to the SQLite database (or create a new one if it doesn't exist)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        if IMPORT_DATA_FROM_FILE:
            drop_all_tables(self.cursor)

        # Create Table Task
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                sccId INTEGER,
                parentSccId INTEGER,
                childSccId INTEGER,
                FOREIGN KEY (parentSccId) REFERENCES Story(name)
            )
        ''')

        # Create Table Story
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Story (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                sccId INTEGER,
                parentSccId INTEGER,
                childSccId INTEGER,
                FOREIGN KEY (parentSccId) REFERENCES Story(name)
            )
        ''')

        # Create Table Epic
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Epic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                sccId INTEGER,
                childSccId INTEGER
            )
        ''')

        # Commit the changes
        self.conn.commit()

        # import data from excel tables
        if IMPORT_DATA_FROM_FILE:
            import_data_from_polarion_task(self.conn, self.cursor, excel_file_path_tracker_list)

        # close connection
        self.conn.close()
