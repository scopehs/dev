import re
import sqlite3

# Establish a connection to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('items.db')  # This will create 'items.db' in the current directory
cursor = conn.cursor()

# Step 1: Read the data from the file with the correct encoding
encodings_to_try = ["utf-8", "utf-16", "ISO-8859-1", "latin1"]  # Added 'latin1' as an additional fallback encoding

data = ""
for encoding in encodings_to_try:
    try:
        with open("data.txt", "r", encoding=encoding, errors="ignore") as file:  # Try different encodings
            data = file.read()
        print(f"File successfully read using {encoding} encoding.")
        break  # Exit the loop if reading is successful
    except UnicodeDecodeError:
        print(f"Error reading the file with {encoding} encoding. Trying next encoding...")

if not data:
    print("Failed to read the file with any of the attempted encodings.")
    exit()

# Step 2: Clean up the data
data = data.replace("return {", "")  # Remove 'return {'
data = data.replace("\\", "")  # Remove backslashes
data = data.replace("nil", "false")  # Convert 'nil' to 'false'
data = re.sub(r",\s*([}])", r"\1", data)  # Remove trailing commas before closing braces
if data.endswith(','):
    data = data[:-1]  # Remove trailing comma
data = data.rstrip('},')  # Remove the final closing brace

# Step 3: Split the cleaned data into lines
lines = data.split("},")  # Split data into individual items

# Step 4: Insert each line into the SQLite database
for line in lines:
    values = [value.strip() for value in line.split(',')]  # Split by commas and strip extra spaces
    
    # Extract item_id, item_name, quantity, price, seller, and time
    item_id = values[22]  # Assuming index 22 is item_id
    item_name = values[8].replace("\"", "")  # Remove quotes from item_name
    quantity = values[10]  # Assuming index 10 is quantity
    price = values[16]  # Assuming index 16 is price
    seller = values[19].replace("\"", "")  # Remove quotes from item_name
    time = values[7]  # Assuming index 7 is time
    
    # Insert the extracted values into the database
    query = """
    INSERT INTO items (item_id, item_name, quantity, price, seller, time)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    
    # Execute the query with the extracted values
    cursor.execute(query, (item_id, item_name, quantity, price, seller, time))
    
    # Print the extracted values for verification
    #print(f"Item ID: {item_id}, Item Name: {item_name}, Quantity: {quantity}, Price: {price}, Seller: {seller}, Time: {time}")

# Commit the transaction to save the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data inserted successfully!")
