import sqlite3 as sql
from datetime import datetime, timedelta
import json

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
                threshold REAL,
                is_measurable BOOLEAN,
                frequency TEXT
            )
    """)
    # days table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS habit_days_{user} (
            habit_id INTEGER PRIMARY KEY,
            monday BOOLEAN DEFAULT 1,
            tuesday BOOLEAN DEFAULT 1,
            wednesday BOOLEAN DEFAULT 1,
            thursday BOOLEAN DEFAULT 1,
            friday BOOLEAN DEFAULT 1,
            saturday BOOLEAN DEFAULT 1,
            sunday BOOLEAN DEFAULT 1,
            FOREIGN KEY(habit_id) REFERENCES habits_{user}(id) ON DELETE CASCADE
            )
    """)

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS habit_logs_{user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            quantity REAL,
            is_completed BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY(habit_id) REFERENCES habits_{user}(id) ON DELETE CASCADE,
            UNIQUE(habit_id, date)
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
    # Drop the logs table
    cur.execute(f"DROP TABLE IF EXISTS habit_logs_{user}")
    conn.commit()
    conn.close()



# -----------add/delete/update-----------

def add_habit(habit, user=''):
    """Add a habit into the database safely for the yes no"""
    info = hab_info(habit) 

    conn = connect_to_db()
    cur = conn.cursor()

    # insert the actual habit
    cur.execute(f"""
        INSERT INTO habits_{user} (name, question, reminder, description)
        VALUES (?, ?, ?, ?)
    """, info[:4])

    # insert the days where the habit is active
    cur.execute(f"""
        INSERT INTO habit_days_{user} (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, info[4][3])

    # insert the logs
    if info[4][3][datetime.today().weekday()] == 1:
        cur.execute(f"""
            SELECT id FROM habits_{user}
            WHERE name = ?""",(info[0],))
        habit_id = cur.fetchone()[0]

        date = datetime.today().strftime("%Y-%m-%d")
        cur.execute(f"""
                    INSERT OR IGNORE INTO habit_logs_{user}
                    (habit_id, date, quantity, is_completed)
                    VALUES (?, ?, ?, ?)
                """, (habit_id, date, 0, 0))
    
    conn.commit()
    conn.close()

def add_habit_m(habit, user=''):
    """Add a habit into the database safely for the measurables"""
    info = hab_info_m(habit) 

    conn = connect_to_db()
    cur = conn.cursor()

    # insert the actual habit
    cur.execute(f"""
        INSERT INTO habits_{user} 
        (name, question, reminder, description, unit, threshold, is_measurable)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, info[:6]+[True])

    # insert the days where the habit is active
    cur.execute(f"""
        INSERT INTO habit_days_{user} (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, info[-1][3])
    
    conn.commit()
    conn.close()

def create_new_day(date = datetime.today(), user=''):
    """called in main program each time the app is launched
    check if it is a new day, if it is: adds a new date to the db
    if not, does nothing"""
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""
            SELECT h.name, h.id, d.monday, d.tuesday, d.wednesday, d.thursday, d.friday, d.saturday, d.sunday
            FROM habits_{user} h LEFT JOIN habit_days_{user} d
            ON h.id = d.habit_id
        """)
    habits = cur.fetchall()

    print(habits)

    for habit in habits:
        # insert the logs
        if habit[date.weekday() + 2] == 1:

            date = date.strftime("%Y-%m-%d")
            cur.execute(f"""
                        INSERT OR IGNORE INTO habit_logs_{user}
                        (habit_id, date, quantity, is_completed)
                        VALUES (?, ?, ?, ?)
                    """, (habit[1], date, 0, 0))
    conn.commit()
    conn.close()

def delete_habit(name = '*', user=''):
    """delete a habit from the database"""
    conn = connect_to_db()
    cur = conn.cursor()
    if name == '*':
        cur.execute(f"""DELETE FROM habits_{user}
                WHERE id < 999999999999999""")
        cur.execute(f"""DELETE FROM habit_logs_{user}
                WHERE id < 999999999999999""")
        
    else:
        cur.execute(f"""SELECT id FROM habits_{user}
                WHERE name = ?""", (name,))
        id_hab = cur.fetchone()[0]
        cur.execute(f"""DELETE FROM habits_{user}
                WHERE name = ?""", (name,))
        cur.execute(f"""DELETE FROM habit_logs_{user}
                WHERE habit_id = ?""", (id_hab,))
    
    conn.commit()
    conn.close()

# update
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

def update_m(hab, old_name, user=''):
    """Update a habit's info in the database."""
    conn = connect_to_db()
    cur = conn.cursor()

    info = hab_info_m(hab)
    # info = [name, question, reminder, description, unit, threshold, quantity, frequency]

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
        SET name = ?, question = ?, description = ?, unit = ?, threshold = ?, quantity = ?
        WHERE id = ?
    """, (info[0], info[1], info[3], info[4], info[5], info[6], habit_id))

    conn.commit()
    conn.close()

def valid(hab_name, date, val=1, user=''):
    conn = connect_to_db()
    cur = conn.cursor()

    # Get the habit_id from the habit name
    cur.execute(f"SELECT id FROM habits_{user} WHERE name = ?", (hab_name,))
    result = cur.fetchone()
    if result is None:
        conn.close()
        raise ValueError(f"Habit '{hab_name}' not found.")

    habit_id = result[0]

    # Update the log entry
    cur.execute(f"""
        UPDATE habit_logs_{user}
        SET is_completed = ?
        WHERE habit_id = ? AND date = ?
    """, (val, habit_id, date))

    conn.commit()
    conn.close()

def add_quantity(hab_name, date, quantity, user=''):
    conn = connect_to_db()
    cur = conn.cursor()

    # Get the habit_id and threshold
    cur.execute(f"SELECT id, threshold FROM habits_{user} WHERE name = ?", (hab_name,))
    result = cur.fetchone()
    if result is None:
        conn.close()
        raise ValueError(f"Habit '{hab_name}' not found.")
    
    habit_id, threshold = result

    # Update the log quantity
    # is_completed only true if quantity is greater than threshold
    cur.execute(f"""
        UPDATE habit_logs_{user}
        SET quantity = ?, is_completed = ?
        WHERE habit_id = ? AND date = ?
    """, (quantity, int(quantity >= threshold), habit_id, date))

    conn.commit()
    conn.close()




# -----------get-----------

# for functions
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

# for debug
def print_habits_everuthing(user=''):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT h.*, d.monday, d.tuesday, d.wednesday, d.thursday, d.friday, d.saturday, d.sunday, l.*
        FROM habits_{user} h
        LEFT JOIN habit_days_{user} d ON h.id = d.habit_id
        LEFT JOIN habit_logs_{user} l ON h.id = l.habit_id
    """)
    results = cur.fetchall()
    conn.close()
    for row in results:
        print(row)

def print_logs(user=''):
    '''prints out the logs/date of the habits 
    (each different days that the habit has been used) db for debug'''
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""
                SELECT * FROM habit_logs_{user} ORDER BY date ASC
                """)

    result = cur.fetchall()
    conn.close()
    for row in result:
        print(row)

def print_days(user=''):
    '''prints out the days of the habits db for debug'''
    conn = connect_to_db()
    cur = conn.cursor()

def print_table(user=''):
    '''prints out the habits db for debug'''
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM habits_{user}")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# ui
# select
def show_habit_for_gui(name = '*', user=''):
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

def sort_by_alpha(name='*', user=''):
    # connect to the db
    conn = connect_to_db()
    cur = conn.cursor()

    # select everything if a *
    if name == "*":
        cur.execute(f"""SELECT * FROM habits_{user} 
                    ORDER BY name""")
    # or just from one habit
    else:
        cur.execute(f"""SELECT * FROM habits_{user}
                    WHERE name = ? 
                    ORDER BY name""", (name,))
    
    # recovers the values
    list_habits = cur.fetchall()

    conn.close()

    return list_habits

def sort_by_time(name='*', user=''):
    # connect to the db
    conn = connect_to_db()
    cur = conn.cursor()

    # select everything if a *
    if name == "*":
        cur.execute(f"""SELECT * FROM habits_{user} 
                    ORDER BY name""")
    # or just from one habit
    else:
        cur.execute(f"""SELECT * FROM habits_{user}
                    WHERE name = ? 
                    ORDER BY name""", (name,))
    
    # recovers the values
    list_habits = cur.fetchall()

    conn.close()

    return list_habits

# utils
def nb_hab(user = ''):
    # connect to the db
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""
            SELECT COUNT(*) FROM habits_{user}
        """)
    count = cur.fetchone()[0]
    
    conn.close()
    return count

def nb_dates(user = ''):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""
            SELECT COUNT(DISTINCT date) FROM habit_logs_{user} 
        """)
    count = cur.fetchone()[0]
    
    conn.close()
    return count

def get_all_habits(user=''):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"SELECT id, name FROM habits_{user}")
    habits = cur.fetchall()
    conn.close()
    return habits

def get_all_dates(user=''):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT date FROM habit_logs_{user} ORDER BY date ASC")
    dates = [row[0] for row in cur.fetchall()]
    conn.close()
    return dates

def check_log(habit_id, date, user=''):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT is_completed FROM habit_logs_{user}
        WHERE habit_id=? AND date=?
    """, (habit_id, date))
    row = cur.fetchone()
    conn.close()
    return bool(row[0]) if row else False

def habits_has_date(date, user=''):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""SELECT h.name 
                    FROM habits_{user} h 
                    LEFT JOIN habit_logs_{user} l 
                    ON h.id = l.habit_id
                    WHERE l.date = ?""", (date,))
    results = cur.fetchall()

    conn.close()

    return [row[0] for row in results]



# -----------else-----------

def insert_sample_data(user=''):
    conn = connect_to_db()
    cur = conn.cursor()

    habits = [
        ("Drink Water", "Did you drink enough water today?", 0, "Stay hydrated", "liters", 2.0, 1, "daily"),
        ("Exercise", "Did you exercise today?", 0, "Stay fit", "minutes", 30.0, 1, "daily"),
        ("Read", "Did you read today?", 0, "Develop your mind", "pages", 10.0, 1, "daily"),
    ]

    # Insert habits
    for habit in habits:
        cur.execute(f"""
            INSERT OR IGNORE INTO habits_{user} 
            (name, question, reminder, description, unit, threshold, is_measurable, frequency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, habit)

    # Get habit IDs
    cur.execute(f"SELECT id FROM habits_{user}")
    habit_ids = [row[0] for row in cur.fetchall()]

    # Generate logs for the past 5 days
    today = datetime.today()
    for i in range(5):
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for habit_id in habit_ids:
            cur.execute(f"""
                INSERT OR IGNORE INTO habit_logs_{user}
                (habit_id, date, quantity, is_completed)
                VALUES (?, ?, ?, ?)
            """, (habit_id, date_str, 1.0, 1))

    conn.commit()
    conn.close()

# -----------main-----------
if __name__ == "__main__":
    create_db('')
    create_new_day('')
    print_habits_everuthing('')
    print_logs('')


# BUG doesnt seem to delete the logs check that next time pal xoxo
