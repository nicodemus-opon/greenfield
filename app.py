from flask import Flask, render_template, redirect, url_for, request, session
import pymysql as mysql
import pymysql
import numstowords
from functools import wraps
import time
from random import randint

app = Flask(__name__)
app.secret_key = "nico"
app.debug = True


@app.template_filter()
def numberFormat(value):
    return format(int(value), ',d')


@app.template_filter()
def words(value):
    return numstowords.huu(value)


def set_db(h, u, p, d):
    session["host"] = h
    session["username"] = u
    session["password"] = p
    session["database"] = d


def connect():
    h = session["host"]
    u = session["username"]
    p = session["password"]
    d = session["database"]
    con = mysql.connect(h, u, p, d, port=3306, cursorclass=pymysql.cursors.DictCursor)
    return con


def del_data(condition=""):
    table = session["table"]
    sql = "DELETE FROM " + table + " where " + condition + " ;"
    con = connect()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()


def create_data(info=[]):
    table = session["table"]
    datax = "'"
    for x in info:
        datax += str(x) + "','"
    datax = datax[:-2]
    sql = "insert into " + table + " values(" + datax + ");"
    print(sql)
    con = connect()
    cur = con.cursor()
    cur.execute(sql)
    con.commit()


def update_data(updates=[], condition=""):
    table = session["table"]
    nico = "update " + table + " set "
    y = 0
    for x in session["cols"]:
        q = str(x) + "= '" + str(updates[y]) + "',"
        nico += q
        y += 1
    nico = nico[:-1]
    nico += " where " + condition + " ;"
    print(nico)
    # return "hj"
    con = connect()
    cur = con.cursor()
    cur.execute(nico)
    con.commit()
    return ("successfully inserted data")


def read_data():
    table = session["table"]
    cond = session["cond"]
    list_of_values = []
    list_of_cols = []
    lit_of_dels = []
    list_of_updates = []
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM " + str(table).lower() + " " + cond)
    with con:
        rows = cur.fetchall()
        try:
            list_of_cols = list(rows[0].keys())
            print(list_of_cols)
        except Exception as e:
            list_of_cols = ["empty", "empty"]
        for row in rows:
            kop = list(row.values())
            list_of_values.append(kop)
            st = "/d/" + kop[0]
            rd = "/invoice/" + kop[0]
            list_of_updates.append(rd)
            lit_of_dels.append(st)
    if list_of_values == []:
        list_of_values = [['UH OH ;)'], ['This table is empty']]
    print(list_of_values)
    session["cols"] = list_of_cols
    session["colsxy"] = len(list_of_cols)
    session["vals"] = list_of_values
    session["valsxy"] = len(list_of_values)
    session["dels"] = lit_of_dels
    session["invoice"] = list_of_updates
    return ([list_of_cols, list_of_values])


@app.route('/dashboard', methods=["GET", "POST"])
def dash():
    return redirect(url_for("index"))


@app.route('/', methods=["GET", "POST"])
def index():
    set_db("localhost", "nico", "Black11060!", "rapha")
    connect()
    session["cond"] = ""
    return render_template('index.html')


@app.route('/transactions', methods=["GET", "POST"])
def reg():
    session["table"] = "transactions"
    session["cond"] = ""
    read_data()
    return render_template('transactions.html')


@app.route('/fees', methods=["GET", "POST"])
def fees():
    return render_template('fees.html')


@app.route('/fee/<string:name>', methods=["GET", "POST"])
def fee(name):
    print(name)
    name.replace("!", ",")
    vals = name.split("..")
    # jj + ".." + from + ".." + cl + ".." + dt + ".." + ex + ".." + pt
    # idx	fromx	classx	datex	particulars	dets	typex	amountx
    idx = str(randint(1000, 9000))
    amt = 0
    ll = vals[0].split(",")
    # ll=["bi-90,jj-10,tt-90"]
    hh=
    neo = [idx, vals[1], vals[2], vals[3], vals[0], vals[4], vals[5], amt]
    print(vals)
    return ('fees.html')


@app.route('/invoice/<string:name>', methods=["GET", "POST"])
def invoice(name):
    session["cond"] = "where idx='" + name + "'"
    session["table"] = "transactions"
    read_data()
    return render_template('invoice.html')


@app.route('/transact', methods=["GET", "POST"])
def inventory():
    if request.method == 'POST':
        print(request.form)
        idx = str(randint(1000, 9000))
        date = request.form["date"]
        desc = request.form["desc"]
        acc = request.form["acc"]
        typex = request.form["type"]
        amount = request.form["amount"]
        status = request.form["status"]
        session["table"] = "transactions"
        # idx	datex	amountx	accountx	descx	type
        inf = [idx, date, amount, acc, desc, typex, status]
        create_data(inf)

    return redirect(url_for("reg"))


if __name__ == '__main__':
    app.run(debug=True)
