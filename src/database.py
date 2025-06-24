import sqlite3 as sql
import habit_mgr as hmgr
from functions import *
from calendar_db import *


def connect_to_db():
    return sql.connect(resource_path2("data/db_habit.db"))

def create_db(user=''):
    conn = connect_to_db()
    cur = conn.cursor()
    # main table
    cur.execute(f"""
            CREATE TABLE IF NOT EXISTS habits_{user} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                colour TEXT,
                question TEXT,
                reminder BOOLEAN,
                description TEXT,
                frequency TEXT
            )
    """)
    # days table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS habit_days_{user} (
            habit_id INTEGER PRIMARY KEY,
            monday BOOLEAN DEFAULT 0,
            tuesday BOOLEAN DEFAULT 0,
            wednesday BOOLEAN DEFAULT 0,
            thursday BOOLEAN DEFAULT 0,
            friday BOOLEAN DEFAULT 0,
            saturday BOOLEAN DEFAULT 0,
            sunday BOOLEAN DEFAULT 0,
            FOREIGN KEY(habit_id) REFERENCES habits_{user}(id) ON DELETE CASCADE
            )
    """)

    conn.commit()
    conn.close()

def get_habits_with_days(user=''):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT h.*, d.monday, d.tuesday, d.wednesday, d.thursday, d.friday, d.saturday, d.sunday
        FROM habits_{user} h
        LEFT JOIN habit_days_{user} d ON h.id = d.habit_id
    """)
    results = cur.fetchall()
    conn.close()
    return results

def print_table(user=''):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM habits_{user}")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def add_habit(habit, user=''):
    """Add a habit into the database safely."""
    info = hab_info(habit) 
    print(info)
    print(len(info))

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""
        INSERT INTO habits_{user} (name, colour, question, reminder, description)
        VALUES (?, ?, ?, ?, ?)
    """, info[:5])

    cur.execute(f"""
        INSERT INTO habit_days_{user} (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, info[5][3])
    
    conn.commit()
    conn.close()

def delete_habit(name = '*', user=''):
    """delete a habit from the database"""
    conn = connect_to_db()
    cur = conn.cursor()
    if name == '*':
        cur.execute(f"""DELETE FROM habits_{user}
                WHERE id < 999999999999999""")
    else:
        cur.execute(f"""DELETE FROM habits_{user}
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

def show_habit_for_gui(name, user=''):
    """function that takes the name or a star of a habit
    in parameter,returns every attribute' values of the
    habit or of every habits if a star"""
    # connect to the db
    conn = connect_to_db()
    cur = conn.cursor()

    # select everything if a *
    if name == "*":
        cur.execute(f"""SELECT * FROM habits_{user}""")
    # or just from one habit
    else:
        cur.execute(f"""SELECT * FROM habits_{user}
                    WHERE name = ?""", (name,))
    
    # recovers the values
    list_habits = cur.fetchall()

    conn.close()

    return list_habits

def get_info_hab(hab_name, attr, user=''):
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
    exe = f"SELECT {attr} FROM habits_{user} WHERE name = ?"
    cur.execute(exe,(hab_name, ))
    rep = cur.fetchone()

    conn.close()
    if rep:
        return rep[0]
    return None

def drop_all_tables(user=''):
    """Drops all tables related to the user in the database."""
    conn = connect_to_db()
    cur = conn.cursor()
    # Drop the main habits table
    cur.execute(f"DROP TABLE IF EXISTS habits_{user}")
    # Drop the days table
    cur.execute(f"DROP TABLE IF EXISTS habit_days_{user}")
    conn.commit()
    conn.close()

def update(hab, user=''):
    """Update a habit's info in the database."""
    conn = connect_to_db()
    cur = conn.cursor()

    info = hab_info(hab)
    # info = [name, colour, question, reminder, description, frequency]

    # Fetch id by name
    cur.execute(f"SELECT id FROM habits_{user} WHERE name = ?", (info[0],))
    row = cur.fetchone()
    print(row)
    if not row:
        conn.close()
        raise ValueError("Habit not found")
    habit_id = row[0]

    cur.execute(f"""
        UPDATE habits_{user}
        SET name = ?, question = ?, description = ?
        WHERE id = ?
    """, (info[0], info[2], info[4], habit_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    hab = hmgr.HabitYesNo("runnnn")
    # create_db("easydoor")
    create_db('')
    # delete_habit("*", "easydoor")
    # print(get_habits_with_days("jen"))
    print("--------------------")
    print(get_habits_with_days(""))
    # print(get_info_hab())