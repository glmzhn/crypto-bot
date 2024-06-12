import sqlite3

conn = sqlite3.connect('accounts.db')

cur = conn.cursor()

cur.execute("""
    CREATE TABLE user_account (
        user_id INT,
        account VARCHAR(255),
        currency VARCHAR(255)
    )
""")

print("Table is Ready")

conn.commit()

conn.close()
