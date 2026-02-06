import sqlite3

# Connect to your existing database
conn = sqlite3.connect('cars.db')
cursor = conn.cursor()

try:
    # This command adds the missing column to your existing table
    cursor.execute('ALTER TABLE cars ADD COLUMN image_file TEXT')
    conn.commit()
    print("Success: image_file column added to cars table.")
except sqlite3.OperationalError as e:
    # If the column is already there, this will prevent a crash
    print(f"Note: {e}")
finally:
    conn.close()