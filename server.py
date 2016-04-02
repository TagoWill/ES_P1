from flask import Flask, request, render_template, jsonify, abort, redirect, url_for, session

server = Flask(__name__)


@server.route("/")
def index():
    return render_template('index.html')

@server.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #verificar base de dados
        session['logged_in'] = request.form['email']
        return redirect(url_for('menu'))
    return render_template('login.html', error=error)


@server.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@server.route("/register")
def register():
    error = None
    return render_template('login.html', error=error)

@server.route("/menu", methods=['GET'])
def menu():
    return render_template('menu.html')


if __name__ == '__main__':
    server.secret_key = 'teste'
    server.run(debug=True)
