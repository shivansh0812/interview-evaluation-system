import sqlite3


def connect_db():
    return sqlite3.connect("database.db")


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            question TEXT,
            answer TEXT,
            score REAL,
            feedback TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_record(role, question, answer, score, feedback):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interviews (role, question, answer, score, feedback)
        VALUES (?, ?, ?, ?, ?)
    """, (role, question, answer, score, feedback))

    conn.commit()
    conn.close()


def get_all_records():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, question, answer, score, feedback 
        FROM interviews
    """)

    rows = cursor.fetchall()

    conn.close()
    return rows