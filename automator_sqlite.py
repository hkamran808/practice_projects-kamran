import sqlite3
from tabulate import tabulate
from datetime import datetime

conn = sqlite3.connect("database1.db")
cur = conn.cursor()

"""
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
"""

# Interactive mode below:
print("Database connected. Enter your SQL commands! or quit!")

while True:
    command = input("SQL>>").strip()
    if command.lower() in ("exit", "quit", "leave"):
        print("You quitted, goodbye!")
        break
    if command == "" or command.startswith("--"):
        continue

    try:
        cur.execute(command)
    except Exception as e:
        print("SQL error", e)

    first_cmd = command.split()[0].lower()
    if first_cmd == "select":
        rows = cur.fetchall()
        print("number of rows fetched:", len(rows))
        if len(rows) > 0:
            print("here they are: ")
        for row in rows:
            print(row)
    else:
        conn.commit()
        print("Executed! Rows that are affected: ", cur.rowcount)

conn.close()
print("all commands executed, connection is closed!")