import random
class CarService:
    def __init__(self):
        self.cars = [
            {"make": "Toyota", "model": "Camry", "year": 2018, "color": "Red", "price": "15000", "mileage": "50000"},
            {"make": "Honda", "model": "Civic", "year": 2019, "color": "Blue", "price": "16000", "mileage": "40000"},
        ]

    def get_random_cars(self, count=10):
        return random.sample(self.cars, min(count, len(self.cars)))

    def add_car(self, car):
        self.cars.append(car)

    def add_car_service(self, form_data):
        make = form_data.get('make', '').strip()
        model = form_data.get('model', '').strip()
        year = form_data.get('year', '').strip()
        color = form_data.get('color', '').strip()
        price = form_data.get('price', '').strip()
        mileage = form_data.get('mileage', '').strip()

        # Validate
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
