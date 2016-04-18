from flask import Flask, request, render_template, jsonify, abort, redirect, url_for, session, send_from_directory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import User, Base, Car, Dealership
import math
import os
import boto3

UPLOAD_FOLDER = '\static\image'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

server = Flask(__name__)


def connect_db():
    return create_engine('mysql+pymysql://esproject:esproject@localhost:3306/esproject1')


@server.route("/", methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        engine = connect_db()
        Base.metadata.bind = engine
        dbsessionbind = sessionmaker(bind=engine)
        dbsession = dbsessionbind()
        userexists = dbsession.query(User).filter_by(email=request.form['email']).first()
        dbsession.close()
        if not userexists:
            error = 'User does not exist!'
        else:
            if userexists.email == request.form['email'] and userexists.password == request.form['password']:
                session['logged_in'] = True
                session['user_email'] = request.form['email']
                session['user_name'] = userexists.name
                session['user_type'] = userexists.type
                session['user_id'] = userexists.userid
                return redirect(url_for('home'))
            else:
                error = 'Email or password do not match. Try Again!'
    return render_template('login.html', error=error)


@server.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@server.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        engine = connect_db()
        Base.metadata.bind = engine
        dbsessionbind = sessionmaker(bind=engine)
        dbsession = dbsessionbind()
        newuser = User(name=request.form['name'], type=request.form['type'], email=request.form['email'],
                       password=request.form['password'])
        dbsession.add(newuser)
        dbsession.commit()
        dbsession.close()
        session['logged_in'] = True
        session['user_email'] = request.form['email']
        session['user_name'] = request.form['name']
        session['user_type'] = request.form['type']
        return redirect(url_for('home'))
    return render_template('register.html', error=error)


@server.route("/home", methods=['GET'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if session['user_type'] == 'client':
        return render_template('client_home.html')
    else:
        return render_template('owner_home.html')


@server.route("/search", methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if session['user_type'] == 'client':
        return render_template('client_search.html')
    else:
        return render_template('owner_search.html')


@server.route("/listclients", methods=['GET', 'POST'])
def listclients():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()

    if request.method == 'POST':
        userlist = dbsession.query(User).filter_by(name=request.json['so_search']).all()
    else:
        userlist = dbsession.query(User).filter_by(type='client').all()

    dbsession.close()
    data = []
    for item in userlist:
        data.append({'name': item.name, 'email': item.email})
    print(data)
    return jsonify(data=data)


@server.route("/mycars", methods=['GET', 'POST'])
def mycars():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('mycars.html')


@server.route("/listmycars", methods=['GET', 'POST'])
def listmycars():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()

    carslist = dbsession.query(Car).filter_by(owner_id=session['user_id']).all()

    dbsession.close()
    data = []
    for item in carslist:
        data.append({'id': item.carid, 'brand': item.brand,
                     'model': item.model, 'fuel': item.fuel, 'price': item.price})
    print(data)
    return jsonify(data=data)


@server.route('/getmodels', methods=['GET', 'POST'])
def getmodels():
    # print(request.json)
    data = []
    if request.json['car_search_brand'] == 'Audi':
        data.append({'modelid': '1', 'model': 'A1'})
        data.append({'modelid': '2', 'model': 'A3'})
        data.append({'modelid': '3', 'model': 'A5'})
    if request.json['car_search_brand'] == 'BMW':
        data.append({'modelid': '1', 'model': 'M3'})
        data.append({'modelid': '2', 'model': '320i'})
        data.append({'modelid': '3', 'model': '320d'})
        data.append({'modelid': '4', 'model': '520i'})
        data.append({'modelid': '5', 'model': '520d'})
    if request.json['car_search_brand'] == 'Ferrari':
        data.append({'modelid': '1', 'model': 'Testarossa'})
        data.append({'modelid': '2', 'model': 'Enzo'})
        data.append({'modelid': '3', 'model': 'F50'})
        data.append({'modelid': '4', 'model': 'California'})
    if request.json['car_search_brand'] == 'Ford':
        data.append({'modelid': '1', 'model': 'Focus'})
        data.append({'modelid': '2', 'model': 'Mustang'})
        data.append({'modelid': '3', 'model': 'Fiesta'})
        data.append({'modelid': '4', 'model': 'Escort'})
    if request.json['car_search_brand'] == 'Mercedes':
        data.append({'modelid': '1', 'model': 'C220'})
        data.append({'modelid': '2', 'model': 'SL200'})
        data.append({'modelid': '3', 'model': 'SLK200'})
        data.append({'modelid': '4', 'model': 'A200'})
        data.append({'modelid': '5', 'model': 'CLK200'})
        data.append({'modelid': '6', 'model': 'E300'})
    if request.json['car_search_brand'] == 'Opel':
        data.append({'modelid': '1', 'model': 'Astra'})
        data.append({'modelid': '2', 'model': 'Corsa'})
        data.append({'modelid': '3', 'model': 'Insignia'})
    if request.json['car_search_brand'] == 'Seat':
        data.append({'modelid': '1', 'model': 'Leon'})
        data.append({'modelid': '2', 'model': 'Toledo'})
        data.append({'modelid': '3', 'model': 'Ibiza'})
    if request.json['car_search_brand'] == 'Volkswagen':
        data.append({'modelid': '1', 'model': 'Astra'})
        data.append({'modelid': '2', 'model': 'Corsa'})
        data.append({'modelid': '3', 'model': ''})
    return jsonify(data=data)


@server.route("/listsearchedcars", methods=['GET', 'POST'])
def listsearchedcars():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()
    carslist = []

    if request.json['car_search_brand'] == 'All':
        if request.json['car_search_model'] == 'All':
            if request.json['car_search_fuel'] == 'All':
                if request.json['car_search_price'] == 'All Prices':
                    if request.json['car_search_kmrange'] == 'All':
                        # ALL CARS
                        carslist = dbsession.query(Car).all()
                    else:
                        # CARS IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
                else:
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS BETWEEN PRICES
                        if request.json['car_search_price'] == '0 - 5.000':
                            carslist = dbsession.query(Car).filter(Car.price <= 5000).all()
                        if request.json['car_search_price'] == '5.000 - 10.000':
                            carslist = dbsession.query(Car).filter(Car.price >= 5000).filter(Car.price <= 10000).all()
                        if request.json['car_search_price'] == '10.000 - 15.000':
                            carslist = dbsession.query(Car).filter(Car.price >= 10000).filter(Car.price <= 15000).all()
                        if request.json['car_search_price'] == '15.000 - 20.000':
                            carslist = dbsession.query(Car).filter(Car.price >= 15000).filter(Car.price <= 20000).all()
                        if request.json['car_search_price'] == '20.000 - 25.000':
                            carslist = dbsession.query(Car).filter(Car.price >= 20000).filter(Car.price <= 25000).all()
                        if request.json['car_search_price'] == '25.000 - 30.000':
                            carslist = dbsession.query(Car).filter(Car.price >= 25000).filter(Car.price <= 30000).all()
                        if request.json['car_search_price'] == '>=30.000':
                            carslist = dbsession.query(Car).filter(Car.price >= 30000).all()
                    else:
                        # CARS BETWEEN PRICES AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
            else:
                if request.json['car_search_price'] == 'All Prices':
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS WITH SPECIFIC FUEL
                        carslist = dbsession.query(Car).filter_by(fuel=request.json['car_search_fuel']).all()
                    else:
                        # CARS WITH SPECIFIC FUEL AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
                else:
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS WITH SPECIFIC FUEL AND BETWEEN PRICES
                        if request.json['car_search_price'] == '0 - 5.000':
                            carslist = dbsession.query(Car).filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price <= 5000).all()
                        if request.json['car_search_price'] == '5.000 - 10.000':
                            carslist = dbsession.query(Car).filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 5000).filter(Car.price <= 10000).all()
                        if request.json['car_search_price'] == '10.000 - 15.000':
                            carslist = dbsession.query(Car).filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 10000).filter(Car.price <= 15000).all()
                        if request.json['car_search_price'] == '15.000 - 20.000':
                            carslist = dbsession.query(Car).filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 15000).filter(Car.price <= 20000).all()
                        if request.json['car_search_price'] == '20.000 - 25.000':
                            carslist = dbsession.query(Car).filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 20000).filter(Car.price <= 25000).all()
                        if request.json['car_search_price'] == '25.000 - 30.000':
                            carslist = dbsession.query(Car).filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 25000).filter(Car.price <= 30000).all()
                        if request.json['car_search_price'] == '>=30.000':
                            carslist = dbsession.query(Car).filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 30000).all()
                    else:
                        # CARS WITH SPECIFIC FUEL AND BETWEEN PRICES AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
        else:
            # CARS FROM ALL BRANDS CANNOT HAVE DIFFERENT MODEL
            carslist = dbsession.query(Car).all()
    else:
        if request.json['car_search_model'] == 'All':
            if request.json['car_search_fuel'] == 'All':
                if request.json['car_search_price'] == 'All Prices':
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS FROM SPECIFIC BRAND
                        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand']).all()
                    else:
                        # CARS FROM SPECIFIC BRAND AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
                else:
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS FROM SPECIFIC BRAND AND BETWEEN PRICES
                        if request.json['car_search_price'] == '0 - 5.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.price <= 5000).all()
                        if request.json['car_search_price'] == '5.000 - 10.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.price >= 5000).filter(Car.price <= 10000).all()
                        if request.json['car_search_price'] == '10.000 - 15.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.price >= 10000).filter(Car.price <= 15000).all()
                        if request.json['car_search_price'] == '15.000 - 20.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.price >= 15000).filter(Car.price <= 20000).all()
                        if request.json['car_search_price'] == '20.000 - 25.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.price >= 20000).filter(Car.price <= 25000).all()
                        if request.json['car_search_price'] == '25.000 - 30.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.price >= 25000).filter(Car.price <= 30000).all()
                        if request.json['car_search_price'] == '>=30.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.price >= 30000).all()
                    else:
                        # CARS FROM SPECIFIC BRAND AND BETWEEN PRICES AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
            else:
                if request.json['car_search_price'] == 'All Prices':
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC FUEL
                        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand']) \
                            .filter_by(fuel=request.json['car_search_fuel']).all()
                    else:
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC FUEL AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
                else:
                    if request.json['car_search_kmrange'] == 'All':
                        if request.json['car_search_price'] == '0 - 5.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price <= 5000).all()
                        if request.json['car_search_price'] == '5.000 - 10.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 5000).filter(Car.price <= 10000).all()
                        if request.json['car_search_price'] == '10.000 - 15.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 10000).filter(Car.price <= 15000).all()
                        if request.json['car_search_price'] == '15.000 - 20.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 15000).filter(Car.price <= 20000).all()
                        if request.json['car_search_price'] == '20.000 - 25.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 20000).filter(Car.price <= 25000).all()
                        if request.json['car_search_price'] == '25.000 - 30.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 25000).filter(Car.price <= 30000).all()
                        if request.json['car_search_price'] == '>=30.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 30000).all()
                    else:
                        # CARS FROM SPECIFIC BRAND AND BETWEEN PRICES AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
        else:
            if request.json['car_search_fuel'] == 'All':
                if request.json['car_search_price'] == 'All Prices':
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC MODEL
                        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand']) \
                            .filter_by(model=request.json['car_search_model']).all()
                    else:
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC MODEL AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
                else:
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC MODEL AND BETWEEN PRICES
                        if request.json['car_search_price'] == '0 - 5.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.price <= 5000).all()
                        if request.json['car_search_price'] == '5.000 - 10.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.price >= 5000).filter(Car.price <= 10000).all()
                        if request.json['car_search_price'] == '10.000 - 15.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.price >= 10000).filter(Car.price <= 15000).all()
                        if request.json['car_search_price'] == '15.000 - 20.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.price >= 15000).filter(Car.price <= 20000).all()
                        if request.json['car_search_price'] == '20.000 - 25.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.price >= 20000).filter(Car.price <= 25000).all()
                        if request.json['car_search_price'] == '25.000 - 30.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.price >= 25000).filter(Car.price <= 30000).all()
                        if request.json['car_search_price'] == '>=30.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.price >= 30000).all()
                    else:
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC MODEL AND BETWEEN PRICES AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
            else:
                if request.json['car_search_price'] == 'All Prices':
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC MODEL AND SPECIFIC FUEL
                        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand']) \
                            .filter_by(model=request.json['car_search_model']) \
                            .filter_by(fuel=request.json['car_search_fuel']).all()
                    else:
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC MODEL AND SPECIFIC FUEL AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR
                else:
                    if request.json['car_search_kmrange'] == 'All':
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC MODEL AND SPECIFIC FUEL AND BETWEEN PRICES
                        if request.json['car_search_price'] == '0 - 5.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price <= 5000).all()
                        if request.json['car_search_price'] == '5.000 - 10.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 5000).filter(Car.price <= 10000).all()
                        if request.json['car_search_price'] == '10.000 - 15.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 10000).filter(Car.price <= 15000).all()
                        if request.json['car_search_price'] == '15.000 - 20.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 15000).filter(Car.price <= 20000).all()
                        if request.json['car_search_price'] == '20.000 - 25.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 20000).filter(Car.price <= 25000).all()
                        if request.json['car_search_price'] == '25.000 - 30.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 25000).filter(Car.price <= 30000).all()
                        if request.json['car_search_price'] == '>=30.000':
                            carslist = dbsession.query(Car).filter(Car.brand == request.json['car_search_brand']) \
                                .filter(Car.model == request.json['car_search_model']) \
                                .filter(Car.fuel == request.json['car_search_fuel']) \
                                .filter(Car.price >= 30000).all()
                    else:
                        # CARS FROM SPECIFIC BRAND AND SPECIFIC MODEL AND SPECIFIC FUEL, BETWEEN PRICES AND IN KM RANGE
                        carslist = dbsession.query(Car).all()  # IMPLEMENTAR

    # dist = distance_on_unit_sphere();

    dbsession.close()
    data = []
    for item in carslist:
        asdf = None
        fdsa = None
        car_item = dbsession.query(Dealership).filter(Dealership.mycars.any(Car.carid == item.carid)).all()
        for info_item in car_item:
            asdf = info_item.name
            fdsa = info_item.district
        data.append({'id': item.carid, 'brand': item.brand,
                     'model': item.model, 'fuel': item.fuel,
                     'price': item.price, 'dealership': asdf, 'district': fdsa})
    print(data)
    return jsonify(data=data)


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi / 180.0
    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians
    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians
    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc


@server.route("/addcar", methods=['GET', 'POST'])
def addcar():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('addcar.html')


@server.route("/add_car", methods=['GET', 'POST'])
def add_car():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()

    if request.method == 'POST':
        new_car = Car(brand=request.json['brand'], model=request.json['model'],
                      fuel=request.json['fuel'], price=request.json['price'], owner_id=session['user_id'])
        dbsession.add(new_car)
        dbsession.commit()
        data = {'brand': new_car.brand, 'model': new_car.model, 'fuel': new_car.fuel, 'price': new_car.price}
        dbsession.close()
        return jsonify(data)
    return render_template('addcar.html')


@server.route("/editcar", methods=['GET', 'POST'])
def editcar():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    session['car'] = request.args.get('id', '')
    return render_template('editcar.html')


@server.route("/edit_car", methods=['GET', 'POST'])
def edit_car():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()
    car = dbsession.query(Car).filter_by(carid=session['car']).first()

    if request.method == 'POST':
        car.brand = request.json['brand']
        car.model = request.json['model']
        car.fuel = request.json['fuel']
        car.price = request.json['price']
        car.owner_id = session['user_id']
        dbsession.commit()

        data = {'brand': car.brand, 'model': car.model, 'fuel': car.fuel, 'price': car.price}
        dbsession.close()
        return jsonify(data)

    dbsession.close()
    data = {'brand': car.brand, 'model': car.model, 'fuel': car.fuel, 'price': car.price}
    return jsonify(data)


@server.route("/delete_car", methods=['GET', 'POST'])
def delete_car():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()

    car = dbsession.query(Car).filter_by(carid=request.args.get('id', '')).first()
    dbsession.delete(car)
    dbsession.commit()
    dbsession.close()
    return redirect(url_for('mycars'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@server.route("/image", methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            filename, file_extension = os.path.splitext(filename)
            file.save(os.path.join(os.path.dirname(__file__) + server.config['UPLOAD_FOLDER'],
                                   session['car'] + file_extension))

            s3 = boto3.client('s3',
                              aws_access_key_id='AKIAIOWPTVBJOODWRFGQ',
                              aws_secret_access_key='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')

            s3.upload_file(os.path.join(os.path.dirname(__file__) + server.config['UPLOAD_FOLDER'],
                                   session['car'] + file_extension), 'esimages3bucket', session['car'] + file_extension)

            os.remove(os.path.join(os.path.dirname(__file__) + server.config['UPLOAD_FOLDER'],
                                   session['car'] + file_extension))

            # return redirect(url_for('uploaded_file',
            #                       filename=filename))
            return redirect(url_for('mycars'))
    return redirect(url_for('home'))


@server.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.dirname(__file__) + server.config['UPLOAD_FOLDER'],
                               filename)


@server.route('/listdealershipsbydonthavecar')
def listdealershipsbydonthavecar():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()
    dealslist = dbsession.query(Dealership).filter(~Dealership.mycars.any(Car.carid == session['car'])).all()

    dbsession.close()
    data = []
    for item in dealslist:
        data.append({'id': item.dealershipid, 'name': item.name, 'contact': item.contact, 'district': item.district})
    print(data)
    return jsonify(data=data)


@server.route('/associatecaranddealership', methods=['GET', 'POST'])
def associatecaranddealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        engine = connect_db()
        Base.metadata.bind = engine
        dbsessionbind = sessionmaker(bind=engine)
        dbsession = dbsessionbind()

        car = dbsession.query(Car).filter_by(carid=session['car']).first()
        dealership = dbsession.query(Dealership).filter_by(dealershipid=request.json['selecteddealership']).first()
        car.mydealership.append(dealership)

        dbsession.commit()
        dbsession.close()

    return redirect(url_for('listdealershipsbydonthavecar'))


@server.route('/listdealershipsbyhavingcar')
def listdealershipsbyhavingcar():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()
    dealslist = dbsession.query(Dealership).filter(Dealership.mycars.any(Car.carid == session['car'])).all()

    dbsession.close()
    data = []
    for item in dealslist:
        data.append({'id': item.dealershipid, 'name': item.name, 'contact': item.contact, 'district': item.district})
    print(data)
    return jsonify(data=data)


@server.route('/dissociatecaranddealership', methods=['GET', 'POST'])
def dissociatecaranddealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        engine = connect_db()
        Base.metadata.bind = engine
        dbsessionbind = sessionmaker(bind=engine)
        dbsession = dbsessionbind()

        car = dbsession.query(Car).filter_by(carid=session['car']).first()
        dealership = dbsession.query(Dealership).filter_by(dealershipid=request.json['selecteddealership']).first()
        car.mydealership.remove(dealership)

        dbsession.commit()
        dbsession.close()

    return redirect(url_for('listdealershipsbyhavingcar'))


@server.route("/mydealerships", methods=['GET', 'POST'])
def mydealerships():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('mydealerships.html')


@server.route("/listmydealerships", methods=['GET', 'POST'])
def listmydealerships():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()

    dealslist = dbsession.query(Dealership).filter_by(seller_id=session['user_id']).all()

    dbsession.close()
    data = []
    for item in dealslist:
        data.append({'id': item.dealershipid, 'name': item.name, 'contact': item.contact, 'district': item.district})

    if request.method == 'POST':
        print('Post')
        if request.json['orientation'] == 'ASC':
            data.sort(key=lambda x: x['name'])
        else:
            print('Reverse')
            data.sort(key=lambda x: x['name'], reverse=True)

    print(data[0]['name'])
    if request.method == 'GET':
        data.sort(key=lambda x: x['name'])
    print(data)
    return jsonify(data=data)


@server.route("/mydealershipdetails", methods=['GET', 'POST'])
def mydealershipdetails():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    session['dealership'] = request.args.get('id', '')
    return render_template('mydealershipdetails.html')


@server.route("/listmydealershipdetails", methods=['GET', 'POST'])
def listmydealershipdetails():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()

    carslist = dbsession.query(Car).filter(Car.mydealership.any(Dealership.dealershipid == session['dealership'])).all() #CORRIGIR

    dbsession.close()
    data = []
    for item in carslist:
        data.append({'id': item.carid, 'brand': item.brand,
                     'model': item.model, 'fuel': item.fuel, 'price': item.price})
    print(data)
    return jsonify(data=data)


@server.route("/listmydealershipdetails2", methods=['GET', 'POST'])
def listmydealershipdetails2():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()
    dealershipinfo = dbsession.query(Dealership).filter_by(dealershipid=session['dealership']).first()
    dbsession.close()
    data2 = [{'name': dealershipinfo.name, 'contact': dealershipinfo.contact, 'district': dealershipinfo.district}]
    print(data2)
    return jsonify(data2=data2)


@server.route("/newdealership", methods=['GET', 'POST'])
def newdealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('newdealership.html')


@server.route("/new_dealership", methods=['GET', 'POST'])
def new_dealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()

    if request.method == 'POST':
        new_deal = Dealership(name=request.json['name'], contact=request.json['contact'],
                              district=request.json['district'], seller_id=session['user_id'])
        dbsession.add(new_deal)
        dbsession.commit()
        data = {'name': new_deal.name, 'contact': new_deal.contact, 'district': new_deal.district}
        dbsession.close()
        return jsonify(data)
    return render_template('newdealership.html')


@server.route("/editdealership", methods=['GET', 'POST'])
def editdealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    session['dealership'] = request.args.get('id', '')
    return render_template('editdealership.html')


@server.route("/edit_dealership", methods=['GET', 'POST'])
def edit_dealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()
    dealership = dbsession.query(Dealership).filter_by(dealershipid=session['dealership']).first()

    if request.method == 'POST':
        dealership.name = request.json['name']
        dealership.contact = request.json['contact']
        dealership.district = request.json['district']
        dbsession.commit()
        data = {'name': dealership.name, 'contact': dealership.contact, 'district': dealership.district}
        dbsession.close()
        return jsonify(data)

    dbsession.close()
    data = {'name': dealership.name, 'contact': dealership.contact, 'district': dealership.district}
    return jsonify(data)
    #return render_template('newdealership.html')


@server.route("/dealership", methods=['GET', 'POST'])
def dealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('owner_home.html')


@server.route("/account", methods=['GET', 'POST'])
def account():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('account.html')


@server.route("/editaccount", methods=['GET', 'POST'])
def editaccount():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # print("edit account")
    email = str(session['user_email'])
    # print(email)
    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()
    useraccount = dbsession.query(User).filter_by(email=email).first()
    if request.method == 'POST':
        useraccount.email = request.json['email']
        useraccount.name = request.json['name']
        session['user_name'] = useraccount.name
        print(request.json)
        useraccount.password = request.json['password']
        dbsession.commit()

        data = {'name': useraccount.name, 'email': useraccount.email}
        dbsession.close()
        return jsonify(data)

    dbsession.close()
    data = {'name': useraccount.name, 'email': useraccount.email}
    return jsonify(data)


@server.route("/deleteaccount", methods=['POST'])
def deleteaccount():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # print("delete account")
    email = str(session['user_email'])
    # print(email)
    engine = connect_db()
    Base.metadata.bind = engine
    dbsessionbind = sessionmaker(bind=engine)
    dbsession = dbsessionbind()
    useraccount = dbsession.query(User).filter_by(email=email).first()
    if useraccount.type == "owner":
        usercars = dbsession.query(Car).filter_by(owner_id=useraccount.userid).all()
        userdealerships = dbsession.query(Dealership).filter_by(seller_id=useraccount.userid).all()
        for each_car in usercars:
            dbsession.delete(each_car)
        for each_dealership in userdealerships:
            dbsession.delete(each_dealership)
    dbsession.delete(useraccount)
    dbsession.commit()
    dbsession.close()
    session.pop('logged_in', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    server.secret_key = 'teste'
    server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    server.run(debug=True)
