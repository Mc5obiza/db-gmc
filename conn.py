import sqlite3
from contextlib import contextmanager
@contextmanager
def open_conn(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    yield conn
    conn.close()
    print('connevtion closed')
def select_all():
    with open_conn("app.db") as conn:
        cursor = conn.execute("""
        Select *
        from users
        """)
        rows = cursor.fetchall()
        print(rows)
    input("Your name")
select_all()