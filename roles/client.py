import psycopg2
from config import DB_URL
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(userid):
    while True:
        print("\n=== Client Menu ===")
        print("1. View Available Properties")
        print("2. Book a Property")
        print("3. Manage Reviews")
        print("4. View My Contracts")
        print("5. View Rewards")
        print("6. View Neighborhoods")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            clear()
            view_available_properties()
        elif choice == "2":
            clear()
            view_available_properties()
            book_property(userid)
        elif choice == "3":
            clear()
            manage_reviews(userid)
        elif choice == "4":
            clear()
            view_contracts(userid)
        elif choice == "5":
            clear()
            view_rewards(userid)
        elif choice == "6":
            clear()
            view_neighborhoods()
        elif choice == "0":
            clear()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

# --- View Properties ---
def view_available_properties():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM ClientAvailableProperties")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\n--- Available Properties ---")
    for row in rows:
        print(f"""
Property ID:     {row[0]}
Description:     {row[1]}
Price:           ${row[2]}
Location:        {row[3]}, {row[4]}
Agent ID:        {row[5]}
Agent Name:      {row[6]} {row[7]}
Contact Info:    {row[8]}
""")

# --- Book a Property ---
def book_property(userid):
    try:
        property_id = int(input("Enter Property ID to book: "))
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")

        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Contract (userid, propertyid, startDate, endDate)
            VALUES (%s, %s, %s, %s)
        """, (userid, property_id, start_date, end_date))
        conn.commit()
        cur.close()
        conn.close()
        print("Property booked successfully.")
    except Exception as e:
        print("Booking failed:", e)

# --- Manage a Review/ Write ---
def manage_reviews(userid):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # View existing reviews
    cur.execute("""
        SELECT R.propertyid, P.description, R.review
        FROM Reviews R
        JOIN Properties P ON R.propertyid = P.propertyid
        WHERE R.userid = %s
    """, (userid,))
    rows = cur.fetchall()

    print("\n--- My Reviews ---")
    if not rows:
        print("You have not written any reviews.")
    else:
        for row in rows:
            print(f"""
Property ID:   {row[0]}
Description:   {row[1]}
Review:        {row[2]}
""")

    # Ask if they want to add one
    choice = input("Would you like to add a new review? (y/n): ").lower()
    if choice == 'y':
        try:
            property_id = int(input("Enter Property ID to review: "))
            review_text = input("Enter your review: ")

            cur.execute("""
                INSERT INTO Reviews (userid, propertyid, review)
                VALUES (%s, %s, %s)
            """, (userid, property_id, review_text))
            conn.commit()
            print("Review submitted.")
        except Exception as e:
            print("Failed to submit review:", e)

    cur.close()
    conn.close()

        # --- View Contracts ---
def view_contracts(userid):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT C.propertyid, P.description, P.city, P.state, C.startDate, C.endDate
        FROM Contract C
        JOIN Properties P ON C.propertyid = P.propertyid
        WHERE C.userid = %s
    """, (userid,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\n--- My Contracts ---")
    if not rows:
        print("You have no active bookings.")
        return

    for row in rows:
        print(f"""
Property ID:   {row[0]}
Description:   {row[1]}
Location:      {row[2]}, {row[3]}
Start Date:    {row[4]}
End Date:      {row[5]}
""")
        
def view_neighborhoods():
    import psycopg2
    from config import DB_URL

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Neighborhood")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\nNeighborhoods:")
    for row in rows:
        print(f"ID: {row[0]}, Avg Price: ${row[1]:,.2f}, Crime Rate: {row[2]}")
    input("\nPress Enter to return...")

def view_rewards(userid):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        cur.execute("""
            SELECT totalPoints, activated
            FROM ClientRewards
            WHERE userid = %s
        """, (userid,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            print("\n--- Rewards Summary ---")
            print(f"Total Points: {row[0]}")
            print(f"Activated: {'Yes' if row[1] else 'No'}")
        else:
            print("No rewards found.")

    except Exception as e:
        print("Error fetching rewards:", e)

    input("\nPress Enter to return...")
