from code.controller import Controller
from code.database.database import Database

if __name__ == "__main__":

    db_name = 'data/sccTracker'

    # create database
    db = Database(db_name)

    # create application
    app = Controller(db_name)

    # start application
    app.run()
