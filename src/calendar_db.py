import sqlite3 as sql
import habit_mgr as hmgr
from functions import *



def connect_to_db():
    return sql.connect(resource_path2("data/db_habit.db"))

def create_table(user = ''):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(f"""CREATE TABLE IF NOT EXISTS calendar_{user}
                    (id INTEGER PRIMARY KEY,
                    time TEXT,
                    date TEXT,
                    is_done BOOLEAN DEFAULT 0,
                    measure INTEGER
                    FOREIGN KEY (id) REFERENCES habit_days_{user}(habit_id) ON DELETE CASCADE)""")

    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_table()