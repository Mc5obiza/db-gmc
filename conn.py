import sqlite3
from contextlib import contextmanager
@contextmanager
def open_conn(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    yield conn
    conn.close()
    print('connevtion closed')
def see_tables():
    with open_conn("app.db") as conn:
        cursor = conn.execute("""
        Select name
        from sqlite_schema
        where type = 'table'
        """)
        rows = cursor.fetchall()
        print(rows)
see_tables()