import pymysql

def get_db():
    ''' creates db connection '''

    db = pymysql.connect(user='admin',
                         password='adminadmin',
                         host='pets-db-instance-1.cxfxc7npxhrp.us-east-1.rds.amazonaws.com',
                         database='pets',
                         cursorclass=pymysql.cursors.DictCursor
                        )
    return db

def init_db():
    ''' initializes the db '''

    # read sql file
    sql_file = open('schema.sql', 'r').read()

    # get commands from file
    sql_commands = sql_file.split(';')

    db = get_db()
    cur = db.cursor()

    # execute each command
    for command in sql_commands:
        if command.strip() != '':
            cur.execute(command)

    db.commit()
