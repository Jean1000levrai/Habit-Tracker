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
    return [hab.name,
            hab.colour,
            hab.question,
            hab.reminder,
            hab.description,
            hab.frequency]

def show_habit_for_gui(stuff):

    conn = connect_to_db()
    cur = conn.cursor()
    if stuff == "*":
        cur.execute("""SELECT * FROM habits""")
    else:
        cur.execute("""SELECT * FROM habits
                    WHERE name = ?""", (stuff,))
    
    list_habits = cur.fetchall()

    conn.commit()
    conn.close()

    return list_habits

def get_info_hab(hab, thing):
    return hab.thing

if __name__ == "__main__":
    hab = hmgr.HabitYesNo()
    # delete_habit()
    print_table()
    # print(get_info_hab())