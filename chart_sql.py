import sqlite3
import time
import threading
from lightweight_charts import Chart, LineSeries
import tkinter as tk

# Function to fetch the latest data from the SQLite database
def fetch_latest_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT time, price FROM items ORDER BY time DESC LIMIT 100")
    data = cursor.fetchall()
    conn.close()
    return [{"time": int(time.mktime(row[0].timetuple())), "value": row[1]} for row in data]

# Function to update chart data
def update_chart(series, db_path):
    while True:
        try:
            # Fetch latest data from the database
            new_data = fetch_latest_data(db_path)
            if new_data:
                # Update chart with the new data
                series.set_data(new_data)
            time.sleep(5)  # Fetch data every 5 seconds
        except Exception as e:
            print(f"Error updating chart: {e}")
            break

# Create the chart and the series
def create_chart():
    # Set up the chart
    chart = Chart({
        'width': 800,
        'height': 400,
        'lineWidth': 2,
        'crosshair': {'mode': 0},
    })

    # Create the line series for the chart
    series = chart.add_line_series()

    return chart, series

# Main function to run the app
def main():
    db_path = "items.db"  # Path to your SQLite database file

    # Initialize the chart
    chart, series = create_chart()

    # Set up a new thread to fetch data and update the chart
    chart_update_thread = threading.Thread(target=update_chart, args=(series, db_path))
    chart_update_thread.daemon = True
    chart_update_thread.start()

    # Use Tkinter window to display the chart (embedded as a basic GUI)
    window = tk.Tk()
    window.title("Real-Time Data Chart")

    # Create a canvas to embed the chart (using a placeholder as Lightweight Charts doesn't directly support Tkinter)
    canvas = tk.Canvas(window, width=800, height=400)
    canvas.pack()

    # Start the Tkinter main loop
    window.mainloop()

# Run the app
if __name__ == "__main__":
    main()
