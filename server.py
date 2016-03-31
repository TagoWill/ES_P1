from flask import Flask, request, render_template, jsonify, abort

server = Flask(__name__)


@server.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # if not request.json or not 'title' in request.json:
        #    abort(400)
        data = {'email': request.json['email']}
        return jsonify(data)
    return render_template('index.html')


@server.route("/menu", methods=['GET'])
def menu():
    return render_template('menu.html')


if __name__ == '__main__':
    server.run(debug=True)
