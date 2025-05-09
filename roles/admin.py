import psycopg2
from config import DB_URL

def menu(userid):
    while True:
        print("\n=== Admin Panel ===")
        print("1. INSERT Menu")
        print("2. VIEW Menu")
        print("3. REMOVE Menu")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            insert_menu()
        elif choice == "2":
            view_menu()
        elif choice == "3":
            remove_menu()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

# INSERT submenu
def insert_menu():
    while True:
        print("\n-- INSERT Menu --")
        print("1. Insert New User")
        print("2. Insert New Agent")
        print("3. Insert New Client")
        print("4. Insert New Property")
        print("0. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            insert_user()
        elif choice == "2":
            insert_agent()
        elif choice == "3":
            insert_client()
        elif choice == "4":
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
        print("0. Back")

        choice = input("Choose an option: ")

        if choice == "1":
            view_users()
        elif choice == "2":
            view_properties()
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
            remove_user()
        elif choice == "2":
            remove_property()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

# ===== INSERT FUNCTIONS =====

def insert_user():
    try:
        uid = int(input("User ID: "))
        email = input("Email: ")
        fname = input("First name: ")
        mname = input("Middle name (optional): ")
        lname = input("Last name: ")
        pw = input("Password: ")

        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO User_Data (userid, emailAddress, firstName, middleName, lastName, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (uid, email, fname, mname or None, lname, pw))
        conn.commit()
        cur.close()
        conn.close()
        print("User inserted.")
    except Exception as e:
        print("Error:", e)

def insert_agent():
    try:
        uid = int(input("User ID (must exist in User_Data): "))
        contact = input("Contact info: ")
        job = input("Job title: ")
        agency = input("Agency: ")

        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Agent (userid, contactInfo, jobTitle, agency)
            VALUES (%s, %s, %s, %s)
        """, (uid, contact, job, agency))
        conn.commit()
        cur.close()
        conn.close()
        print("Agent inserted.")
    except Exception as e:
        print("Error:", e)

def insert_client():
    try:
        uid = int(input("User ID (must exist in User_Data): "))
        budget = float(input("Budget: "))
        date = input("Desired Move Date (YYYY-MM-DD): ")

        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Client (userid, budget, desiredMoveDate)
            VALUES (%s, %s, %s)
        """, (uid, budget, date))
        conn.commit()
        cur.close()
        conn.close()
        print("Client inserted.")
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