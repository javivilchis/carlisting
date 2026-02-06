import subprocess
import sys

def install_sqlite3():
    """
    Check if sqlite3 is available and install if needed.
    Note: sqlite3 is part of Python's standard library since Python 2.5
    """
    try:
        import sqlite3
        print("sqlite3 is already available (part of Python standard library)")
    except ImportError:
        print("sqlite3 not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pysqlite3"])
            print("sqlite3 installed successfully")
        except subprocess.CalledProcessError:
            print("Failed to install sqlite3. Please install manually.")
            sys.exit(1)

# Ensure cars.db file has read and write permissions
import os
db_path = 'cars.db'
if os.path.exists(db_path):
    os.chmod(db_path, 0o666)  # Set read and write permissions for owner, group, and others

# Ensure sqlite3 is available before running the application
install_sqlite3()
import sqlite3
from werkzeug.utils import secure_filename

class Car:
  def __init__(self, make: str, model: str, year: int, color: str):
    self.make = make
    self.model = model
    self.year = year
    self.color = color
    self.is_running = False
  
  def start(self):
    self.is_running = True
    print(f"{self.year} {self.make} {self.model} is now running.")
  
  def stop(self):
    self.is_running = False
    print(f"{self.year} {self.make} {self.model} has stopped.")
  
  def __str__(self):
    return f"{self.year} {self.color} {self.make} {self.model}"

class CarManager:
  def __init__(self):
    self.cars = []
    # Initialize SQLite database connection
    self.conn = sqlite3.connect('cars.db')
    self.cursor = self.conn.cursor()
    # Create cars table if it doesn't exist
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        color TEXT NOT NULL,
        is_running BOOLEAN DEFAULT FALSE,
        image_file TEXT
      )
    ''')
    self.conn.commit()
  
  def create_car(self, car):
    # 1. Create a local connection for this specific thread/request
    conn = sqlite3.connect('cars.db')
    cursor = conn.cursor()
    
    try:
        # 2. Add to your local list (if you are still using self.cars)
        self.cars.append(car)
        
        # 3. Use the local 'cursor' (NOT self.cursor) to insert
        cursor.execute('''
          INSERT INTO cars (make, model, year, color, is_running, image_file)
          VALUES (?, ?, ?, ?, ?)
        ''', (car.make, car.model, car.year, car.color, car.is_running, None))
        
        # 4. Use the local 'conn' (NOT self.conn) to commit
        conn.commit()
        print(f"Added: {car}")
        
    except Exception as e:
        print(f"Database error: {e}")
        raise e  # Re-raise so the API knows it failed
    finally:
        # 5. Always close the connection for this thread
        conn.close()


  def add_car(self, car, image_file=None):
    # 1. Handle image saving
    image_filename = None
    if image_file and image_file.filename != '':
        # Use secure_filename to prevent directory traversal attacks
        image_filename = secure_filename(image_file.filename)
        
        # Ensure path is relative to the app execution directory
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        upload_path = os.path.join(upload_folder, image_filename)
        image_file.save(upload_path)

    # 2. Database Operation
    # Using a context manager (with) for the connection is even safer
    try:
        with sqlite3.connect('cars.db') as conn:
            cursor = conn.cursor()
            
            # Ensure the car object has all these attributes!
            # Note: Added car.is_running - make sure your Car class has this.
            cursor.execute('''
              INSERT INTO cars (make, model, year, color, is_running, image_file)
              VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                car.make, 
                car.model, 
                car.year, 
                car.color, 
                getattr(car, 'is_running', True), # Fallback to True if missing
                image_filename
            ))
            conn.commit()
            
        # Update local list only if DB insert succeeds
        self.cars.append(car)
        print(f"Successfully added {car.make} to DB and local list.")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise e
    except Exception as e:
        print(f"General error in add_car: {e}")
        raise e

  # def add_car(self, car):
  #   self.cars.append(car)
  #   # Insert car into SQLite database
  #   self.cursor.execute('''
  #     INSERT INTO cars (make, model, year, color, is_running)
  #     VALUES (?, ?, ?, ?, ?)
  #   ''', (car.make, car.model, car.year, car.color, car.is_running))
  #   self.conn.commit()
  #   print(f"Added: {car}")
  
  def remove_car(self, car):
    self.cars.remove(car)
    # Remove car from SQLite database
    self.cursor.execute('''
      DELETE FROM cars WHERE make = ? AND model = ? AND year = ? AND color = ?
    ''', (car.make, car.model, car.year, car.color))
    self.conn.commit()
    print(f"Removed: {car}")
  
  import sqlite3

  def list_cars(self):
    # 1. Connect inside the method to avoid Thread errors
    conn = sqlite3.connect('cars.db')
    
    # 2. Use Row factory to allow column name access (e.g., car['make'])
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM cars")
        rows = cursor.fetchall()
        
        # 3. Convert sqlite3.Row objects into a list of real dictionaries
        cars_list = [dict(row) for row in rows]
        return cars_list
    finally:
        conn.close()

  
  def find_car(self, make, model):
    for car in self.cars:
      if car.make == make and car.model == model:
        return car
    return None

  def get_car(self, car_id):
    with sqlite3.connect('cars.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
  def delete_car_by_id(self, car_id):
    with sqlite3.connect('cars.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        conn.commit()
    return True  
    
  def __del__(self):
    # Close database connection when CarManager is destroyed
    if hasattr(self, 'conn'):
      self.conn.close()





