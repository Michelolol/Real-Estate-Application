import psycopg2
from config import DB_URL

def menu(userid):
    while True:
        print("\n=== Client Menu ===")
        print("1. View Available Properties")
        print("2. Book a Property")
        print("3. Manage Reviews")
        print("4. View My Contracts")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_available_properties()
        elif choice == "2":
            book_property(userid)
        elif choice == "3":
            manage_reviews(userid)
        elif choice == "4":
            view_contracts(userid)
        elif choice == "0":
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
