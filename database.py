import sqlite3 as sql
import habit_mgr as hmgr
from functions import *


def connect_to_db():
    return sql.connect(resource_path2("data/db_habit.db"))

def create_db():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                colour TEXT,
                question TEXT,
                reminder BOOLEAN,
                description TEXT,
                frequency TEXT
            )
    """)
    conn.commit()
    conn.close()

def print_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM habits")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def add_habit(habit):
    """Add a habit into the database safely."""
    info = hab_info(habit) 

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO habits (name, colour, question, reminder, description, frequency)
        VALUES (?, ?, ?, ?, ?, ?)
    """, info)

    conn.commit()
    conn.close()

def delete_habit(name = '*'):
    """delete a habit from the database"""
    conn = connect_to_db()
    cur = conn.cursor()
    if name == '*':
        cur.execute("""DELETE FROM habits
                WHERE id < 999999999999999""")
    else:
        cur.execute("""DELETE FROM habits
                WHERE name = ?""", (name,))
    
    conn.commit()
    conn.close()

def hab_info(hab = hmgr.HabitYesNo()):
    """function taht takes a habityesno is param,
    returns every attributes of it. used for sql"""
    return [hab.name,
            hab.colour,
            hab.question,
            hab.reminder,
            hab.description,
            hab.frequency]

def show_habit_for_gui(name):
    """function that takes the name or a star of a habit
    in parameter,returns every attribute' values of the
    habit or of every habits if a star"""
    # connect to the db
    conn = connect_to_db()
    cur = conn.cursor()

    # select everything if a *
    if name == "*":
        cur.execute("""SELECT * FROM habits""")
    # or just from one habit
    else:
        cur.execute("""SELECT * FROM habits
                    WHERE name = ?""", (name,))
    
    # recovers the values
    list_habits = cur.fetchall()

    conn.close()

    return list_habits

def get_info_hab(hab_name, attr):
    """function that takes the name and an attribute
    of a habit, returns the value of the attribute"""
    # connect to the db
    conn = connect_to_db()
    cur = conn.cursor()
    
    # check if attr is valid, prevent sql injection
    allowed_attr = ["question", "reminder", "description", "frequency", "created_at"]
    if attr not in allowed_attr:
        raise ValueError("invalid attribute, please try something else")

    # select the info
    exe = f"SELECT {attr} FROM habits WHERE name = ?"
    cur.execute(exe,(hab_name, ))
    rep = cur.fetchone()

    conn.close()
    if rep:
        return rep[0]
    return None

if __name__ == "__main__":
    hab = hmgr.HabitYesNo()
    create_db()
    # delete_habit()
    print_table()
    # print(get_info_hab())