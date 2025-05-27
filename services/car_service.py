import itertools
import json
from pathlib import Path
from utils import validators


class CarService:
    _id_counter = itertools.count(1)
    DATA_FILE = Path("data/cars_data.json")

    def __init__(self):
        self.favorites = set()
        self.cars = self._load_initial_cars()

    def _load_initial_cars(self):
        if not self.DATA_FILE.exists():
            return []

        with self.DATA_FILE.open("r", encoding="utf-8") as f:
            car_list = json.load(f)

        # Stelle sicher, dass jede geladene ID einzigartig ist
        for car in car_list:
            car["id"] = next(self._id_counter)
        return car_list

    def _save_cars_to_file(self):
        # Speichere Autos ohne die ID, wenn du willst
        with self.DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(self.cars, f, indent=2, ensure_ascii=False)

    # Add a new car to the service
    def add_car(self, car):
        car["id"] = next(self._id_counter)
        self.cars.append(car)
        self._save_cars_to_file()

    # Get all cars
    def get_all_cars(self):
        return self.cars

    # Add a new car from form input
    def add_car_service(self, form_data):
        make = form_data.get('make', '').strip()
        model = form_data.get('model', '').strip()
        year = form_data.get('year', '').strip()
        color = form_data.get('color', '').strip()
        price = form_data.get('price', '').strip()
        mileage = form_data.get('mileage', '').strip()
        image_url = form_data.get('image_url', '').strip()

        if not validators.validate_required_fields(make, model, year):
            return False, 'Please fill in all required fields.'

        if not validators.validate_year(year):
            return False, 'Please enter a valid year.'

        if not validators.validate_price(price):
            return False, 'Please enter a valid price.'

        if not validators.validate_mileage(mileage):
            return False, 'Please enter a valid mileage.'

        new_car = {
            "make": make,
            "model": model,
            "year": int(year),
            "color": color,
            "price": int(price),
            "mileage": int(mileage),
            "image_url": image_url,
        }

        self.add_car(new_car)
        return True, 'Car added successfully!'

    # Search cars based on criteria
    def search_cars(self, year=None, model=None, price_max=None, sort_by=None):
        results = self.cars

        if year is not None:
            results = [car for car in results if car.get('year') == year]

        if model:
            results = [car for car in results if car.get('model', '').lower() == model.lower()]

        if price_max is not None:
            results = [
                car for car in results
                if isinstance(car.get('price'), int) and car['price'] <= price_max
            ]

        if sort_by in ['year', 'price', 'mileage']:
            results.sort(key=lambda car: car.get(sort_by, 0))

        return results

    # Get a car by ID
    def get_car_by_id(self, car_id):
        for car in self.cars:
            if car["id"] == car_id:
                return car
        return None

    # Delete a car by ID
    def delete_car_by_id(self, car_id):
        for i, car in enumerate(self.cars):
            if car["id"] == car_id:
                del self.cars[i]
                self._save_cars_to_file()
                return True
        return False

    # Add a car to favorites
    def add_to_favorites(self, car_id):
        if self.get_car_by_id(car_id):
            self.favorites.add(car_id)
            return True, "Car added to favorites."
        return False, "Car not found."

    # Remove a car from favorites
    def remove_from_favorites(self, car_id):
        if car_id in self.favorites:
            self.favorites.remove(car_id)
            return True, "Car removed from favorites."
        return False, "Car not in favorites."

    # Get the last added car ID
    def get_last_added_car_id(self):
        if self.cars:
            return self.cars[-1]["id"]
        return None

    # Get all favorite cars
    def get_favorite_cars(self):
        return [car for car in self.cars if car["id"] in self.favorites]
