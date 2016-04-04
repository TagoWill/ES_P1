from flask import Flask, request, render_template, jsonify, abort, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import User, Base, Car, Dealership

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


@server.route("/search", methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if session['user_type'] == 'client':
        return render_template('client_search.html')
    else:
        return render_template('owner_search.html')


@server.route("/newdealership", methods=['GET', 'POST'])
def newdealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('owner_home.html')


@server.route("/dealership", methods=['GET', 'POST'])
def dealership():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('owner_home.html')


@server.route("/mycars", methods=['GET', 'POST'])
def mycars():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('owner_home.html')


@server.route("/mydealerships", methods=['GET', 'POST'])
def mydealerships():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('owner_home.html')


@server.route("/account", methods=['GET', 'POST'])
def account():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('account.html')


@server.route("/search_clients", methods=['GET','POST'])
def searchclients():
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


@server.route("/editaccount", methods=['GET', 'POST'])
def editaccount():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    print("edit account")
    email = str(session['user_email'])
    print(email)
    engine = connect_db()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()
    useraccount = dbsession.query(User).filter_by(email=email).first()
    if request.method == 'POST':
        useraccount.email = request.json['email']
        useraccount.name = request.json['name']
        print(request.json)
        useraccount.password = request.json['password']
        dbsession.commit()

        data = {'name': useraccount.name, 'email': useraccount.email}
        dbsession.close()
        return jsonify(data)

    dbsession.close()
    data = {'name': useraccount.name, 'email': useraccount.email}
    return jsonify(data)


@server.route("/home", methods=['GET'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if session['user_type'] == 'client':
        return render_template('client_home.html')
    else:
        return render_template('owner_home.html')


if __name__ == '__main__':
    server.secret_key = 'teste'
    server.run(debug=True)
