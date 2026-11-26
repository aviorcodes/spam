import sqlite3
from contextlib import contextmanager

DB_NAME = "students.db"
SUBJECTS = ("Math", "Science", "English", "Computer", "Social")


class Database:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._init()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init(self):
        with self._conn() as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_no  TEXT UNIQUE NOT NULL,
                    name     TEXT NOT NULL,
                    klass    TEXT NOT NULL,
                    gender   TEXT,
                    math     REAL DEFAULT 0,
                    science  REAL DEFAULT 0,
                    english  REAL DEFAULT 0,
                    computer REAL DEFAULT 0,
                    social   REAL DEFAULT 0,
                    created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    # ---- CRUD ----
    def add(self, d: dict):
        with self._conn() as c:
            c.execute("""
                INSERT INTO students
                (roll_no,name,klass,gender,math,science,english,computer,social)
                VALUES (:roll_no,:name,:klass,:gender,
                        :math,:science,:english,:computer,:social)
            """, d)

    def update(self, sid: int, d: dict):
        d = {**d, "id": sid}
        with self._conn() as c:
            c.execute("""
                UPDATE students SET
                  roll_no=:roll_no, name=:name, klass=:klass, gender=:gender,
                  math=:math, science=:science, english=:english,
                  computer=:computer, social=:social
                WHERE id=:id
            """, d)

    def delete(self, sid: int):
        with self._conn() as c:
            c.execute("DELETE FROM students WHERE id=?", (sid,))

    def all(self):
        with self._conn() as c:
            rows = c.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
            return [dict(r) for r in rows]

    def search(self, kw: str):
        with self._conn() as c:
            like = f"%{kw}%"
            rows = c.execute("""
                SELECT * FROM students
                WHERE name LIKE ? OR roll_no LIKE ? OR klass LIKE ?
                ORDER BY id DESC
            """, (like, like, like)).fetchall()
            return [dict(r) for r in rows]

    def get(self, sid: int):
        with self._conn() as c:
            r = c.execute("SELECT * FROM students WHERE id=?", (sid,)).fetchone()
            return dict(r) if r else None

    def count(self):
        with self._conn() as c:
            return c.execute("SELECT COUNT(*) FROM students").fetchone()[0]