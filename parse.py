import re

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
# Remove 'return {' at the start of the data (if present)
data = data.replace("return {", "")

#print(data)
# Remove all backslashes
data = data.replace("\\", "")

# Convert 'nil' to 'false'
data = data.replace("nil", "false")

# Remove trailing commas before closing braces
data = re.sub(r",\s*([}])", r"\1", data)

# Remove the trailing comma after the last entry (if any)
if data.endswith(','):
    data = data[:-1]

# Remove the final closing brace and curly brace
data = data.rstrip('},')

# Step 3: Split the cleaned data into lines
lines = data.split("},{")
#print(lines)

# Step 4: Iterate through each line, split it into values, and print the extracted values
# for line in lines:
#     values = [value.strip() for value in line.split(',')]  # Split by commas and strip extra spaces
    
#     # Extract item_id (index 22), item_name (index 8), price (index 16), and time (index 7)
#     item_id = values[22] if len(values) > 22 else "N/A"
#     item_name = values[8] if len(values) > 8 else "N/A"
#     price = values[16] if len(values) > 16 else "N/A"
#     time = values[7] if len(values) > 7 else "N/A"
    
#     # Print the extracted values per line
#     print(f"Item ID: {item_id}, Item Name: {item_name}, Price: {price}, Time: {time}")


## Debug Code

# Iterate through each line, split the line into values, and print each value with its index
# Open the file in write mode (or append mode if you don't want to overwrite the file)
with open('output.txt', 'w') as file:
    for line in lines:
        values = [value.strip() for value in line.split(',')]  # Split by commas and strip extra spaces
        
        file.write("Processing Line:\n")
        for index, value in enumerate(values):
            file.write(f"  Index {index}: {value}\n")
        file.write("-" * 40 + "\n")  # Separator line for readability