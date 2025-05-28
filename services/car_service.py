import itertools, json, os
from pathlib import Path
from utils import validators

# CarService-Klasse zur Verwaltung von Autos
class CarService:
    _id_counter = itertools.count(1)
    DATA_FILE = Path("data/cars_data.json")

    def __init__(self):
        self.favorites = set()
        self.cars = self._load_initial_cars()

    # Lade Anfangsautos aus der JSON-Datei
    def _load_initial_cars(self):
        if not self.DATA_FILE.exists():
            return []

        # Lade Autos aus der JSON-Datei
        with self.DATA_FILE.open("r", encoding="utf-8") as f:
            car_list = json.load(f)

        # Füge IDs zu den Autos hinzu, falls sie nicht vorhanden sind
        for car in car_list:
            car["id"] = next(self._id_counter)
        return car_list

    # Speichere Autos in die JSON-Datei
    def _save_cars_to_file(self):
     with self.DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(self.cars, f, indent=2, ensure_ascii=False)

    # Füge ein neues Auto der Liste hinzu und speichere es in die Datei
    def add_car(self, car):
        car["id"] = next(self._id_counter)
        self.cars.append(car)
        self._save_cars_to_file()

    # Gib alle Autos zurück
    def get_all_cars(self):
        return self.cars

    # Füge ein neues Auto über Formulardaten hinzu
    def add_car_service(self, form_data):
        errors = {}

        make = form_data.get('make', '').strip()
        model = form_data.get('model', '').strip()
        year = form_data.get('year', '').strip()
        color = form_data.get('color', '').strip()
        price = form_data.get('price', '').strip()
        mileage = form_data.get('mileage', '').strip()
        image_url = form_data.get('image_url', '').strip()

        if not validators.validate_required_fields(make, model, year):
            if not make:
                errors['make'] = 'Pflichtfeld'
            if not model:
                errors['model'] = 'Pflichtfeld'
            if not year:
                errors['year'] = 'Pflichtfeld'

        if year and not validators.validate_year(year):
            errors['year'] = 'Ungültiges Jahr'

        if price and not validators.validate_price(price):
            errors['price'] = 'Ungültiger Preis'

        if mileage and not validators.validate_mileage(mileage):
            errors['mileage'] = 'Ungültiger Kilometerstand'

        if errors:
            return False, 'Bitte korrigiere die markierten Felder.', form_data, errors

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
        return True, 'Auto erfolgreich hinzugefügt!', None, None

    # Suche Autos anhand von Kriterien
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

    # Hole ein Auto anhand der ID
    def get_car_by_id(self, car_id):
        for car in self.cars:
            if car["id"] == car_id:
                return car
        return None

    # Lösche ein Auto anhand der ID
    def delete_car_by_id(self, car_id):
        for i, car in enumerate(self.cars):
            if car["id"] == car_id:
                # Bild löschen, falls vorhanden
                image_path = car.get("image_url")
                if image_path:
                    # Erstelle den vollständigen Pfad zum Bild basierend auf dem aktuellen Arbeitsverzeichnis
                    full_image_path = os.path.join(os.getcwd(), image_path)
                    try:
                        if os.path.exists(full_image_path):
                            os.remove(full_image_path)
                            print(f"Bild gelöscht: {full_image_path}")
                    except Exception as e:
                        print(f"Fehler beim Löschen des Bildes: {e}")

                # Auto aus der Liste entfernen
                del self.cars[i]
                self._save_cars_to_file()
                return True
        return False

    # Füge ein Auto zu den Favoriten hinzu
    def add_to_favorites(self, car_id):
        if self.get_car_by_id(car_id):
            self.favorites.add(car_id)
            return True, "Auto zu Favoriten hinzugefügt."
        return False, "Auto nicht gefunden."

    # Entferne ein Auto aus den Favoriten
    def remove_from_favorites(self, car_id):
        if car_id in self.favorites:
            self.favorites.remove(car_id)
            return True, "Auto aus Favoriten entfernt."
        return False, "Auto nicht in Favoriten."

    # Hole die ID des zuletzt hinzugefügten Autos
    def get_last_added_car_id(self):
        if self.cars:
            return self.cars[-1]["id"]
        return None

    # Hole alle Favoriten-Autos
    def get_favorite_cars(self):
        return [car for car in self.cars if car["id"] in self.favorites]
