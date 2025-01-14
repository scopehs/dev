from lupa import LuaRuntime

# Initialize Lua runtime
lua = LuaRuntime(unpack_returned_tuples=True)

# Get the Lua type function
lua_type = lua.globals()['type']

# Convert Lua table to a Python dictionary
def lua_to_dict(lua_table):
    if lua_type(lua_table) == 'table':
        return {lua_to_dict(key): lua_to_dict(value) for key, value in lua_table.items()}
    elif lua_type(lua_table) == 'table':
        return [lua_to_dict(item) for item in lua_table]
    else:
        return lua_table

def load_lua_file(file_path):
    # Read the Lua file
    with open(file_path, 'r', encoding='utf-8') as lua_file:
        lua_code = lua_file.read()

    # Execute the Lua code to get the Lua table
    lua.execute(lua_code)

    # Get the Lua table
    AucScanData = lua.globals()['AucScanData']
    
    return AucScanData
