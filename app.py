from flask import Flask, render_template

app = Flask(__name__)


# app.debug(True)

@app.route('/', methods=["GET", "POSTT"])
def index():
    return render_template('index.html')


@app.route('/registration', methods=["GET", "POSTT"])
def reg():
    return render_template('registration.html')


@app.route('/fees', methods=["GET", "POSTT"])
def fees():
    return render_template('blank.html')


@app.route('/exams', methods=["GET", "POSTT"])
def exams():
    return render_template('exams.html')


@app.route('/inventory', methods=["GET", "POSTT"])
def inventory():
    return render_template('inventory.html')


if __name__ == '__main__':
    app.run(debug=True)
