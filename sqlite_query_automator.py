import sqlite3
conn = sqlite3.connect('database1.db')
cur = conn.cursor()

cur.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        );
""")

starter_users = [
    ("Ronaldo", 39),
    ("Messi", 36),
    ("Modric", 38),
    ("Haaland", 24),
    ("Mbappe", 25),
    ("Lewandowski", 35),
    ("Pedri", 21),
    ("Gavi", 20),
    ("De Bruyne", 33),
    ("Bellingham", 21),
    ("Vinicius", 23),
    ("Musiala", 21),
    ("Kane", 31),
    ("Saka", 23),
    ("Odegaard", 25),
    ("Salah", 32),
    ("Alvarez", 24),
    ("Foden", 24),
    ("Rashford", 26),
    ("Bruno", 29),
    ("Martinez", 26),
    ("Sterling", 30),
    ("Neymar", 32),
    ("Sancho", 24),
    ("Gundogan", 33),
    ("Griezmann", 33),
    ("Suarez", 37)
]

cur.executemany("INSERT INTO users (name, age) VALUES (?,?)", starter_users)
print("Inserted users:", cur.rowcount)

conn.commit()
conn.close()

print("database is ready!")