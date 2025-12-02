import sqlite3
conn = sqlite3.connect('database1.db')
cur = conn.cursor()

cur.execute("SELECT * FROM users")
rows = cur.fetchall()
print(rows)
print("query executed successfully!, number of rows: ", len(rows))