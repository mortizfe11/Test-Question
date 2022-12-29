
from flask import render_template
import sqlite3 as sql

# connect to qa_database.sq (database will be created, if not exist)
def init_database(db_name, db_table):
    con = sql.connect(db_name)
    con.execute(f'CREATE TABLE IF NOT EXISTS {db_table} (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'question TEXT, answer TEXT)')
    con.close()

def connect_database(db_name, query):
    connection = sql.connect(db_name)    
    cursor =  connection.cursor() # cursor
    # insert data
    cursor.execute(query)  
    return connection, cursor

def send_query_within_response(db_name,query):
    try:
        con, _ = connect_database(db_name, query) 
        con.commit() # apply changes
    except con.Error as err: # if error
            # then display the error in 'database_error.html' page
        return err
    finally:
        con.close() # close the connection

def send_query_with_response(db_name, query, isAll = False):
    try:
        con, c = connect_database(db_name, query)
        if isAll:
            question = c.fetchall()
        else:
            question = c.fetchone()
        con.commit() # apply changes
        return question

    except con.Error as err: # if error
            # then display the error in 'database_error.html' page
        return err
    finally:
        con.close() # close the connection