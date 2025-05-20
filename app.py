from flask import Flask, render_template, request, flash, redirect, url_for
from services.car_service import CarService  # Make sure this file exists in a `services/` folder

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure value in production

car_service = CarService()

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
        # You can implement sending emails or saving to a DB here
        flash(f'Thank you, {name}! Your message has been received.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        success, message = car_service.add_car_service(request.form)

        if success:
            flash(message, 'success')
            return redirect(url_for('all_cars'))
        else:
            flash(message, 'error')

    return render_template('add_car.html')

@app.route('/all_cars')
def all_cars():
    if not any(request.args.values()):
        cars = car_service.get_random_cars(10)
    else:
        model = request.args.get('model')
        year = request.args.get('year', type=int)
        price_max = request.args.get('price_max', type=int)
        sort_by = request.args.get('sort_by')

        cars = car_service.search_cars(year=year, model=model, price_max=price_max, sort_by=sort_by)

    return render_template('all_cars.html', cars=cars)

if __name__ == '__main__':
    app.run(debug=True)
