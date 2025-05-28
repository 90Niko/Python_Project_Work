import os
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from werkzeug.utils import secure_filename
from services.car_service import CarService  # Importiere den CarService

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Setze den Secret-Key (in Produktion sicher wählen)

UPLOAD_FOLDER = os.path.join('static', 'image')  # Upload-Ordner für Bilder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Erlaubte Dateiendungen für Bilder

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Upload-Ordner in Flask-Konfiguration speichern

# CarService initialisieren
car_service = CarService()


# Prüfen, ob Datei eine erlaubte Dateiendung hat
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Startseite – leitet auf /index weiter
@app.route('/')
def home():
    return redirect(url_for('index'))


# Index-Seite rendern
@app.route('/index')
def index():
    return render_template('index.html')


# About-Seite rendern
@app.route('/about')
def about():
    return render_template('about.html')


# Kontakt-Seite mit GET und POST
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Formulardaten auslesen
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Hier könnte man z.B. eine E-Mail senden oder Nachricht speichern
        flash(f'Danke, {name}! Deine Nachricht wurde empfangen.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


# Neue Auto-Daten erfassen und speichern
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        file = request.files.get('image')

        # Wenn eine Bilddatei hochgeladen wurde und erlaubt ist
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Sicheren Dateinamen erstellen
            upload_folder = app.config['UPLOAD_FOLDER']

            # Upload-Ordner erstellen, falls er nicht existiert
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Bild speichern
            file.save(os.path.join(upload_folder, filename))

            # Pfad zum Bild im Formular-Daten-Dict speichern
            form_data['image_url'] = f'static/image/{filename}'

        # Auto über CarService hinzufügen
        success, message = car_service.add_car_service(form_data)

        if success:
            flash(message, 'success')
            # Nach Hinzufügen auf Detailseite weiterleiten
            return redirect(url_for('view_car', car_id=car_service.get_last_added_car_id(), redirect_after=1))
        else:
            flash(message, 'error')

    return render_template('add_car.html')


# Alle Autos anzeigen, mit Filter- und Paginierungsfunktion
@app.route('/all_cars')
def all_cars():
    page = request.args.get('page', 1, type=int)
    per_page = 8  # Autos pro Seite

    # Wenn keine Filter gesetzt sind, alle Autos holen
    if not any(request.args.values()):
        all_cars_list = car_service.get_all_cars()
    else:
        # Filter aus URL-Parametern lesen
        model = request.args.get('model')
        year = request.args.get('year', type=int)
        price_max = request.args.get('price_max', type=int)
        sort_by = request.args.get('sort_by')

        # Autos mit Filter suchen
        all_cars_list = car_service.search_cars(year=year, model=model, price_max=price_max, sort_by=sort_by)

    total = len(all_cars_list)
    # Autos für die aktuelle Seite auswählen
    cars = all_cars_list[(page - 1) * per_page: page * per_page]
    total_pages = (total + per_page - 1) // per_page  # Gesamtseiten berechnen

    return render_template('all_cars.html', cars=cars, page=page, total_pages=total_pages, request=request)


# Detailansicht für ein einzelnes Auto
@app.route('/cars/view/<int:car_id>')
def view_car(car_id):
    car = car_service.get_car_by_id(car_id)
    if not car:
        abort(404)  # 404 wenn Auto nicht gefunden
    return render_template('view_car.html', car=car)


# Auto löschen (POST-Methode)
@app.route('/cars/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    success = car_service.delete_car_by_id(car_id)
    if not success:
        abort(404)  # 404 wenn Auto nicht gefunden
    flash("Auto erfolgreich gelöscht!", "success")
    return redirect(url_for('all_cars'))


# Favoriten-Seite anzeigen
@app.route('/favorite')
def favorite():
    favorite_cars = car_service.get_favorite_cars()
    if not favorite_cars:
        flash("Du hast keine Lieblingsautos.", "info")
    return render_template('favorite.html', favorite_cars=favorite_cars)


# Auto zu Favoriten hinzufügen (POST)
@app.route('/add_to_favorites/<int:car_id>', methods=['POST'])
def add_to_favorites(car_id):
    success, message = car_service.add_to_favorites(car_id)
    if not success:
        flash(message, "error")
    else:
        flash("Auto zu Favoriten hinzugefügt.", "success")
    return redirect(url_for('favorite', car_id=car_id))


# Auto aus Favoriten entfernen (POST)
@app.route('/remove_from_favorites/<int:car_id>', methods=['POST'])
def remove_from_favorites(car_id):
    success, message = car_service.remove_from_favorites(car_id)
    if not success:
        flash(message, "error")
    else:
        flash("Auto aus Favoriten entfernt.", "success" if success else "error")
    return redirect(url_for('favorite'))


# Fehlerseite für 404 (Seite nicht gefunden)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, message="Seite nicht gefunden"), 404


if __name__ == '__main__':
    app.run(debug=True)  # Flask-Server im Debug-Modus starten. Bei Änderungen im Code wird der Server automatisch neu gestartet.
