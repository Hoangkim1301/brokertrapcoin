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
def insert(conn, query, data):
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

#main
if __name__ == '__main__':
    conn = create_connection(r"finance.db")
    
    query = r"""CREATE TABLE IF NOT EXISTS users (
                            id integer PRIMARY KEY,
                            username text NOT NULL,
                            password text NOT NULL
                            );"""
                            
    if conn is not None:
        create_table(conn, query)
        
    #if conn is not None:
        #insert(conn, "INSERT INTO users (id, username, password) VALUES (?, ?, ?)", ("3","tommy", "admin"))
       
    res = conn.execute("SELECT * FROM USERS")  
    
    for row in res:  
        print(row)   
       
    conn.commit()           
    conn.close()