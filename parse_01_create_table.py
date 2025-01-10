import sqlite3

# Connect to the SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect('items.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    item_name TEXT,
    quantity INTEGER,
    price REAL,
    seller TEXT,
    time INTEGER
);
""")

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Table created successfully!")
