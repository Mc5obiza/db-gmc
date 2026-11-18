import sqlite3
from contextlib import contextmanager
from datetime import datetime
class DBServiceError(Exception):
    def __init__(self,kind,message):
        super().__init__(message)
        self.kind = kind
        self.message = message
@contextmanager
def open_conn(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    try:
        yield conn
    finally:
        conn.close()
    print('connevtion closed')
def create_conversation(conn:sqlite3.Connection,title,user_id):
    isUser = conn.execute(
        """
        SELECT *
        from users
        where id = ?
        """,
        (user_id,)
    ).fetchall()
    if not isUser:
        raise DBServiceError(kind="not_found",message="User doesn t exist")
    cursor = conn.execute("INSERT INTO conversations (user_id,title) values (?,?)",
                          (user_id,title))
    conn.commit()
    return cursor.lastrowid
def add_message(conn:sqlite3.Connection,role,content,tokens_used,user_id=None,title="New convesation",conversation_id=None):
    if role not in ('user','assistant','system'):
        raise DBServiceError("user","Role ")
    if not conversation_id:
        if user_id:
            conversation_id = create_conversation(conn,title,user_id)
        else:
            raise DBServiceError("Input_Error",message="User id can t be none")
    isConversation = conn.execute("""
        SELECT * 
        from conversations
        where id = ?
        """,(conversation_id,)).fetchall()
    if not isConversation:
        raise DBServiceError("not_found","Conversation id does not exist")
    update = conn.execute("""
        UPDATE conversations
        SET update_at = CURRENT_TIMESTAMP
        where id = ?
    """,(conversation_id,))
    cursor = conn.execute("INSERT INTO messages (conversation_id,role,content,tokens_used)" \
    "VALUES (?,?,?,?)",(conversation_id,role,content,tokens_used))
    conn.commit()
    return cursor.lastrowid

def see_tables(conn):
    
    cursor = conn.execute("""
        Select name
        from sqlite_schema
        where type = 'table'
        """)
    rows = cursor.fetchall()
    print(rows)
import sqlite3
def add_user(email,password_hash,conn:sqlite3.Connection):
    
    cursor = conn.execute("""
            SELECT * from users
    """)
    rows = cursor.fetchall()
    print(rows)
    isUser = conn.execute(f"""
        SELECT * 
        from users
        where  email= '{email}'
    """).fetchall()
    if isUser:
        raise DBServiceError(kind = "exist",message="User already exists")

    cursor = conn.execute(
            """
            INSERT INTO users (email,password_hash) values (?,?)
            """,
            (email,password_hash)
    )

    conn.commit()
    return cursor.lastrowid
def get_messages(conn:sqlite3.Connection,conversation_id):
    isConversation = conn.execute("""
        SELECT *
        from conversations
        where id = ?
        """,[conversation_id]).fetchall()
    if not isConversation:
        raise DBServiceError(kind="not_found",message="Conversation doesn t exist")
    cursor = conn.execute("""
        SELECT role,content
        from messages
        where conversation_id = ?
    """,[conversation_id])
    rows = cursor.fetchall()
    print(rows)
def see_users(conn):
    
    cursor = conn.execute(
            """
            SELECT * from users;
            """
    )
    rows = cursor.fetchall()
    print(rows)
if __name__ == "__main__":
    with open_conn("app.db") as conn:
        see_tables(conn)
        # add_user("exam@example.com","ex_hash",conn)
        # see_users(conn)
        get_messages(conn,1)
        create_conversation(conn,"Python",1)
        add_message(conn,"user","What is Python",256,1)