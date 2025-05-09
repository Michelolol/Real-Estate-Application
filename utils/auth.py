import psycopg2
from config import DB_URL

def login(email, password):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT userid,
               CASE 
                 WHEN userid IN (SELECT userid FROM Agent) THEN 'agent'
                 WHEN userid IN (SELECT userid FROM Client) THEN 'client'
                 ELSE 'admin'
               END AS role
        FROM User_Data
        WHERE emailAddress = %s AND password = %s
    """, (email, password))
    
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return {'userid': row[0], 'role': row[1]}
    return None