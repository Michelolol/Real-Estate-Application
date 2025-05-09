import psycopg2
from config import DB_URL

def menu(userid):
    while True:
        print("\n=== Agent Menu ===")
        print("1. View My Properties")
        print("2. Add New Property")
        print("3. Remove a Property")
        print("4. View Reviews on My Properties")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_my_properties(userid)
        elif choice == "2":
            add_property(userid)
        elif choice == "3":
            remove_property(userid)
        elif choice == "4":
            view_property_reviews(userid)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

# --- View ---
def view_my_properties(userid):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT propertyid, description, price, city, state
        FROM Properties
        WHERE listedBy = %s
    """, (userid,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\n--- My Listed Properties ---")
    if not rows:
        print("You have no properties listed.")
    else:
        for row in rows:
            print(f"""
Property ID:   {row[0]}
Description:   {row[1]}
Price:         ${row[2]}
Location:      {row[3]}, {row[4]}
""")

# --- Insert ---
def add_property(userid):
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
                propertyid, sqFeet, roomCt, availability, description, price,
                city, state, street, zipCode, neighborhoodid, listedBy
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (pid, sqft, rooms, avail, desc, price, city, state, street, zipc, nid, userid))
        conn.commit()
        cur.close()
        conn.close()
        print("Property added.")
    except Exception as e:
        print("Failed to add property:", e)

# --- Remove ---
def remove_property(userid):
    try:
        pid = int(input("Enter Property ID to remove: "))
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Properties
            WHERE propertyid = %s AND listedBy = %s
        """, (pid, userid))
        conn.commit()
        cur.close()
        conn.close()
        print("Property removed.")
    except Exception as e:
        print("Failed to remove property:", e)


# --- View property reviews ---
def view_property_reviews(agent_id):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT R.propertyid, P.description, R.review,
               U.firstName, U.lastName, U.emailAddress
        FROM Reviews R
        JOIN Properties P ON R.propertyid = P.propertyid
        JOIN User_Data U ON R.userid = U.userid
        WHERE P.listedBy = %s
    """, (agent_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\n--- Reviews on Your Properties ---")
    if not rows:
        print("No reviews yet.")
    else:
        for row in rows:
            print(f"""
Property ID:   {row[0]}
Description:   {row[1]}
Review:        {row[2]}
By:            {row[3]} {row[4]} ({row[5]})
""")
