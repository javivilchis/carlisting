from mypython import Car, CarManager

def main_menu():
    """Display the main menu options"""
    print("\n=== Car Manager System ===")
    print("1. Add a new car")
    print("2. Remove a car")
    print("3. List all cars")
    print("4. Start a car")
    print("5. Stop a car")
    print("6. Find a car")
    print("7. Exit")
    print("=" * 27)

def get_car_details():
    """Get car details from user input"""
    make = input("Enter car make: ").strip()
    model = input("Enter car model: ").strip()
    year = int(input("Enter car year: "))
    color = input("Enter car color: ").strip()
    return make, model, year, color

def get_car_search_details():
    """Get make and model for car search"""
    make = input("Enter car make: ").strip()
    model = input("Enter car model: ").strip()
    return make, model

def run_car_manager():
    """Main function to run the car manager interface"""
    manager = CarManager()
    
    while True:
        main_menu()
        try:
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == "1":
                # Add a new car
                try:
                    make, model, year, color = get_car_details()
                    new_car = Car(make, model, year, color)
                    manager.add_car(new_car)
                except ValueError:
                    print("Invalid input. Please enter a valid year.")
                except Exception as e:
                    print(f"Error adding car: {e}")
            
            elif choice == "2":
                # Remove a car
                make, model = get_car_search_details()
                car = manager.find_car(make, model)
                if car:
                    manager.remove_car(car)
                else:
                    print(f"Car {make} {model} not found.")
            
            elif choice == "3":
                # List all cars
                manager.list_cars()
            
            elif choice == "4":
                # Start a car
                make, model = get_car_search_details()
                car = manager.find_car(make, model)
                if car:
                    car.start()
                else:
                    print(f"Car {make} {model} not found.")
            
            elif choice == "5":
                # Stop a car
                make, model = get_car_search_details()
                car = manager.find_car(make, model)
                if car:
                    car.stop()
                else:
                    print(f"Car {make} {model} not found.")
            
            elif choice == "6":
                # Find a car
                make, model = get_car_search_details()
                car = manager.find_car(make, model)
                if car:
                    print(f"Found: {car} - Running: {car.is_running}")
                else:
                    print(f"Car {make} {model} not found.")
            
            elif choice == "7":
                # Exit
                print("Thank you for using Car Manager System!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        
        except KeyboardInterrupt:
            print("\n\nExiting Car Manager System...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_car_manager()