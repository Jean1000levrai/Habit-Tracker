import sqlite3 as sql
import habit_mgr as hmgr


def connect_to_db():
    return sql.connect("db_habit.db")

def create_db():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                colour TEXT,
                question TEXT,
                reminder BOOLEAN,
                description TEXT,
                frequency TEXT
            )
    """)
    conn.commit()
    conn.close()

def add_habits(hab):
    """add a habit into the database"""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(...)
    conn.commit()
    conn.close()

def delete_habits():
    """delete a habit from the database"""
    pass

def load_habits():
    pass

def save_habits():
    pass


new_hab = hmgr.HabitYesNo()