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


def add_habits(hab):
    """add a habit into the database"""
    info = hab_info(hab)
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"""
        INSERT INTO habits 
        VALUES ({info[0]}, {info[1]}, {info[2]}, {info[3]}, {info[4]}, {info[5]})
""")
    conn.commit()
    conn.close()

def delete_habits():
    """delete a habit from the database"""
    pass

def load_habits():
    pass

def save_habits():
    pass

def hab_info(hab = hmgr.HabitYesNo()):
    return [hab.name,
            hab.colour,
            hab.question,
            hab.reminder,
            hab.description,
            hab.frequency]

if __name__ == "__main__":
    hab = hmgr.HabitYesNo()
    add_habits(hab)
    print_table()