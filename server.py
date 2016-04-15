from flask import Flask, request, render_template, jsonify, abort, redirect, url_for, session, send_from_directory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import User, Base, Car, Dealership
import math
import os


UPLOAD_FOLDER = '\statc\image'
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
        DBSession = sessionmaker(bind=engine)
        dbsession = DBSession()
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
        DBSession = sessionmaker(bind=engine)
        dbsession = DBSession()
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
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

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
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

    carslist = dbsession.query(Car).filter_by(owner_id=session['user_id']).all()

    dbsession.close()
    data = []
    for item in carslist:
        data.append({'id': item.carid, 'brand': item.brand,
                     'model': item.model, 'fuel': item.fuel, 'price': item.price})
    print(data)
    return jsonify(data=data)


@server.route("/listsearchedcars", methods=['GET', 'POST'])
def listsearchedcars():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()
    carslist = []

    # ALL CARS
    if request.json['car_search_brand'] == 'All' and request.json['car_search_model'] == 'All' and \
                    request.json['car_search_fuel'] == 'All' and request.json['car_search_price'] == 'All Prices' and \
                    request.json['car_search_kmrange'] == 'All':
        carslist = dbsession.query(Car).all()
    # CARS FROM BRAND X
    elif request.json['car_search_brand'] != 'All' and request.json['car_search_model'] == 'All' and \
                    request.json['car_search_fuel'] == 'All' and request.json['car_search_price'] == 'All Prices' and \
                    request.json['car_search_kmrange'] == 'All':
        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand']).all()
    # CARS FROM BRAND X AND MODEL Y
    elif request.json['car_search_brand'] != 'All' and request.json['car_search_model'] != 'All' and \
                    request.json['car_search_fuel'] == 'All' and request.json['car_search_price'] == 'All Prices' and \
                    request.json['car_search_kmrange'] == 'All':
        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand'])\
                                        .filter_by(model=request.json['car_search_model']).all()
    # CARS FROM FUEL X
    elif request.json['car_search_brand'] == 'All' and request.json['car_search_model'] == 'All' and \
                    request.json['car_search_fuel'] != 'All' and request.json['car_search_price'] == 'All Prices' and \
                    request.json['car_search_kmrange'] == 'All':
        carslist = dbsession.query(Car).filter_by(fuel=request.json['car_search_fuel']).all()
    # CARS FROM PRICES BETWEEN X AND Y
    elif request.json['car_search_brand'] == 'All' and request.json['car_search_model'] == 'All' and \
             request.json['car_search_fuel'] == 'All' and request.json['car_search_price'] != 'All Prices' and \
             request.json['car_search_kmrange'] == 'All':
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
    # CARS IN MY DISTRICT
    elif request.json['car_search_brand'] == 'All' and request.json['car_search_model'] == 'All' and \
             request.json['car_search_fuel'] == 'All' and request.json['car_search_price'] == 'All Prices' and \
             request.json['car_search_kmrange'] != 'All':
        carslist = dbsession.query(Car).filter(Car.mydealership.any(Dealership.district == request.json['car_search_kmrange'])).all()
    # CARS FROM BRAND X AND FUEL Y
    elif request.json['car_search_brand'] != 'All' and request.json['car_search_model'] == 'All' and \
             request.json['car_search_fuel'] != 'All' and request.json['car_search_price'] == 'All Prices' and \
             request.json['car_search_kmrange'] == 'All':
        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand'])\
                                        .filter_by(fuel=request.json['car_search_fuel']).all()
    # CARS FROM BRAND X AND PRICES BETWEEN Y AND Z
    elif request.json['car_search_brand'] != 'All' and request.json['car_search_model'] != 'All' and \
                    request.json['car_search_fuel'] == 'All' and request.json['car_search_price'] != 'All Prices' and \
                    request.json['car_search_kmrange'] == 'All':
        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand'])\
                                        .filter_by(price=request.json['car_search_price']).all()
    # CARS FROM BRAND X AND IN MY DISTRICT
    elif request.json['car_search_brand'] != 'All' and request.json['car_search_model'] == 'All' and \
                    request.json['car_search_fuel'] != 'All' and request.json['car_search_price'] == 'All Prices' and \
                    request.json['car_search_kmrange'] != 'All':
        carslist = dbsession.query(Car).filter_by(brand=request.json['car_search_brand']).\
                                        filter(Car.mydealership.any(Dealership.district == request.json['car_search_kmrange'])).all()


    #dist = distance_on_unit_sphere();


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
    degrees_to_radians = math.pi/180.0
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
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
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

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
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()
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
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

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
            file.save(os.path.join(os.path.dirname(__file__)+server.config['UPLOAD_FOLDER'], session['car'] + file_extension))
            #return redirect(url_for('uploaded_file',
            #                       filename=filename))
            return redirect(url_for('mycars'))
    return redirect(url_for('home'))


@server.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.dirname(__file__)+server.config['UPLOAD_FOLDER'],
                               filename)


@server.route('/listdealershipsbydonthavecar')
def listdealershipsbydonthavecar():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()
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
        DBSession = sessionmaker(bind=engine)
        dbsession = DBSession()

        car = dbsession.query(Car).filter_by(carid=session['car']).first()
        dealership = dbsession.query(Dealership).filter_by(dealershipid=request.json['selecteddealership']).first()
        car.mydealership.append(dealership)

        dbsession.commit()
        dbsession.close()

    return redirect(url_for('listdealershipsbydonthavecar'))


@server.route('/listdealershipsbyhavingcar')
def listdealershipsbyhavingcar():
    print('list')
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    engine = connect_db()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()
    dealslist = dbsession.query(Dealership).filter(Dealership.mycars.any(Car.carid == session['car'])).all()

    dbsession.close()
    data = []
    for item in dealslist:
        data.append({'id': item.dealershipid, 'name': item.name, 'contact': item.contact, 'district': item.district})
    print(data)
    return jsonify(data=data)


@server.route('/desassociatecaranddealership', methods=['GET', 'POST'])
def desassociatecaranddealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        engine = connect_db()
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        dbsession = DBSession()

        car = dbsession.query(Car).filter_by(carid=session['car']).first()
        dealership = dbsession.query(Dealership).filter_by(dealershipid=request.json['selecteddealership']).first()
        car.mydealership.remove(dealership)

        dbsession.commit()
        dbsession.close()

    return redirect(url_for('listdealershipsbydonthavecar'))


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
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

    dealslist = dbsession.query(Dealership).filter_by(seller_id=session['user_id']).all()

    dbsession.close()
    data = []
    for item in dealslist:
        data.append({'id': item.dealershipid, 'name': item.name, 'contact': item.contact, 'district': item.district})
    print(data)
    return jsonify(data=data)


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
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

    if request.method == 'POST':
        new_deal = Dealership(name=request.json['name'], contact=request.json['contact'],
                              district=request.json['district'], location_lat=40.1,
                              location_long=-8.4, seller_id=session['user_id'])
        dbsession.add(new_deal)
        dbsession.commit()
        data = {'name': new_deal.name, 'contact': new_deal.contact, 'district': new_deal.district}
        dbsession.close()
        return jsonify(data)
    return render_template('newdealership.html')


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
    #print("edit account")
    email = str(session['user_email'])
    #print(email)
    engine = connect_db()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()
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
    #print("delete account")
    email = str(session['user_email'])
    #print(email)
    engine = connect_db()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()
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


@server.route('/getmodels', methods=['GET', 'POST'])
def getmodels():

    print(request.json)
    if request.json['car_search_brand'] == 'Audi':
        data = []
        data.append({'modelid': '1', 'model': 'teste1'})
        return jsonify(data=data)
    if request.json['car_search_brand'] == 'BMW':
        data = []
        data.append({'modelid': '2', 'model': 'teste2'})
        return jsonify(data=data)
    else:
        data = []
        return jsonify(data=data)


if __name__ == '__main__':
    server.secret_key = 'teste'
    server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    server.run(debug=True)
