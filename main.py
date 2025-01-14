from database import insert_to_sql, create_database
from lua_to_dict import load_lua_file, lua_to_dict
import json

# Create the Table
create_database()

# Path to the Lua file
lua_file_path = 'Auc-ScanData.lua'  # Replace with your actual Lua file name

# Load the Lua file and get the AucScanData table
AucScanData = load_lua_file(lua_file_path)

# Convert the Lua table to a Python dictionary
auc_scan_data_dict = lua_to_dict(AucScanData)

# Extract ropes data
ropes_data = auc_scan_data_dict['scans']['Spineshatter_Horde']['ropes']

# Print the length of each collection in ropes_data
for key, value in ropes_data.items():
    print(f"{key}: {len(value)}")  # Assuming value is a collection

# Save ropes data to output.json
output_file_path = 'output.json'

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(ropes_data, json_file, ensure_ascii=False, indent=4)

# print(f"Ropes data has been saved to {output_file_path}.")

# Load in the JSON and Process
# Open and load the JSON file
with open('output.json', 'r', encoding='utf-8', errors="ignore") as file:
    data = json.load(file)
    
# Define a function to do something with each key
def process_key(key, value):
    # Replace this with whatever action you want to perform
    # print(f"Processing key: {key} with value: {value}")
    # Insert to SQL
    insert_to_sql(value)

# Loop through each key-value pair in the JSON data
for key, value in data.items():
    process_key(key, value)
