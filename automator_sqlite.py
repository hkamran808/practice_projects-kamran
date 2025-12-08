import sqlite3
from tabulate import tabulate
from datetime import datetime

def log(message):
    with open("automator-log.txt", "a") as log_file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] {message}")

conn = sqlite3.connect("database1.db")
cur = conn.cursor()
print("Database connected: ")

# Interactive mode with UI below:
def menu():
    print("--- My SQLite Automator! ---")
    print("1. Show all users")
    print("2. Add a new user")
    print("3. Update user age")
    print("4. Delete user")
    print("5. Search user by name")
    print("0. Quit")

def show_users():
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    if len(rows) == 0:
        print("no data found!")
    if len(rows) > 0:
        print("users => ")
        print(tabulate(rows, headers=columns, tablefmt="fancy_grid"))
        print(f"{len(rows)} rows x {len(columns)} columns")

def add_user():
    name = input("Enter name of user: ")
    age = input("Enter age of user: ")

    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    print("user added succesfully!")

def update_user():
    id = int(input("Enter ID of user: "))
    new_age = input("Enter updated age of user: ")
    cur.execute("UPDATE users SET age=? WHERE id=? VALUES()", (new_age, id))
    conn.commit()
    print("user's age updated succesfully!")

def delete_user():
    user_id = int(input("Enter ID of user: "))
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    print("user deleted succesfully!")

def search_user_byName():
    searched_name = input("Enter name to search: ")
    cur.execute("SELECT * FROM users WHERE name LIKE ?", ('%'+searched_name+'%',))
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No user found!")
        return
    
    columns = [desc[0] for desc in cur.description]
    print(tabulate(rows, headers=columns, tablefmt="fancy_grid"))
    print(f"({len(rows)} rows) x {len(columns)} columns")

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
        case "0" | "quit" | "exit" | "leave":
            print("Quitting...")
            break
        
    """
    try:
        cur.execute(command)
    except Exception as e:
        print("SQL error", e)
        log(f"ERROR: {command} | reason: {e}")
        continue
    """
    
conn.close()
print("connection is closed!")