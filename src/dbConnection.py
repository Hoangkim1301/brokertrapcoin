import os
import sqlite3

def create_connection(db_file):
    """create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: connection object or None
    """
    conn = None
    # Check if the database file exists
    if os.path.exists(db_file):
        # Connect to the database
        conn = sqlite3.connect(db_file)
        print('Connection successful')
    else:
        print('Database does not exist')
    return conn

def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        conn.execute(create_table_sql)
        print('Table created')
    except sqlite3.Error as e:
        print(e)

#put to database table
def add(conn, query, data):
    """insert a row of data into the table
    :param conn: connection object
    :param query: an INSERT statement
    :param data: a tuple of values
    :return:
    """
    try:
        conn.execute(query, data)
        print('Data inserted')
    except sqlite3.Error as e:
        print(e)

def showDB(conn):
    res = conn.execute("SELECT * FROM users")  
    for row in res:  
        print(row)   
    conn.commit()           
    conn.close()
    
def clearDB(conn):
    conn.execute("DELETE FROM users")
    conn.commit()
    print('Show database after clear:')
    showDB(conn)
    conn.close()
    
def testConnecDB():
    conn = create_connection(r"finance.db")
    query = r"""CREATE TABLE IF NOT EXISTS ress (
                            id integer PRIMARY KEY,
                            resname text NOT NULL,
                            password text NOT NULL
                            );"""                   
    if conn is not None:
        create_table(conn, query)
    
    res = conn.execute("SELECT * FROM users")  
    for row in res:  
        print(row)   
    conn.commit()           
    conn.close()
    
def importDB(conn):
    query = r"""CREATE TABLE IF NOT EXISTS ress (
                            id integer PRIMARY KEY,
                            resname text NOT NULL,
                            password text NOT NULL
                            );"""                   
    if conn is not None:
        create_table(conn, query)
    
    query = r'''INSERT INTO users (id, resname, password)
                VALUES 
                ('1','kimlonghoang','12345'),
                ('2','hoanganhnguyen','12345'),
                ('3','minhducpham','12345'),
                ('4','phuongthaonguyen','12345');'''
    res = conn.execute("SELECT * FROM users")  
    for row in res:  
        print(row)   
    conn.commit()           
    conn.close()
    
#main
if __name__ == '__main__':
    '''
    TEST DATABASE BLOCK
    '''
    conn = create_connection(r"finance.db")
    
    add(conn, "CREATE TABLE IF NOT EXISTS stocks (user_id integer NOT NULL, symbol STRING, shares INTEGER, price DOUBLE, transaction INTEGER, name STRING;", ())
        
    conn.commit() 
    conn.close()    
    
    
    
    
    