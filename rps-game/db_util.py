import sqlite3

# Initialize SQLite database
conn = sqlite3.connect('student_database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students
             (student_id text, code text, score integer)''')
