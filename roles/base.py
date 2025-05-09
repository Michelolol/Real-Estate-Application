# roles/base.py
import psycopg2
from config import DB_URL
from roles import admin, agent, client

def base_menu(user):
    while True:
        print(f"\n=== Welcome {user['role'].capitalize()} (User ID: {user['userid']}) ===")
        print("1. View My Profile")
        print("2. Login")
        print("0. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            view_profile(user['userid'])
        elif choice == "2":
            launch_role_menu(user)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def view_profile(userid):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT userid, emailAddress, firstName, middleName, lastName
        FROM User_Data WHERE userid = %s
    """, (userid,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    print("\n--- Profile Info ---")
    print(f"User ID: {user[0]}")
    print(f"Email: {user[1]}")
    print(f"Name: {user[2]} {user[3] or ''} {user[4]}")

def launch_role_menu(user):
    role = user['role']
    uid = user['userid']
    if role == 'admin':
        admin.menu(uid)
    elif role == 'agent':
        agent.menu(uid)
    elif role == 'client':
        client.menu(uid)
