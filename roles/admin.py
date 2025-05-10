import psycopg2
from config import DB_URL
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(userid):
    while True:
        print("\n=== Admin Panel ===")
        print("1. INSERT Menu")
        print("2. VIEW Menu")
        print("3. REMOVE Menu")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            clear()
            insert_menu()
        elif choice == "2":
            clear()
            view_menu()
        elif choice == "3":
            clear()
            remove_menu()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

# INSERT submenu
def insert_menu():
    while True:
        print("\n-- INSERT Menu --")
        print("1. Insert New User with Role")
        print("2. Insert New Property")
        print("0. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            clear()
            insert_user_with_role()
        elif choice == "2":
            clear()
            insert_property()
        elif choice == "0":
            break
        else:
            print("Invalid option.")


# VIEW submenu
def view_menu():
    while True:
        print("\n-- VIEW Menu --")
        print("1. View All Users")
        print("2. View All Properties")
        print("3. View Users by Role")
        print("0. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            clear()
            view_users()
        elif choice == "2":
            clear()
            view_properties()
        elif choice == "3":
            clear()
            view_users_by_role()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

# REMOVE submenu
def remove_menu():
    while True:
        print("\n-- REMOVE Menu --")
        print("1. Remove User (and their Agent/Client role if exists)")
        print("2. Remove Property by ID")
        print("0. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            clear()
            view_users()
            remove_user()
        elif choice == "2":
            clear()
            view_properties()
            remove_property()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

# ===== INSERT FUNCTIONS =====

def insert_user_with_role():
    try:
        uid = int(input("New User ID: "))
        email = input("Email: ")
        fname = input("First name: ")
        mname = input("Middle name (optional): ")
        lname = input("Last name: ")
        pw = input("Password: ")
        role = input("Assign Role (admin / agent / client): ").lower()

        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Insert into User_Data
        cur.execute("""
            INSERT INTO User_Data (userid, emailAddress, firstName, middleName, lastName, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (uid, email, fname, mname or None, lname, pw))

        # Insert into Agent or Client if applicable
        if role == 'agent':
            contact = input("Contact info: ")
            job = input("Job title: ")
            agency = input("Agency: ")
            cur.execute("""
                INSERT INTO Agent (userid, contactInfo, jobTitle, agency)
                VALUES (%s, %s, %s, %s)
            """, (uid, contact, job, agency))

        elif role == 'client':
            budget = float(input("Budget: "))
            date = input("Desired Move Date (YYYY-MM-DD): ")
            cur.execute("""
                INSERT INTO Client (userid, budget, desiredMoveDate)
                VALUES (%s, %s, %s)
            """, (uid, budget, date))

        elif role == 'admin':
            print("Admin role will be recognized automatically (no extra table).")

        else:
            print("Invalid role. Only admin, agent, client allowed.")
            conn.rollback()
            cur.close()
            conn.close()
            return

        conn.commit()
        cur.close()
        conn.close()
        print("User with role inserted successfully.")
    except Exception as e:
        print("Error:", e)

def insert_property():
    try:
        pid = int(input("Property ID: "))
        sqft = int(input("Square feet: "))
        rooms = int(input("Room count: "))
        avail = input("Available (true/false): ").lower() == 'true'
        desc = input("Description: ")
        price = float(input("Price: "))
        city = input("City: ")
        state = input("State: ")
        street = input("Street: ")
        zipc = input("Zip code: ")
        nid = int(input("Neighborhood ID: "))

        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Properties (
                propertyid, sqFeet, roomCt, availability, description,
                price, city, state, street, zipCode, neighborhoodid
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (pid, sqft, rooms, avail, desc, price, city, state, street, zipc, nid))
        conn.commit()
        cur.close()
        conn.close()
        print("Property inserted.")
    except Exception as e:
        print("Error:", e)

# ===== VIEW FUNCTIONS =====

def view_users():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT userid, emailAddress, firstName, lastName FROM User_Data")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    print("\nUsers:")
    for row in rows:
        print(f"ID: {row[0]}, Email: {row[1]}, Name: {row[2]} {row[3]}")

def view_properties():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT propertyid, price, city, state FROM Properties")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\nProperties:")
    for row in rows:
        print(f"ID: {row[0]}, ${row[1]}, Location: {row[2]}, {row[3]}")

def view_users_by_role():
    role = input("Enter role to filter (agent/client): ").lower()
    if role not in ("agent", "client"):
        print("Invalid role.")
        return

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    if role == "agent":
        cur.execute("""
            SELECT U.userid, U.emailAddress, U.firstName, U.lastName
            FROM User_Data U
            JOIN Agent A ON U.userid = A.userid
        """)
    else:
        cur.execute("""
            SELECT U.userid, U.emailAddress, U.firstName, U.lastName
            FROM User_Data U
            JOIN Client C ON U.userid = C.userid
        """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"\nUsers with role '{role}':")
    for row in rows:
        print(f"ID: {row[0]}, Email: {row[1]}, Name: {row[2]} {row[3]}")

# ===== REMOVE FUNCTIONS =====

def remove_user():
    try:
        uid = int(input("Enter User ID to fully remove: "))
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        # Remove from role tables if they exist
        cur.execute("DELETE FROM Agent WHERE userid = %s", (uid,))
        cur.execute("DELETE FROM Client WHERE userid = %s", (uid,))

        # Remove from base user table (cascade removes related foreign keys)
        cur.execute("DELETE FROM User_Data WHERE userid = %s", (uid,))
        conn.commit()
        cur.close()
        conn.close()
        print("User and related roles removed.")
    except Exception as e:
        print("Error:", e)

def remove_property():
    pid = int(input("Property ID to remove: "))
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM Properties WHERE propertyid = %s", (pid,))
    conn.commit()
    cur.close()
    conn.close()
    print("Property removed.")