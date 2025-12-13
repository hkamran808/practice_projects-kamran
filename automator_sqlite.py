import sqlite3
from tabulate import tabulate
from datetime import datetime

conn = sqlite3.connect("database1.db")
cur = conn.cursor()
print("Database connected: ")

# query log for storing all commands executed (+avoid errors with drop if exists)
def setup_query_log():
    cur.execute("DROP TABLE IF EXISTS query_logs")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS query_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        query TEXT,
        executed_at TEXT,
        success INTEGER,
        error_message TEXT
    )
    """)
    conn.commit()

setup_query_log()

def log_query(action, query, success, error_message=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute("INSERT INTO query_logs (action, query, executed_at, success, error_message) VALUES(?,?,?,?,?)", 
                    (action, query, timestamp, int(success), error_message))
        conn.commit()
    except Exception as e:
        print("Failed to write to query_logs table: ", e)
        #print("Original log: ", action, query, int(success), error_message)

# Interactive mode with UI below:
# menu modified with "show query history" option
def menu():
    print("--- My SQLite Automator! ---")
    print("1. Show all users")
    print("2. Add a new user")
    print("3. Update user age")
    print("4. Delete user")
    print("5. Search user by name")
    print("6. Show query history")
    print("7. Export logs to CSV")
    print("8. Export logs to JSON")
    print("0. Quit")

#each menu function modified so it logs the action, +try/except
def show_users():
    query = "SELECT * FROM users"

    try:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        if len(rows) == 0:
            print("no data found!")
        if len(rows) > 0:
            print("users => ")
            print(tabulate(rows, headers=columns, tablefmt="fancy_grid"))
            print(f"{len(rows)} rows x {len(columns)} columns")

        log_query("SELECT", query, success=1)

    except Exception as e:
        print("SQL error", e)
        log_query("SELECT", query, success=0, error_message=str(e))

def add_user():
    name = input("Enter name of user: ")
    age = input("Enter age of user: ")
    query = "INSERT INTO users (name, age) VALUES (?, ?)"

    try:
        cur.execute(query, (name, age))
        conn.commit()
        print("user added succesfully!")
        log_query("INSERT", query, success=1)
    except Exception as e:
        print("SQL error", e)
        log_query("INSERT", query, success=0, error_message=str(e))

def update_user():
    query = "UPDATE users SET age=? WHERE id=?"
    id = int(input("Enter ID of user: "))
    new_age = input("Enter updated age of user: ")

    try:
        cur.execute(query, (new_age, id))
        conn.commit()
        print("user's age updated succesfully!")
        log_query("UPDATE", query, success=1)
    except Exception as e:
        print("SQL error", e)
        log_query("UPDATE", query, success=0, error_message=str(e))

def delete_user():
    user_id = int(input("Enter ID of user: "))
    query = "DELETE FROM users WHERE id=?"
    
    try:
        cur.execute(query, (user_id,))
        conn.commit()
        print("user deleted succesfully!")
        log_query("DELETE", query, success=1)
    except Exception as e:
        print("SQL error", e)
        log_query("DELETE", query, success=0, error_message=str(e))

def search_user_byName():
    query = "SELECT * FROM users WHERE name LIKE ?"
    searched_name = input("Enter name to search: ")

    try:
        cur.execute(query, ('%'+searched_name+'%',))
        rows = cur.fetchall()

        if len(rows) == 0:
            print("No user found!")
            return
        
        columns = [desc[0] for desc in cur.description]
        print(tabulate(rows, headers=columns, tablefmt="fancy_grid"))
        print(f"{len(rows)} rows x {len(columns)} columns")
        log_query("SELECT", query, success=1)
    except Exception as e:
        print("SQL error: ", e)
        log_query("SEARCH", query, success=0, error_message=str(e))

def query_history():
    cur.execute("SELECT id, action, executed_at, success FROM query_logs ORDER BY id DESC")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No history yet.")
        return

    print(tabulate(rows, headers=["ID","Action","Time","Success"], tablefmt="fancy_grid"))
    print(f"{len(rows)} rows x 4 columns")

#helper function for exp./imp.:
def get_all_logs():
    cur.execute("SELECT * FROM query_logs ORDER BY id ASC")
    logs = cur.fetchall()
    return logs

import csv
def export_logs_to_csv(filename):
    logs = get_all_logs()
    if not logs:
        print("No logs to export")
        return
    
    columns = ["id", "action", "query", "executed_at", "success", "error_message"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(logs)
    print(f"Exported {len(logs)} log entries to {filename}")

import json
def export_logs_to_json(filename):
    logs = get_all_logs()
    if not logs:
        print("No logs to export")
        return
    
    columns = ["id", "action", "query", "executed_at", "success", "error_message"]
    with open(filename, mode='w', encoding='utf-8') as file:
        data = [dict(zip(columns, row)) for row in logs]
        json.dunmp(data, file, indent=4)
    print(f"Exported {len(logs)} log entries to {filename}")


while True:
    menu()
    choice = input("OPTION>> ").strip()
    match choice:
        case "1":
            show_users() 
        case "2":
            add_user()
        case "3":
            update_user()
        case "4":
            delete_user()
        case "5":
            search_user_byName()
        case "6":
            query_history()
        case "7":
            export_logs_to_csv("query_logs_exported.csv")
        case "8":
            export_logs_to_json("query_logs_exported.json")
        case "0" | "quit" | "exit" | "leave":
            print("Quitting...")
            break
        
    
conn.close()
print("connection is closed!")