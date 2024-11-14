import sqlite3

def connect_to_db(database: str):
    conn = sqlite3.connect(database)
    curr = conn.cursor()
    return (conn, curr)