import os
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from werkzeug.utils import secure_filename
from services.car_service import CarService  # Assuming you have this service

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key in production

UPLOAD_FOLDER = os.path.join('static', 'image')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

car_service = CarService()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Implement sending email or save message here
        flash(f'Thank you, {name}! Your message has been received.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file.save(os.path.join(upload_folder, filename))
            form_data['image_url'] = f'/static/image/{filename}'

        success, message = car_service.add_car_service(form_data)

        if success:
            flash(message, 'success')
            return redirect(url_for('all_cars'))
        else:
            flash(message, 'error')

    return render_template('add_car.html')


@app.route('/all_cars')
def all_cars():
    page = request.args.get('page', 1, type=int)
    per_page = 8

    if not any(request.args.values()):
        all_cars_list = car_service.get_all_cars()  # Or your logic
    else:
        model = request.args.get('model')
        year = request.args.get('year', type=int)
        price_max = request.args.get('price_max', type=int)
        sort_by = request.args.get('sort_by')

        all_cars_list = car_service.search_cars(year=year, model=model, price_max=price_max, sort_by=sort_by)

    total = len(all_cars_list)
    cars = all_cars_list[(page - 1) * per_page: page * per_page]
    total_pages = (total + per_page - 1) // per_page

    return render_template('all_cars.html', cars=cars, page=page, total_pages=total_pages, request=request)

@app.route('/cars/view/<int:car_id>')
def view_car(car_id):
    car = car_service.get_car_by_id(car_id)
    if not car:
        abort(404)
    timestamp = int(datetime.utcnow().timestamp())
    return render_template('view_car.html', car=car, timestamp=timestamp)

@app.route('/cars/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    success = car_service.delete_car_by_id(car_id)
    if not success:
        abort(404)
    flash("Car deleted successfully!", "success")
    return redirect(url_for('all_cars'))

@app.route('/favorite')
def favorite():
    favorite_cars = car_service.get_favorite_cars()
    return render_template('favorite.html', favorite_cars=favorite_cars)

@app.route('/add_to_favorites/<int:car_id>', methods=['POST'])
def add_to_favorites(car_id):
    success, message = car_service.add_to_favorites(car_id)
    flash(message)
    return redirect(url_for('favorite', car_id=car_id))


@app.route('/remove_from_favorites/<int:car_id>', methods=['POST'])
def remove_from_favorites(car_id):
    success, message = car_service.remove_from_favorites(car_id)
    flash(message)
    return redirect(url_for('favorite'))

if __name__ == '__main__':
    app.run(debug=True)
