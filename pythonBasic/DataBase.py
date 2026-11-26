'''import sqlite3
conn = sqlite3.connect("college.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT)
    """)
conn.commit()
print("Table created successfully!")
conn.close()
'''
#insert command
'''import sqlite3
conn = sqlite3.connect("college.db")
cursor = conn.cursor()
students = [
    (101,'Rajdev',23,'MCA'),
    (102,'Rajde',21,'MCA'),
    (103,'Rajd',22,'MCA'),
    (104,'Raj',20,'MCA'),
    (105,'Ra',22,'MCA')

]
cursor.executemany("""
    INSERT INTO students(id,name,age,course) values (?,?,?,?)

    """,students)
conn.commit()
print("Values inserted successfully!")
conn.close()'''
#display all records
import sqlite3
conn = sqlite3.connect("college.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM students")
records = cursor.fetchall()
for row in records:
    print(row)
conn.close()