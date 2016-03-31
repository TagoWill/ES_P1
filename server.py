from flask import Flask, request, render_template

server = Flask(__name__)


@server.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        value_one = int(request.form['number_one'])
        value_two = int(request.form['number_two'])
        total = value_one + value_two
        return render_template('index.html', value=total)
    return render_template('index.html')


if __name__ == '__main__':
    server.run(debug=True)
