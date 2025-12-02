import sqlite3

conn = sqlite3.connect("database1.db")
cur = conn.cursor()

with open("queries.sql", "r") as file:
    sql_commands = file.read().split(";")

for command in sql_commands:
    command = command.strip()
    if command == "":
        continue
    print(f"current command: {command}")

    try:
        cur.execute(command)
        if command.lower().startswith("select"):
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print(row)
            print(f"number of rows: {len(rows)}")

        else:
            conn.commit()
            print("command executed successfully!")
    except Exception as e:
        print(f"exception (error) occurred: {e}")

conn.close()
print("all commands executed, connection is closed!")