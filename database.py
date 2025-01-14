import mysql.connector
import re

def insert_to_sql(data):
    # Establish a connection to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',       # Replace with your MySQL host (e.g., 'localhost')
        user='root',       # Replace with your MySQL user
        password='password',  # Replace with your MySQL password
        database='wow_econ'   # Replace with your MySQL database name
    )
    cursor = conn.cursor()

    try:
        # Step 1: Clean up the data
        data = data.replace("return {", "")  # Remove 'return {' 
        data = data.replace("\\", "")  # Remove backslashes
        data = data.replace("nil", "false")  # Convert 'nil' to 'false'
        data = re.sub(r",\s*([}])", r"\1", data)  # Remove trailing commas before closing braces
        if data.endswith(','):
            data = data[:-1]  # Remove trailing comma
        data = data.rstrip('},')  # Remove the final closing brace

        # Step 2: Split the cleaned data into lines
        lines = data.split("},")  # Split data into individual items

        # Prepare the list of tuples for bulk insertion
        data_to_insert = []

        # Step 3: Process each line and extract relevant data
        for line in lines:
            values = [value.strip() for value in line.split(',')]  # Split by commas and strip extra spaces

            # Extract item_id, item_name, quantity, price, seller, and time
            item_id = values[22]  # Assuming index 22 is item_id
            item_name = values[8].replace("\"", "")  # Remove quotes from item_name
            quantity = values[10]  # Assuming index 10 is quantity
            price = values[16]  # Assuming index 16 is price
            seller = values[19].replace("\"", "")  # Remove quotes from seller
            time = values[7]  # Assuming index 7 is time

            # Add the tuple to the list for later insertion
            data_to_insert.append((item_id, item_name, quantity, price, seller, time))

        # Step 4: Insert all the rows in a single query
        query = """
        INSERT INTO items (item_id, item_name, quantity, price, seller, time)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.executemany(query, data_to_insert)

        # Commit the transaction to save the changes
        conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback in case of error

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

def create_database():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',       # Replace with your MySQL host (e.g., 'localhost')
        user='root',       # Replace with your MySQL user
        password='password',  # Replace with your MySQL password
        database='wow_econ'   # Replace with your MySQL database name
    )
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_id INT,
        item_name VARCHAR(255),
        quantity INT,
        price DECIMAL(10, 2),
        seller VARCHAR(255),
        time INT
    );
    """)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print("Table created successfully!")
