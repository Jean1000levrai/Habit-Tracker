import sqlite3 as sql
import habit_mgr as hmgr
from functions import *
from calendar_db import *

# -----------creation/drop-----------
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
                question TEXT,
                reminder BOOLEAN,
                description TEXT,
                unit TEXT,
                quantity REAL,
                threshold REAL,
                is_measurable BOOLEAN,
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



# -----------add/delete/update-----------

def add_habit(habit, user=''):
    """Add a habit into the database safely for the yes no"""
    info = hab_info(habit) 
    print(info)
    print(len(info))

    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""
        INSERT INTO habits_{user} (name, question, reminder, description)
        VALUES (?, ?, ?, ?)
    """, info[:4])

    cur.execute(f"""
        INSERT INTO habit_days_{user} (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, info[4][3])
    
    conn.commit()
    conn.close()

def add_habit_m(habit, user=''):
    """Add a habit into the database safely for the measurables"""
    info = hab_info_m(habit) 
    print(info)
    print(len(info))

    conn = connect_to_db()
    cur = conn.cursor()

    print("_________________________________________________")
    print(info[:7]+[True])

    cur.execute(f"""
        INSERT INTO habits_{user} 
        (name, question, reminder, description, unit, quantity, threshold, is_measurable)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, info[:7]+[True])

    cur.execute(f"""
        INSERT INTO habit_days_{user} (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, info[-1][3])
    
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

def update(hab, old_name, user=''):
    """Update a habit's info in the database."""
    conn = connect_to_db()
    cur = conn.cursor()

    info = hab_info(hab)
    # info = [name, colour, question, reminder, description, frequency]

    # Fetch id by name
    cur.execute(f"SELECT id FROM habits_{user} WHERE name = ?", (old_name,))
    row = cur.fetchone()
    print(row)
    if not row:
        conn.close()
        raise ValueError("Habit not found")
    habit_id = str(row[0])

    cur.execute(f"""
        UPDATE habits_{user}
        SET name = ?, question = ?, description = ?
        WHERE id = ?
    """, (info[0], info[1], info[3], habit_id))

    conn.commit()
    conn.close()



# -----------get-----------

# ----for functions----
def hab_info(hab = hmgr.HabitYesNo()):
    """function that takes a habityesno is param,
    returns every attributes of it. used for sql"""
    return [hab.name,
            hab.question,
            hab.reminder,
            hab.description,
            hab.frequency]

def hab_info_m(hab = hmgr.HabitMeasurable()):
    """function taht takes a HabitMeasurable is param,
    returns every attributes of it. used for sql"""
    return [hab.name,
            hab.question,
            hab.reminder,
            hab.description,
            hab.unit,
            hab.threshold,
            hab.quantity,
            hab.frequency
            ]

def get_info_hab(hab_name, attr, user=''):
    """function that takes the name and an attribute
    of a habit, returns the value of the attribute"""
    # connect to the db
    conn = connect_to_db()
    cur = conn.cursor()
    
    # check if attr is valid, prevent sql injection
    allowed_attr = ["question", "reminder", "description", "frequency",
                     "id", "unit", "quantity", "threshold", "is_measurable"]
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

# ----for ui/debug----
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



# -----------else-----------











# -----------main-----------
if __name__ == "__main__":
    hab = hmgr.HabitYesNo("runnnn")
    create_db("bebouu")
    create_db('')
    create_db('jean')
    # delete_habit("*", "easydoor")
    # print(get_habits_with_days("jen"))
    print("--------------------")
    # print(get_habits_with_days(""))
    # print(get_info_hab())
    