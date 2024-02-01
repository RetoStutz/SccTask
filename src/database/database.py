import pandas as pd
import sqlite3

excel_file_path_tracker_list = "data/workitemExport.xlsx"
excel_file_path_sap = "data/export.xlsx"

column_mapping_task = {
    'id': 'id',
    'name': 'name',
    'sccId': 'sccId',
    'parentTracker': 'parentTracker',
    'childTracker': 'childTracker'
}

column_mapping_function = {
    'name': 'name'
}


def execute_query(con, cursor, query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        con.commit()

        return True

    except sqlite3.Error as e:
        print(str(e))
        return False


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


def import_data_from_excel_table(con, cursor, file_path, table_name, column_mapping):
    try:
        # Read data from Excel
        excel_data = pd.read_excel(file_path, sheet_name=None)

        for sheet_name, data in excel_data.items():
            # Iterate over rows and insert into SQLite table
            for index, row in data.iterrows():
                columns = ', '.join(column_mapping.keys())
                values = ', '.join(['?'] * len(column_mapping))

                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                params = tuple(row[column_mapping[col]] for col in column_mapping)
                execute_query(con, cursor, query, params)

    except Exception as e:
        print(f"Error during import data from {file_path}: {str(e)}")


def import_data_from_excel_matrix(con, cursor, file_path, table_name, column_mapping, storeEntryToTable=1):
    try:
        # Read data from Excel
        excel_data = pd.read_excel(file_path, sheet_name=None)

        for sheet_name, data in excel_data.items():

            column_names = data.columns.tolist()

            # Iterate over rows and insert into SQLite table
            for _, row in data.iterrows():
                function_name = row.iloc[0]

                columns = ', '.join(column_mapping.keys())
                values = ', '.join(['?'] * len(column_mapping))

                # Iterate over non-first columns
                for column_index, cell_value in enumerate(row[1:], start=1):
                    if cell_value == storeEntryToTable:
                        # Insert into SQLite table
                        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                        params = (function_name, column_names[column_index])
                        execute_query(con, cursor, query, params)

    except Exception as e:
        print(f"Error during import data from {file_path}: {str(e)}")


def import_data_and_value_from_excel_matrix(con, cursor, file_path, table_name, column_mapping):
    try:
        # Read data from Excel
        excel_data = pd.read_excel(file_path, sheet_name=None)

        for sheet_name, data in excel_data.items():

            column_names = data.columns.tolist()

            # Iterate over rows and insert into SQLite table
            for _, row in data.iterrows():
                function_name = row.iloc[0]

                columns = ', '.join(column_mapping.keys())
                values = ', '.join(['?'] * len(column_mapping))

                # Iterate over non-first columns
                for column_index, cell_value in enumerate(row[1:], start=1):
                    if cell_value > 0:
                        # Insert into SQLite table
                        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                        params = (function_name, column_names[column_index], cell_value)
                        execute_query(con, cursor, query, params)

    except Exception as e:
        print(f"Error during import data from {file_path}: {str(e)}")


class Database:

    def __init__(self, db_name):

        # switch for development, possibility to switch of import data for fast app start
        IMPORT_DATA_FROM_FILE = True

        # Connect to the SQLite database (or create a new one if it doesn't exist)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        if IMPORT_DATA_FROM_FILE:
            drop_all_tables(self.cursor)

        # Create Table Crane
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Crane (
                craneId INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''')

        # Create Table Generator
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Generator (
                generatorId INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''')

        # Create Table Zone
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Element (
                elementId INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                generatorId INTEGER,
                FOREIGN KEY (generatorId) REFERENCES Generator(generatorId)
            )
        ''')

        # Create Table Typical
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Typical (
                typicalId INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                elementId INTEGER,
                elementName Text,
                craneId INTEGER,
                FOREIGN KEY (elementId) REFERENCES Element(elementId)
                FOREIGN KEY (craneId) REFERENCES Crane(craneId)      
            )
        ''')

        # Create Table Function
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Function (
                functionId INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                FOREIGN KEY (functionId) REFERENCES FunctionTypical(functionId)
            )
        ''')

        # Create Table Bmk
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Bmk (
                bmkId INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                plcName TEXT,
                plcCommentDe TEXT,
                plcCommentEn TEXT,
                polarionPage TEXT
            )
        ''')

        # Create Table BmkFunction
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BmkFunction (
                bmkFunctionId INTEGER PRIMARY KEY AUTOINCREMENT,
                bmkName TEXT,
                bmkId INTEGER,
                functionName TEXT,
                functionId INTEGER,
                FOREIGN KEY (bmkId) REFERENCES Bmk(bmkId),
                FOREIGN KEY (functionId) REFERENCES Function(functionId)
            )
        ''')

        # Create Table ExcludeFunction
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ExcludeFunction (
                  excludeFunctionId INTEGER PRIMARY KEY AUTOINCREMENT,
                  functionId  INTEGER,
                  functionName TEXT,
                  nonCompatibleFunctionId INTEGER,
                  nonCompatibleFunctionName TEXT,
                  FOREIGN KEY (functionId) REFERENCES Function(functionId)
            )
        ''')

        # Create Table FunctionTypical
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FunctionTypical (
                  functionTypicalId INTEGER PRIMARY KEY AUTOINCREMENT,
                  functionId INTEGER,
                  functionName TEXT,
                  typicalId INTEGER,
                  typicalName TEXT,
                  selection INTEGER,
                  FOREIGN KEY (typicalId) REFERENCES Typical(typicalId)
            )
        ''')

        # Commit the changes
        self.conn.commit()

        # import data from excel tables
        if IMPORT_DATA_FROM_FILE:
            import_data_from_excel_table(self.conn, self.cursor, excel_file_path_bmk, "Bmk", column_mapping_bmk)
            import_data_from_excel_table(self.conn, self.cursor, excel_file_path_function, "Function",
                                         column_mapping_function)
            import_data_from_excel_table(self.conn, self.cursor, excel_file_path_typical, "Typical",
                                         column_mapping_typical)
            import_data_from_excel_table(self.conn, self.cursor, excel_file_path_element, "Element",
                                         column_mapping_element)

            import_data_from_excel_matrix(self.conn, self.cursor, excel_file_path_excludeFunction, "ExcludeFunction",
                                          column_mapping_excludeFunction, 0)
            import_data_from_excel_matrix(self.conn, self.cursor, excel_file_path_bmk_function, "BmkFunction",
                                          column_mapping_bmkFunction, 1)
            import_data_and_value_from_excel_matrix(self.conn, self.cursor, excel_file_path_function_typical,
                                                    "FunctionTypical",
                                                    column_mapping_functionTypical)

        # close connection
        self.conn.close()
