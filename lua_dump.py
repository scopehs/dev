from lupa import LuaRuntime

# Create a Lua runtime environment
lua = LuaRuntime(unpack_returned_tuples=True)

# Function to read Lua file and extract ropes
def extract_ropes_from_file(filename):
    with open(filename, 'r') as file:
        lua_code = file.read()

    # Debug: Print the Lua code
    print("Lua Code Loaded:")
    print(lua_code)

    # Execute the Lua code in the Lua runtime
    lua.execute(lua_code)
    
    # Check if AucScanData exists in the Lua environment
    if 'AucScanData' not in lua.globals():
        print("Error: AucScanData is not found in the Lua environment.")
        return None

    # Access the AucScanData variable from the Lua environment
    AucScanData = lua.globals().AucScanData

    # Check if the 'ropes' field exists in the structure
    if 'scans' not in AucScanData or 'Spineshatter_Horde' not in AucScanData['scans']:
        print("Error: Unable to locate the 'Spineshatter_Horde' scan data.")
        return None
    
    if 'ropes' not in AucScanData['scans']['Spineshatter_Horde']:
        print("Error: 'ropes' not found.")
        return None

    # Extract the first entry from the ropes field
    ropes_code = AucScanData['scans']['Spineshatter_Horde']['ropes'][0]
    
    # Check if ropes_code is None
    if ropes_code is None:
        print("Error: ropes_code is None.")
        return None

    # Debug: Print extracted ropes code
    print("Extracted Ropes Code:")
    print(ropes_code)

    # Execute the extracted Lua string from ropes
    try:
        ropes = lua.execute(ropes_code)
    except Exception as e:
        print(f"Error executing Lua code: {e}")
        return None

    print('Found Auction House Data')

    # Convert the ropes from a Lua table to a Python list and print it
    print("Ropes Section:")
    for rope in ropes:
        print(rope)

    return ropes

# File path to your Lua file (change this to the actual file path)
filename = 'auc_parsed.lua'

# Extract the ropes section
ropes = extract_ropes_from_file(filename)

# If you want to see the ropes directly in the Python console
if ropes is not None:
    print("\nFull Ropes Data:")
    print(ropes)
else:
    print("No ropes data found.")
