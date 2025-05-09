# roles/base.py
import psycopg2
from config import DB_URL
from roles import admin, agent, client

def base_menu(user):
    while True:
        print(f"\n=== Welcome {user['role'].capitalize()} (User ID: {user['userid']}) ===")
        print("1. View My Profile")
        print("2. Login")
        print("3. Update My Profile")
        print("0. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            view_profile(user['userid'])
        elif choice == "2":
            launch_role_menu(user)
        elif choice == "3":
            update_profile(user['userid'])
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

def update_profile(userid):
    while True:
        print("\n--- Update My Profile ---")
        print("1. Change Name")
        print("2. Change Password")
        print("0. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            update_name(userid)
        elif choice == "2":
            update_password(userid)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

# -- Helper Functions for update --
def update_name(userid):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    first = input("New First Name: ")
    middle = input("New Middle Name (optional): ")
    last = input("New Last Name: ")

    try:
        cur.execute("""
            UPDATE User_Data
            SET firstName = %s,
                middleName = %s,
                lastName = %s
            WHERE userid = %s
        """, (first, middle or None, last, userid))
        conn.commit()
        print("Name updated successfully.")
    except Exception as e:
        print("Error updating name:", e)

    cur.close()
    conn.close()


def update_password(userid):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    new_password = input("New Password: ")
    confirm_password = input("Confirm New Password: ")

    if new_password != confirm_password:
        print("Passwords do not match. Password not updated.")
        cur.close()
        conn.close()
        return

    try:
        cur.execute("""
            UPDATE User_Data
            SET password = %s
            WHERE userid = %s
        """, (new_password, userid))
        conn.commit()
        print("Password updated successfully.")
    except Exception as e:
        print("Error updating password:", e)

    cur.close()
    conn.close()

