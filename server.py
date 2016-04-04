from flask import Flask, request, render_template, jsonify, abort, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import User, Base, Car, Dealership

server = Flask(__name__)


def connect_db():
    return create_engine('mysql+pymysql://esproject:esproject@localhost:3306/esproject1')


@server.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        engine = connect_db()
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session2 = DBSession()
        userexists = session2.query(User).filter_by(email=request.form['email']).first()
        session2.close()
        if not userexists:
            error = 'User does not exist!'
        else:
            if userexists.email == request.form['email'] and userexists.password == request.form['password']:
                session['logged_in'] = request.form['email']
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
    error = None
    if request.method == 'POST':
        engine = connect_db()
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session2 = DBSession()
        newuser = User(name=request.form['name'], type=request.form['type'], email=request.form['email'], password=request.form['password'])
        session2.add(newuser)
        session2.commit()
        session2.close()
        session['logged_in'] = request.form['email']
        session['name'] = request.form['name']
        session['user_type'] = request.form['type']
        return redirect(url_for('home'))
    return render_template('register.html', error=error)


@server.route("/search", methods=['GET', 'POST'])
def search():
    if session['user_type'] == 'client':
        return render_template('client_search.html')
    else:
        return render_template('owner_search.html')


@server.route("/newdealership", methods=['GET', 'POST'])
def newdealership():
    return render_template('owner_home.html')


@server.route("/mycars", methods=['GET', 'POST'])
def mycars():
    return render_template('owner_home.html')


@server.route("/mydealerships", methods=['GET', 'POST'])
def mydealerships():
    return render_template('owner_home.html')


@server.route("/account", methods=['GET', 'POST'])
def account():
    return render_template('account.html')

@server.route("/editaccount", methods=['GET', 'POST'])
def editaccount():
    print("edit account")
    email = str(session['logged_in'])
    print(email)
    if request.method == 'POST':
        engine = connect_db()
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session2 = DBSession()
        usermodified = session2.query(User).filter_by(email=email).first()
        usermodified.email = request.json['email']
        usermodified.name = request.json['name']
        print(request.json)
        usermodified.password = request.json['password']
        session2.commit()


        data= {'name': usermodified.name, 'email': usermodified.email, 'type': usermodified.type}
        session2.close()
        return jsonify(data)

    engine = connect_db()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session2 = DBSession()
    userexists = session2.query(User).filter_by(email=email).first()
    session2.close()
    data = {'name': userexists.name, 'email': userexists.email, 'type': userexists.type}
    return jsonify(data)


@server.route("/home", methods=['GET'])
def home():
    if session['user_type'] == 'client':
        return render_template('client_home.html')
    else:
        return render_template('owner_home.html')


if __name__ == '__main__':
    server.secret_key = 'teste'
    server.run(debug=True)
