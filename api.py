from flask import Flask, request, jsonify, render_template
import mypython
from mypython import Car, CarManager

app = Flask(__name__)
manager = CarManager()


@app.route('/')
def home():
    # Retrieve the list of dictionaries from your manager
    cars_data = manager.list_cars()
    # Pass it to the template as 'data'
    return render_template("index.html", data=cars_data)

@app.route('/car/<int:car_id>')
def car_details(car_id):
    car = manager.get_car(car_id)
    if not car:
        return "Car not found", 404
    
    return render_template('details.html', car=car)

@app.route('/api/cars', methods=['GET'])
def api_list_cars():
    cars = manager.list_cars()
    return jsonify({"message": "Cars retrieved successfully", "data": cars})

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    try:
        manager.delete_car_by_id(car_id)
        return jsonify({"message": "Car deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route('/api/cars', methods=['POST'])
def add_car_route(): # Renamed the function slightly to avoid confusion with the manager method
    try:
        # 1. Capture text data from multipart form
        make = request.form.get('make')
        model = request.form.get('model')
        year_raw = request.form.get('year')
        color = request.form.get('color')

        # 2. Capture the image file
        image = request.files.get('image_file')

        if not make or not model:
            return jsonify({"error": "Make and Model are required"}), 400

        # 3. Safely convert year to integer
        try:
            year = int(year_raw) if year_raw else 0
        except ValueError:
            year = 0

        # 4. Build your Car object
        new_car_object = Car(
            make=make, 
            model=model, 
            year=year, 
            color=color
        )

        # 5. FIX: Call manager.add_car (instead of create_car) to match your class
        manager.add_car(new_car_object, image)
        
        return jsonify({"message": "Car created successfully"}), 201
        
    except Exception as e:
        print(f"Debug Error: {e}") 
        return jsonify({"error": str(e), "message": "Failed to create car"}), 400

@app.route('/api/cars/<make>/<model>', methods=['DELETE'])
def remove_car(make, model):
  """Remove a car"""
  # Communicate with CarManager to delete a car
  result = manager.delete_car(make, model)
  if "error" in result:
    return jsonify({"message": "Failed to delete car", "data": result}), 404
  return jsonify({"message": "Car deleted successfully", "data": result})

@app.route('/api/cars/<make>/<model>', methods=['GET'])
def find_car(make, model):
  """Find a specific car"""
  # Communicate with CarManager to read car information
  result = manager.read_car(make, model)
  if "error" in result:
    return jsonify({"message": "Car not found", "data": result}), 404
  return jsonify({"message": "Car found successfully", "data": result})

@app.route('/api/cars/<make>/<model>', methods=['PUT'])
def update_car(make, model):
  """Update a car"""
  try:
    data = request.json
    # Communicate with CarManager to update car information
    result = manager.update_car(make, model, data)
    if "error" in result:
      return jsonify({"message": "Failed to update car", "data": result}), 404
    return jsonify({"message": "Car updated successfully", "data": result})
  except Exception as e:
    return jsonify({"error": str(e), "message": "Failed to update car"}), 400

@app.route('/api/cars/<make>/<model>/start', methods=['POST'])
def start_car(make, model):
  """Start a car"""
  # Communicate with CarManager to find the car, then with Car to start it
  car = manager.find_car(make, model)
  if car:
    start_result = car.start()
    return jsonify({"message": "Car started successfully", "car_response": start_result})
  return jsonify({"error": "Car not found", "message": "Failed to start car - car does not exist"}), 404

@app.route('/api/cars/<make>/<model>/stop', methods=['POST'])
def stop_car(make, model):
  """Stop a car"""
  # Communicate with CarManager to find the car, then with Car to stop it
  car = manager.find_car(make, model)
  if car:
    stop_result = car.stop()
    return jsonify({"message": "Car stopped successfully", "car_response": stop_result})
  return jsonify({"error": "Car not found", "message": "Failed to stop car - car does not exist"}), 404

if __name__ == "__main__":
  app.run(port=8000,debug=True)
