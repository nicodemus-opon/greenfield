import csv
from random import randint

import pymysql
import pymysql as mysql
from flask import Flask, render_template, redirect, url_for, request, session

import numstowords

app = Flask(__name__)
app.secret_key = "nico"
app.debug = True


def wrap():
    print("jjj")


def add_di_balance():
    pass


def adder(ll=""):
    # ll = "bi-90,jj-10,tt-90"
    kk = ll.split(",")
    # print(kk)
    op = "-".join(kk)
    # print(op)
    opon = op.split("-")
    # print(opon)
    kkk = []
    for z in opon:
        try:
            int(z)
            kkk.append(z)
        except Exception as e:
            pass

    full = 0
    for x in kkk:
        full += int(x)
    # print(kkk)
    return (full)


def get_text(ll=""):
    # ll = "bi-90,jj-10,tt-90"
    kk = ll.split(",")
    # print(kk)
    op = "-".join(kk)
    # print(op)
    opon = op.split("-")
    # print(opon)
    kkk = []
    for z in opon:
        try:
            int(z)
        except Exception as e:
            kkk.append(z)
    return (kkk)


def get_nums(ll=""):
    # ll = "bi-90,jj-10,tt-90"
    kk = ll.split(",")
    # print(kk)
    op = "-".join(kk)
    # print(op)
    opon = op.split("-")
    # print(opon)
    kkk = []
    for z in opon:
        try:
            int(z)
            kkk.append(z)
        except Exception as e:
            pass
    return (kkk)


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


def com_exec(sql=""):
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
            st = "/d/" + str(kop[0])
            rd = "/invoice/" + str(kop[0])
            list_of_updates.append(rd)
            lit_of_dels.append(st)
    if list_of_values == []:
        list_of_values = [['UH OH ;)'], ['This table is empty']]
    if session["table"] == "fees":
        todo = get_text(list_of_values[0][4])
        pricex = get_nums(list_of_values[0][4])
        lens = len(todo)
        session["todo"] = todo
        print(session["todo"])
        session["pricex"] = pricex
        session["lens"] = lens
        session["fromx"] = list_of_values[0][1].split("/")[0]
        session["admno"] = list_of_values[0][1].split("/")[1]
    print(list_of_values)
    list_of_values.reverse()
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


@app.route('/d/<string:name>', methods=["GET", "POST"])
def delete(name):
    print(name)
    que = "delete from transactions where idx= " + name
    exe(que)
    return redirect(url_for("reg"))


def exe(query):
    con = connect()
    cur = con.cursor()
    cur.execute(query)
    lv = []
    with con:
        rows = cur.fetchall()
        for row in rows:
            kop = list(row.values())
            lv.append(kop)
    # print(lv)
    return (lv)


@app.route('/', methods=["GET", "POST"])
def index():
    # set_db("localhost", "nico", "Black11060!", "rapha")
    set_db("remotemysql.com", "0BkENsbWPp", "pyZ1NN0Rhd", "0BkENsbWPp")
    connect()
    trs = "SELECT COUNT(*) FROM transactions;"  # COUNT(*)
    inse = "SELECT SUM(amountx) FROM transactions WHERE accountx='In';"  # SUM(amountx)
    outse = "SELECT SUM(amountx) FROM transactions WHERE accountx='Out';"
    mpesa = "SELECT SUM(amountx) FROM transactions WHERE type='Mpesa';"
    cash = "SELECT SUM(amountx) FROM transactions WHERE type='Cash';"
    bank = "SELECT SUM(amountx) FROM transactions WHERE type='Bank';"
    notif = "SELECT * FROM notifications;"
    f = t = i = o = 0
    try:
        t = exe(trs)
        t = int(t[0][0])
        ir = exe(inse)
        i = int(ir[0][0])
        out = exe(outse)
        o = int(out[0][0])

    except Exception as e:
        print(t, i, o, f)
        print("shit!", e)
    f = i - o
    session["notif"] = exe(notif)
    session["leno"] = len(session["notif"])
    print("====notif===")
    print(session["notif"])
    print(session["leno"])
    mp = exe(mpesa)[0][0]
    cs = exe(cash)[0][0]
    bn = exe(bank)[0][0]
    if mp == None:
        mp = 0
    if cs == None:
        cs = 0
    if bn == None:
        bn = 0
    session["compp"] = [mp, cs, bn]
    session["valo"] = [f, i, o, t]
    session["cond"] = ""
    return render_template('index.html')


@app.route('/transactions', methods=["GET", "POST"])
def reg():
    extras = "Salary,water,vehicle maintenance,electricity,bank charges,food supplies,fuel expenses,loan repayment,telephone and postage,other"
    session["extras"] = extras.split(",")
    session["lextras"] = len(session["extras"])
    session["table"] = "transactions"
    session["cond"] = ""
    read_data()
    return render_template('transactions.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')


@app.route('/fees', methods=["GET", "POST"])
def fees():
    bb = "select * from grade"
    cc = "select * from students"
    session["grades"] = exe(bb)
    print(session["grades"])
    session["lgrades"] = len(session["grades"])
    session["dents"] = exe(cc)
    session["ldents"] = len(session["dents"])
    return render_template('fees.html')


def update_balance(amount=0, id=""):
    que = "select balancex from students where idx='" + id + "'"
    res = exe(que)
    print("res")
    print(res)
    cbal = int(res[0][0])
    newamt = cbal - amount

    sqq = "update students set`balancex`=" + str(newamt) + " where `idx`='" + id + "'"
    print(sqq)
    com_exec(sqq)


@app.route('/fee/<string:name>', methods=["GET", "POST"])
def fee(name):
    print(name)
    name = name.replace("@", "/")
    name = name.replace("!", ",")
    vals = name.split("..")
    # jj + ".." + from + ".." + cl + ".." + dt + ".." + ex + ".." + pt
    # idx	fromx	classx	datex	particulars	dets	typex	amountx
    idx = str(randint(1000, 9000))
    ll = vals[0]
    amt = str(adder(ll))
    neo = [idx, vals[1], vals[2], vals[3], vals[0], vals[4], vals[5], amt]
    idd = neo[1].split("/")
    dd = idd[1]
    update_balance(int(amt), dd)
    print(vals)
    session["cond"] = ""
    session["table"] = "fees"
    create_data(neo)
    fp = ",".join(get_text(vals[0]))
    desci = "fees for " + fp + " by " + vals[1]
    print(desci)
    other = [idx, vals[3], amt, "In", desci, vals[5], "Fees"]
    session["cond"] = ""
    session["table"] = "transactions"
    create_data(other)
    rdd = "/receipt/" + idx
    return (redirect(rdd))


@app.route('/invoice/<string:name>', methods=["GET", "POST"])
def invoice(name):
    session["cond"] = "where idx='" + name + "'"
    session["table"] = "transactions"
    read_data()
    return render_template('invoice.html')


@app.route('/receipt/<string:name>', methods=["GET", "POST"])
def receipt(name):
    session["cond"] = "where idx='" + name + "'"
    session["table"] = "fees"
    read_data()
    return render_template('receipt.html')


@app.route('/download/<string:name>', methods=["GET", "POST"])
def download(name):
    session["cond"] = ""
    session["table"] = name
    arr = read_data()
    urlx = "static/" + name + ".csv"
    wtr = csv.writer(open(urlx, 'w'), delimiter=',', lineterminator='\n')
    print("arr[0]")
    print(arr[0])
    for x in [arr[0]]:
        newarray = []
        for y in x:
            if y[-1] == "x":
                print("equo")
                y = y[0:-1]
            else:
                print("not equo")
            newarray.append(y)
        wtr.writerows([newarray])
    for x in arr[1]: wtr.writerows([x])

    return redirect(urlx)


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


@app.route('/newstudent', methods=["GET", "POST"])
def newstudent():
    if request.method == 'POST':
        print(request.form)

        name = request.form["name"]
        grade = request.form["grade"]
        balance = request.form["balance"]

        inf = "insert into students (namex,gradex,balancex) values('" + name + "','" + grade + "','" + balance + "')"
        com_exec(inf)

    return redirect(url_for("students"))


@app.route("/calendar")
def cal():
    return render_template('calendar.html')


@app.route("/students")
def students():
    bb = "select * from grade"
    session["grades"] = exe(bb)
    print(session["grades"])
    session["lgrades"] = len(session["grades"])
    session["table"] = "students"
    session["cond"] = ""
    read_data()
    return render_template('students.html')


@app.route("/setfees")
def setfee():
    session["feex"] = exe("select * from termfees")[0]
    return render_template('setfee.html')


def setbal(idx, amt, grade, list_amts):
    newamt = 0
    amt = int(amt)
    if grade == "playgroup1":
        newamt = amt + int(list_amts[1])
    elif grade == "pp1":
        newamt = amt + int(list_amts[2])
    elif grade == "pp2":
        newamt = amt + int(list_amts[3])
    elif grade == "grade1":
        newamt = amt + int(list_amts[4])
    elif grade == "grade2":
        newamt = amt + int(list_amts[5])
    elif grade == "grade3":
        newamt = amt + int(list_amts[6])
    elif grade == "grade4":
        newamt = amt + int(list_amts[7])
    elif grade == "grade5":
        newamt = amt + int(list_amts[8])
    elif grade == "grade6":
        newamt = amt + int(list_amts[9])
    elif grade == "grade7":
        newamt = amt + int(list_amts[10])
    elif grade == "grade8":
        newamt = amt + int(list_amts[11])

    sqq = "update students set`balancex`=" + str(newamt) + " where `idx`='" + str(idx) + "'"
    print(sqq)
    com_exec(sqq)


@app.route("/promote")
def promote():
    grades = ['playgroup', 'pp1', 'pp2', 'grade1', 'grade2', 'grade3', 'grade4', 'grade5', 'grade6', 'grade7', 'grade8']
    c = 0
    zx=exe("select idx from students")
    beg=""
    for x in grades:
        y = c + 1
        try:
            sqq = "update students set`gradex`='" + grades[y] + "' where gradex='" + grades[c] + "'"
            print(sqq)
        except Exception as e:
            print(e)
            sqq = "update students set`gradex`='Finished' where gradex='" + grades[c] + "'"
            com_exec(sqq)
            break
        com_exec(sqq)
        c += 1
    return redirect(url_for("students"))


@app.route('/sf/<string:name>', methods=["GET", "POST"])
def sf(name):
    gh = name.split("-")
    print("-------")
    print(gh)
    sql = "truncate termfees"
    com_exec(sql)
    session["table"] = "termfees"
    create_data(gh)
    sq = "select * from students"
    res = exe(sq)
    for x in res:
        setbal(x[0], x[3], x[2], gh)

    session["fees"] = []
    return redirect(url_for("setfee"))


if __name__ == '__main__':
    app.run(debug=True)
