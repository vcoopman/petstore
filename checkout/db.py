import sqlite3

def get_db():
    ''' creates db connection '''
    sqlite3_file = './storage/student-microservice.db'

    try:

        db = sqlite3.connect(sqlite3_file)
        db.row_factory = sqlite3.Row

    except Exception as ex:
        print("Error creating connection to student database")
        print(ex)

    return db

def init_db():
    ''' initializes the db '''

    db = get_db()
    sql_file = open('schema.sql')
    db.executescript(sql_file.read())
