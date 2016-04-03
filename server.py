from flask import Flask, request, render_template, jsonify, abort, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import User, Base, Car, Dealership

server = Flask(__name__)


def connect_db():
    return create_engine('mysql+pymysql://esproject:esproject@localhost:3306/esproject1')


@server.route("/")
def index():
    return render_template('index.html')


@server.route("/login", methods=['GET', 'POST'])
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
            error = 'algo nao esta bem'
        else:
            if userexists.email == request.form['email'] and userexists.password == request.form['password']:
                session['logged_in'] = request.form['email']
                return redirect(url_for('menu'))
            else:
                error = 'login nao correcto'

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
        novo = User(name=request.form['name'], type=request.form['type'], email=request.form['email'], password=request.form['password'])
        session2.add(novo)
        session2.commit()
        session2.close()
        session['logged_in'] = request.form['email']
        return redirect(url_for('menu'))
    return render_template('register.html', error=error)


@server.route("/account", methods=['GET', 'POST'])
def account():
    return render_template('account.html')


@server.route("/editaccount", methods=['GET', 'POST'])
def editaccount():
    print("edit acount")
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

@server.route("/menu", methods=['GET'])
def menu():
    return render_template('menu.html')


if __name__ == '__main__':
    server.secret_key = 'teste'
    server.run(debug=True)
