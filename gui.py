import tkinter as tk
from tkinter import filedialog, messagebox
from database import insert_to_sql, create_database
from lua_to_dict import load_lua_file, lua_to_dict
import json
import os

class AucScanDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AucScanData Processor")
        self.root.geometry("400x300")
        
        self.lua_file_path = ""
        self.ropes_data = None

        # Create the widgets
        self.create_widgets()

    def create_widgets(self):
        # File loading button
        self.load_file_button = tk.Button(self.root, text="Load Lua File", command=self.load_lua_file)
        self.load_file_button.pack(pady=10)

        # Process button
        self.process_button = tk.Button(self.root, text="Process Data", command=self.process_data, state=tk.DISABLED)
        self.process_button.pack(pady=10)

        # Save button
        self.save_button = tk.Button(self.root, text="Save Data to JSON", command=self.save_to_json, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        # Insert button
        self.insert_button = tk.Button(self.root, text="Insert Data to SQL", command=self.insert_to_sql, state=tk.DISABLED)
        self.insert_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Waiting for action...", anchor="w")
        self.status_label.pack(fill=tk.X, pady=10)

    def load_lua_file(self):
        # Open file dialog to choose the Lua file
        self.lua_file_path = filedialog.askopenfilename(title="Select Lua File", filetypes=[("Lua files", "*.lua")])
        
        if self.lua_file_path:
            # Load the Lua file and get the AucScanData table
            try:
                AucScanData = load_lua_file(self.lua_file_path)  # Pass the file path instead of the file object
                auc_scan_data_dict = lua_to_dict(AucScanData)
                
                # Extract the ropes data
                self.ropes_data = auc_scan_data_dict.get('scans', {}).get('Spineshatter_Horde', {}).get('ropes', {})

                if isinstance(self.ropes_data, dict):
                    self.status_label.config(text="Status: Lua file loaded and data processed.")
                    self.process_button.config(state=tk.NORMAL)  # Enable the process button
                else:
                    self.status_label.config(text="Status: No ropes data found.")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def process_data(self):
        # Process the data into JSON format
        if self.ropes_data:
            output_file_path = "output.json"
            try:
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(self.ropes_data, json_file, ensure_ascii=False, indent=4)
                self.status_label.config(text=f"Status: Data saved to {output_file_path}.")
                self.save_button.config(state=tk.NORMAL)  # Enable the save button
                self.insert_button.config(state=tk.NORMAL)  # Enable the insert button
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_to_json(self):
        # This is already handled in process_data(), so you can skip extra implementation here
        pass

    def insert_to_sql(self):
        # Insert data into SQL database
        try:
            if isinstance(self.ropes_data, dict):
                for key, value in self.ropes_data.items():
                    insert_to_sql(value)  # Assuming value is insertable directly
            self.status_label.config(text="Status: Data inserted into SQL.")
            messagebox.showinfo("Success", "Data successfully inserted into the SQL database.")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Initialize the database
    create_database()  # Ensure this is called only once to initialize your DB

    # Create the main window and run the app
    root = tk.Tk()
    app = AucScanDataApp(root)
    root.mainloop()
