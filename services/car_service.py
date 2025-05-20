import random
import itertools

class CarService:
    _id_counter = itertools.count(1)  # auto-incrementing ID generator

    def __init__(self):
        self.cars = [
            {"id": next(self._id_counter), "make": "Toyota", "model": "Camry", "year": 2018, "color": "Red", "price": "15000", "mileage": "50000"},
            {"id": next(self._id_counter), "make": "Honda", "model": "Civic", "year": 2019, "color": "Blue", "price": "16000", "mileage": "40000"},
            {"id": next(self._id_counter), "make": "Ford", "model": "Focus", "year": 2020, "color": "Black", "price": "17000", "mileage": "30000"},
            {"id": next(self._id_counter), "make": "Chevrolet", "model": "Malibu", "year": 2021, "color": "White", "price": "18000", "mileage": "20000"},
            {"id": next(self._id_counter), "make": "Nissan", "model": "Altima", "year": 2022, "color": "Silver", "price": "19000", "mileage": "10000"},
            {"id": next(self._id_counter), "make": "Hyundai", "model": "Elantra", "year": 2023, "color": "Green", "price": "20000", "mileage": "5000"},
            {"id": next(self._id_counter), "make": "Kia", "model": "Optima", "year": 2024, "color": "Yellow", "price": "21000", "mileage": "0"},
            {"id": next(self._id_counter), "make": "Volkswagen", "model": "Jetta", "year": 2025, "color": "Purple", "price": "22000", "mileage": "0"},
            {"id": next(self._id_counter), "make": "Subaru", "model": "Impreza", "year": 2026, "color": "Pink", "price": "23000", "mileage": "0"},
            {"id": next(self._id_counter), "make": "Mazda", "model": "3", "year": 2027, "color": "Orange", "price": "24000", "mileage": "0"},
            {"id": next(self._id_counter), "make": "Chrysler", "model": "300", "year": 2028, "color": "Brown", "price": "25000", "mileage": "0"},
            {"id": next(self._id_counter), "make": "Dodge", "model": "Charger", "year": 2029, "color": "Gray", "price": "26000", "mileage": "0"},
        ]

    def get_random_cars(self, count=10):
        return random.sample(self.cars, min(count, len(self.cars)))

    def add_car(self, car):
        # Assign a new unique ID
        car["id"] = next(self._id_counter)
        self.cars.append(car)

    def add_car_service(self, form_data):
        make = form_data.get('make', '').strip()
        model = form_data.get('model', '').strip()
        year = form_data.get('year', '').strip()
        color = form_data.get('color', '').strip()
        price = form_data.get('price', '').strip()
        mileage = form_data.get('mileage', '').strip()

        if not make or not model or not year:
            return False, 'Please fill in all fields.'

        if not year.isdigit() or int(year) < 1886 or int(year) > 2100:
            return False, 'Please enter a valid year.'

        new_car = {
            "make": make,
            "model": model,
            "year": int(year),
            "color": color,
            "price": price,
            "mileage": mileage,
        }

        self.add_car(new_car)
        return True, 'Car added successfully!'

    def search_cars(self, year=None, model=None, price_max=None, sort_by=None):
        results = self.cars

        if year is not None:
            results = [car for car in results if car.get('year') == year]

        if model:
            results = [car for car in results if car.get('model', '').lower() == model.lower()]

        if price_max is not None:
            results = [
                car for car in results
                if car.get('price') and car['price'].isdigit() and int(car['price']) <= price_max
            ]

        if sort_by in ['year', 'price', 'mileage']:
            results.sort(key=lambda car: int(car.get(sort_by, 0)) if car.get(sort_by) and str(car.get(sort_by)).isdigit() else 0)

        return results

    # New: get a car by ID
    def get_car_by_id(self, car_id):
        for car in self.cars:
            if car["id"] == car_id:
                return car
        return None

    # New: delete a car by ID
    def delete_car_by_id(self, car_id):
        for i, car in enumerate(self.cars):
            if car["id"] == car_id:
                del self.cars[i]
                return True
        return False
