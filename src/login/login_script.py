import sqlite3 as sql
import hashlib as hash


def connect_to_db():
    return sql.connect("data/db_userinfo.db")

def create_db():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS userinfo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                userinfo_id INTEGER,
                FOREIGN KEY(userinfo_id) REFERENCES habits(id))""")
    conn.commit()
    conn.close()

def join_info(username, usr_id):
    conn = connect_to_db()
    cur = conn.cursor()
    
    cur.execute("")

    conn.commit()
    conn.close()

def set_info(username, email, pwd):
    conn = connect_to_db()
    cur = conn.cursor()

    username = username.strip()
    email = email.strip()
    pwd = pwd.strip()
    
    pwd2 = hash.sha256(pwd.encode('UTF-8')).hexdigest()

    cur.execute("INSERT INTO userinfo "\
                "(username, email, password) "\
                "VALUES (?, ?, ?)", (username, email, pwd2))

    conn.commit()
    conn.close()

def print_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM userinfo")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_user(name = '*'):
    conn = connect_to_db()
    cur = conn.cursor()
    if name == '*':
        cur.execute("""DELETE FROM userinfo
                WHERE id < 999999999999999""")
    else:
        cur.execute("""DELETE FROM userinfo
                WHERE name = ?""", (name,))
    
    conn.commit()
    conn.close()

def get_from_username(username):
    conn = connect_to_db()
    cur = conn.cursor()

    username = username.strip()

    cur.execute("""SELECT password FROM userinfo
                WHERE username = ?""", (username,))
    
    pwd = cur.fetchone()
    
    conn.close()

    return pwd[0] if pwd else None

def test_log(username, pwd):

    username = username.strip()
    pwd = pwd.strip()
    hashed_pwd = get_from_username(username)
    if get_from_username(username) is None:
        # raise ValueError("username not registered")
        pass
    if hashed_pwd == hash.sha256(pwd.encode('UTF-8')).hexdigest():
        print("logged in!")
        return True
    else:
        print("invalid username or password!")
        return False


if __name__ == "__main__":
    create_db()
    # delete_user()
    set_info("easydoor", "easy@gmia.com", "1234")
    print_table()
    # test_log("jen", "1234")
