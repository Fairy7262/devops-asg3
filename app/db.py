import sqlite3

def init_db():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS messages(msg TEXT)")
    conn.commit()
    conn.close()

def add_msg(m):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages VALUES(?)", (m,))
    conn.commit()
    conn.close()

def get_msgs():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT msg FROM messages")
    d = c.fetchall()
    conn.close()
    return d
