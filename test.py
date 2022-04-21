# блок библиотек
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import sqlite3
import datetime
import random
from os import environ
import cgi, cgitb
import http.cookiejar as cookielib
import urllib
import shutil
import os
from os import path


# from PIL import Image


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///article.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db1 = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    number_of_adds = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return '<Article %r>' % self.id


class Adds(db1.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    public_date = db.Column(db.String, default=date.today())
    type = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer(), nullable=False)
    actual = db.Column(db.String(), nullable=False, default='1')
    category = db.Column(db.String(), nullable=False, default='0')

    def __repr__(self):
        return '<Adds %r>' % self.id


def user_id():
    with open('user.txt', 'r') as f:
        a = f.read()
    return int(a)

@app.errorhandler(404)
def e404(error):
    return render_template('404.html'), error.code
#endregion

@app.route('/my_adds')
def my_adds():
    with open('user.txt', 'r') as f:
        a = f.read()
    id = a
    print('id >>>', id)
    model = Article.query.all()
    model1 = Adds.query.all()

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM adds WHERE actual = 1""").fetchall()
    result_costs = cur.execute("""SELECT cost FROM adds WHERE host_id = (?) AND actual = 1""", (id,)).fetchall()
    result_phones = cur.execute("""SELECT phone_number FROM article WHERE id = (?)""", (str(int(id) + 1),)).fetchall()

    true_adds = []
    for i in range(len(result)):
        if str(result[i][1]) == str(id):
            true_adds.append(int(result[i][0]) - 1)

    print('true_adds >>>', true_adds)

    true_dates = []
    for i in range(len(true_adds)):
        true_dates.append(cur.execute("""SELECT public_date FROM adds WHERE id = (?)""",
                                      (true_adds[i] + 1,)).fetchall())
    con.commit()

    print(f"truedates >>> {true_dates}")

    dates = []

    months = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря'
    }

    for i in true_dates:
        if i[0][0] == str(date.today() - datetime.timedelta(days=1)):
            dates.append('Вчера')
        elif i[0][0] == str(date.today()):
            dates.append('Сегодня')
        else:
            dates.append(str(i[0][0].split('-')[2]) + ' ' + str(months[i[0][0].split('-')[1]]))

    dates_to_output = {}
    print("true_dates >>>", true_dates)
    for i in range(len(dates)):
        dates_to_output[int(true_adds[i])] = dates[i]

    phone_number = []
    model2 = Article.query.get(int(id) + 1)
    for i in range(len(result_phones)):
        num = model[model1[i + 1].host_id].phone_number
        phone_number.append(
            str("+" + str(num)[0] + ' ' + str(num)[1:4] + ' ' + str(num)[4:7] + '-' + str(num)[7:9] +
                '-' + str(num)[9:]))

    print('result costs >>>', result_costs)
    costs = {}

    for i in range(len(result_costs)):
        a = str(result_costs[i][0])
        if len(a) == 4:
            b = a[0] + ' ' + a[1:]
        elif len(a) == 5:
            b = a[0:2] + ' ' + a[2:]
        elif len(a) == 6:
            b = a[0:3] + ' ' + a[3:]
        elif len(a) == 7:
            b = a[0] + ' ' + a[1:4] + ' ' + a[4:]
        elif len(a) == 8:
            b = a[0:2] + ' ' + a[2:5] + ' ' + a[5:]
        else:
            b = a
        costs[true_adds[i]] = b


    print('costs >>>', costs)
    print('output >>>', true_adds)
    true_adds[-1] = true_adds[-1]
    return render_template("my_adds.html", adds=model1, art=model, id=id, ids=true_adds, dates=dates_to_output,
                           art1=model2, phone_number=phone_number[0], costs=costs)


@app.route('/add_archive')
def archive():
    with open('user.txt', 'r') as f:
        a = f.read()
    id = a

    model = Article.query.all()
    model1 = Adds.query.all()

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM adds WHERE actual = 0""").fetchall()
    result_costs = cur.execute("""SELECT cost FROM adds WHERE host_id = (?) AND actual = 1""", (id,)).fetchall()
    result_phones = cur.execute("""SELECT phone_number FROM article WHERE id = (?)""", (str(int(id) + 1),)).fetchall()

    true_adds = []
    for i in range(len(result)):
        if str(result[i][1]) == str(id):
            true_adds.append(int(result[i][0]) - 1)

    true_dates = []
    for i in range(len(true_adds)):
        true_dates.append(cur.execute("""SELECT public_date FROM adds WHERE id = (?)""", (true_adds[i],)).fetchall())
    con.commit()
    print(f"truedates >>> {true_dates}")

    months = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря'
    }

    dates = []
    for i in true_dates:
        if i[0][0] == str(date.today() - datetime.timedelta(days=1)):
            dates.append('Вчера')
        elif i[0][0] == str(date.today()):
            dates.append('Сегодня')
        else:
            dates.append(str(i[0][0].split('-')[2]) + ' ' + str(months[i[0][0].split('-')[1]]))

    dates_to_output = {}
    for i in range(len(dates)):
        dates_to_output[int(true_adds[i])] = dates[i]

    print('id >>>', id)
    model2 = Article.query.get(int(id) + 1)
    phone_number = []
    for i in range(len(result_phones)):
        num = (model[model1[i + 1].host_id].phone_number)
        phone_number.append(
            str("+" + str(num)[0] + ' ' + str(num)[1:4] + ' ' + str(num)[4:7] + '-' + str(num)[7:9] + '-' + str(num)[9:]))
    print('result costs >>>', result_costs)
    costs = {}
    for i in range(len(result_costs)):
        a = str(result_costs[i][0])
        if len(a) == 4:
            b = a[0] + ' ' + a[1:]
        elif len(a) == 5:
            b = a[0:2] + ' ' + a[2:]
        elif len(a) == 6:
            b = a[0:3] + ' ' + a[3:]
        elif len(a) == 7:
            b = a[0] + ' ' + a[1:4] + ' ' + a[4:]
        elif len(a) == 8:
            b = a[0:2] + ' ' + a[2:5] + ' ' + a[5:]
        else:
            b = a
        try:
            print(true_adds, i, 'RES')
            print(true_adds[i])
            costs[true_adds[i]] = b
        except Exception as E:
            print('ERROR', E)
    print('costs >>>', costs)

    return render_template("add_archive.html", adds=model1, art=model, id=str(id), ids=true_adds, dates=dates_to_output,
                           art1=model2, phone_number=phone_number[0], costs=costs)


@app.route('/add_public/<int:add_id>')
def add_public(add_id):
    with open('user.txt', 'r') as f:
        a = f.read()
    id = a

    model = Article.query.all()
    model1 = Adds.query.all()

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    cur.execute("""UPDATE adds SET actual = 1 WHERE id = (? )""", (add_id + 1,))
    cur.execute("""UPDATE article SET number_of_adds = number_of_adds + 1 WHERE id = (?)""", (id,))
    con.commit()

    title = model1[add_id].title
    print(f"title: {title}")
    model2 = Article.query.get(int(id) + 1)
    return render_template("public_success.html", id=id, title=title, art1=model2)


def dates():
    with open('user.txt', 'r') as f:
        a = f.read()
    id_user = a

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT id FROM adds""").fetchall()
    result_dates = cur.execute("""SELECT public_date FROM adds""").fetchall()
    con.commit()

    output = []
    for i in range(len(result)):
        output.append(int(str(result[i])[1:].split(',)')[0]) - 1)

    id_user = int(id_user) + 1

    months = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря'
    }

    dates = []
    for i in result_dates:
        if i[0] == str(date.today() - datetime.timedelta(days=1)):
            dates.append('Вчера')
        elif i[0] == str(date.today()):
            dates.append('Сегодня')
        else:
            dates.append(str(i[0].split('-')[2]) + ' ' + str(months[i[0].split('-')[1]]))
    print('dates >>>', dates)
    print('output >>>', output)

    dates_to_output = {}
    for i in range(len(dates)):
        dates_to_output[output[i]] = dates[i]
    print(dates_to_output)

    return dates_to_output


@app.route('/')
def home():
    model = Article.query.all()
    model1 = Adds.query.all()

    with open('user.txt', 'r') as f:
        a = f.read()
    id_user = a
    id = id_user

    # перемешиваю объявления
    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT id FROM adds""").fetchall()
    result_dates = cur.execute("""SELECT public_date FROM adds""").fetchall()
    result_costs = cur.execute("""SELECT cost FROM adds""").fetchall()
    result_phones = cur.execute("""SELECT phone_number FROM article""").fetchall()
    con.commit()

    output = []
    for i in range(len(result)):
        output.append(int(str(result[i])[1:].split(',)')[0]) - 1)
    id_user = int(id_user) + 1
    print("result_costs >>>", result_costs)

    costs = []
    for i in range(len(result_costs)):
        a = str(result_costs[i][0])
        if len(a) == 4:
            b = a[0] + ' ' + a[1:]
        elif len(a) == 5:
            b = a[0:2] + ' ' + a[2:]
        elif len(a) == 6:
            b = a[0:3] + ' ' + a[3:]
        elif len(a) == 7:
            b = a[0] + ' ' + a[1:4] + ' ' + a[4:]
        elif len(a) == 8:
            b = a[0:2] + ' ' + a[2:5] + ' ' + a[5:]
        else:
            b = a
        costs.append(b)

    random.shuffle(output)
    print('OUTPUT >>>', output)

    model2 = Article.query.get(int(id) + 1)

    phone_number = []
    for i in range(len(model1)):
        num = model[model1[i].host_id].phone_number
        phone_number.append(str("+" + str(num)[0] + ' ' + str(num)[1:4] + ' ' + str(num)[4:7] + '-' + str(num)[7:9] + '-' + str(num)[9:]))

    return render_template("home.html", art1=model2, art=model, adds=model1, id=id_user, cards_id=output,
                           dates=dates(), cost=costs, phone_number=phone_number)


@app.route('/add_info')
def add_info():
    with open('user.txt', 'r') as f:
        a = f.read()
    user_id = a

    with open('add_id.txt', 'r') as f:
        add_id = int(f.read())

    model = Article.query.all()
    model1 = Adds.query.all()

    model2 = Article.query.get(int(user_id) + 1)

    print("id user >>>", user_id)
    with open('user.txt', 'r') as f:
        a = f.read()
    user_id = int(a)

    num = model[model1[add_id ].host_id].phone_number
    phone_number = "+" + str(num)[0] + ' ' + str(num)[1:4] + ' ' + str(num)[4:7] + '-' + str(num)[7:9] + '-' + str(num)[9:]
    print('phone_number >>>', phone_number)

    a = str(model1[add_id].cost)
    if len(a) == 4:
        b = a[0] + ' ' + a[1:]
    elif len(a) == 5:
        b = a[0:2] + ' ' + a[2:]
    elif len(a) == 6:
        b = a[0:3] + ' ' + a[3:]
    elif len(a) == 7:
        b = a[0] + ' ' + a[1:4] + ' ' + a[4:]
    elif len(a) == 8:
        b = a[0:2] + ' ' + a[2:5] + ' ' + a[5:]
    else:
        b = a

    categories = {0: 'Не указано',
                  1: 'Транспорт',
                  2: 'Недвижимость',
                  3: 'Личные вещи',
                  4: 'Для дома и дачи',
                  5: 'Электроника',
                  6: 'Хобби и отдых',
                  7: 'Другое'}

    return render_template("add_info.html", art=model, adds=model1, add_id=add_id, id=int(user_id), art1=model2,
                           dates=dates(), name=model[model1[add_id ].host_id].name, phone_number=phone_number,
                           cost=b, category=categories[int(model1[add_id].category)])


@app.route('/add/<int:add_id>')
def add(add_id):
    with open('add_id.txt', 'w') as f:
        f.write(str(add_id))

    return redirect('/add_info')


@app.route('/about')
def about():
    with open('user.txt', 'r') as f:
        a = f.read()
    id = a
    print('id user >>>', id)

    model = Article.query.all()
    model2 = Article.query.get(int(id) + 1)

    return render_template("about.html", art1=model2, art=model, id=id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    with open('user.txt', 'r') as f:
        a = f.read()
    id_user = a

    model = Article.query.all()
    model2 = Article.query.get(int(id_user) + 1)

    return render_template("login_choose.html", art=model, id=id_user, art1=model2)


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        p = request.form.to_dict()
        print('request form >>>', p)
        name, email, ps1, ps2, phone_number = p['Name'], p['email'], p['password1'], p['password2'], p['phone_number']

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        print('result >>>', result)

        if ps1 != ps2:
            print('Error 03')
            return redirect('/reg_error3')

        for i in result:
            if i[1] == name:
                print('Error 04')
                return redirect('/reg_error4')

            elif i[2] == email:
                print('Error 05')
                return redirect('reg_error5')

            elif i[4] == phone_number:
                print("Error 06")
                return redirect('reg_error6')

            elif phone_number == '' or name == '' or email == '' or ps1 == '':
                print("Error 07")
                return redirect('reg_error7')

            elif (str(phone_number)[0] == '+' and len(str(phone_number)) == 12) or (str(phone_number) == '8' and len(str(phone_number)) == 11):
                print("Error 08")
                return redirect('reg_error8')

        art = Article(name=name, email=email, password=ps1, phone_number=phone_number)

        db.session.add(art)
        db.session.commit()

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        for i in result:
            if i[2] == email:
                print('success')
                id = i[0]
            else:
                id = 1

        print(f'id {id} wrote')

        with open('user.txt', 'w') as f:
            f.write(str(int(id) - 1))
        print('go to profile', id)
        return redirect(f'/profile/{id}')

    else:
        model = Article.query.all()
        with open('user.txt', 'r') as f:
            a = f.read()
        id_user = a
        model2 = Article.query.get(int(id_user) + 1)

        return render_template("sign_up.html", art=model, id=id_user, art1=model2)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == "POST":
        p = request.form.to_dict()
        print('request form >>>', p)

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        id = False
        for i in range(len(result)):
            try:
                if result[i].index(p['email']):
                    if result[i][3] == p['password']:
                        print('Успешный вход!')
                        id = i
                        a = True

                    else:
                        print('Неправильный пароль! Попробуйте бла бла бла')
                        print("Error 02")
                        return redirect('/login_error2')

            except:
                print('Error 01')

        if id:
            print(id, 'write')
            with open('user.txt', 'w') as f:
                f.write(str(id))
            print('логин', id)
            return redirect(f'/profile/{id}')

        else:
            return redirect('/login_error1')

    else:

        with open('user.txt', 'r') as f:
            a = f.read()
        id_user = a

        model2 = Article.query.get(int(id_user) + 1)
        return render_template("sign_in.html", id=id_user, art1=model2)


@app.route('/logout')
def logout():
    with open('user.txt', 'w') as f:
        f.write(str('0'))

    return redirect('/')


@app.route('/profile/<int:id>')
def profile(id):
    check_adds_amount(id)

    with open('user.txt', 'r') as f:
        a = f.read()
    id = int(a)
    print('id >>>', id)

    model = Article.query.get(id + 1)
    model2 = Article.query.get(int(id) + 1)

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT id FROM adds WHERE host_id = (?)""", (1,)).fetchall()
    print('result from database >>>', result)
    con.commit()

    for i in range(len(result)):
        result[i] = result[i][0]

    num = model.phone_number
    phone_number = "+" + str(num)[0] + ' ' + str(num)[1:4] + ' ' + str(num)[4:7] + '-' + str(num)[7:9] + '-' +\
                   str(num)[9:]

    return render_template("profile.html", art=model, id=id, art1=model2,
                           phone_number=phone_number, ids=result, dates=dates(), len_phone_number=len(phone_number))


@app.route('/add', methods=['POST', 'GET'])
def add_main():
    with open('user.txt', 'r') as f:
        a = f.read()
    id = int(a)

    model = Article.query.get(id + 1)
    print('request method >>>', request.method)

    if request.method == "POST":
        pass

    else:
        model2 = Article.query.get(int(id) + 1)
        return render_template("Add_main.html", art=model, id=id, art1=model2)


@app.route('/add/sell')
def redir():
    return redirect('/add_sell')


@app.route('/add_sell', methods=['POST', 'GET'])
def add_sell():
    with open('user.txt', 'r') as f:
        a = f.read()
    id = int(a)

    model = Article.query.get(id + 1)
    model2 = Article.query.get(int(id) + 1)

    if request.method == "POST":
        # Загрузка изображения
        try:
            f = request.files['file']

            with open(f'static/img/{f.filename}', 'wb') as file:
                file.write(f.read())
            file = url_for('static', filename=f'img/{user_id}/{f.filename}')
            print('filename >>>', f.filename)
            # ПЕРЕМЕЩЕНИЕ ФАЙЛА В СООТВЕТСТВУЮЩИЙ КАТАЛОГ

            # Определение максимального значения среди объявлений
            # start

            #       start
            os.chdir("static/img")
            images = []
            for root, dirs, files in os.walk(".", topdown=False):
                for name in files:
                    # print(os.path.join(root, name))
                    pass
                for name in dirs:
                    print(os.path.join(root, name))
                    images.append(int(name))
            # РЕЗУЛЬТАТ
            max_add_id = (max(images))
            print(max_add_id)
            # os.chdir("/")
            os.chdir("/Users/uraseregin/PycharmProjects/buy-sell-update 2")
            source_path = f"static/img/{f.filename}"
            path1 = f"static/img/{max_add_id + 1}"

            try:
                os.mkdir(path1)

            except OSError as E:
                print("Создать директорию %s не удалось" % path1, E)

            else:
                print("Успешно создана директория %s " % path1)

            if path.exists(source_path):
                destination_path = f"static/img/{max_add_id + 1}/original.jpg"
                new_location = shutil.move(source_path, destination_path)
                print("{0} перемещается в нужное место, {1}".format(source_path, new_location))

            else:
                print("Неверный путь к файлу.")

        except Exception as E:
            print(E)
            return redirect("/add_error9")

        text = request.form['message']
        p = request.form.to_dict()
        print('request form >>>', p)

        for i in p:
            if p[i] == '':
                print('Error9')
                return redirect("/add_error9")

        # Добавление в бд
        art = Adds(host_id=id, title=p['title'], message=p['message'], address=p['address'], condition=p['condition'],
                   type='Продам', cost=p['cost'], category=p['category_id'])
        db1.session.add(art)
        db1.session.commit()

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        id = str(int(id) + 1)
        cur.execute("""UPDATE article SET number_of_adds = number_of_adds + 1 WHERE id = (?)""", (id,))
        con.commit()

        return render_template("add_success.html", art=model, id=id, art1=model2)
    else:
        file = 'static/img/original.jpg'

        return render_template("add_sell.html", art=model, id=id, art1=model2, file=file)


@app.route('/add_buy', methods=['POST', 'GET'])
def add_buy():
    with open('user.txt', 'r') as f:
        a = f.read()
    id = int(a)

    model = Article.query.get(id + 1)
    model2 = Article.query.get(int(id) + 1)

    if request.method == "POST":
        try:
            # Загрузка изображения
            f = request.files['file']

            with open(f'static/img/{f.filename}', 'wb') as file:
                file.write(f.read())
            file = url_for('static', filename=f'img/{user_id}/{f.filename}')
            print('FILENAME ->>>', f.filename)
            # ПЕРЕМЕЩЕНИЕ ФАЙЛА В СООТВЕТСТВУЮЩИЙ КАТАЛОГ

            # Определение максимального значения среди объявлений
            # start

            #       start
            os.chdir("static/img")
            images = []
            for root, dirs, files in os.walk(".", topdown=False):
                for name in files:
                    # print(os.path.join(root, name))
                    pass
                for name in dirs:
                    print(os.path.join(root, name))
                    images.append(int(name))
            # РЕЗУЛЬТАТ
            max_add_id = (max(images))
            print(max_add_id)
            # os.chdir("/")

            os.chdir("/Users/uraseregin/PycharmProjects/buy-sell-update 2")
            source_path = f"static/img/{f.filename}"
            path1 = f"static/img/{max_add_id + 1}"
            try:
                os.mkdir(path1)

            except OSError as E:
                print("Создать директорию %s не удалось" % path1, E)

            else:
                print("Успешно создана директория %s " % path1)

            if path.exists(source_path):
                destination_path = f"static/img/{max_add_id + 1}/original.jpg"
                new_location = shutil.move(source_path, destination_path)
                print("{0} перемещается в нужное место, {1}".format(source_path, new_location))

            else:
                print("Неверный путь к файлу.")

        except Exception as E:
            print(E)
            return redirect("/add_error9")

        #       end
        # end
        text = request.form['message']
        p = request.form.to_dict()
        print('request form >>>', p)
        for i in p:
            if p[i] == '':
                print('Error9')
                return redirect("/add_error9")
        # Добавление в бд

        art = Adds(host_id=id, title=p['title'], message=p['message'], address=p['address'], condition=p['condition'],
                   type='Куплю', cost=p['cost'], category=p['category_id'])
        db1.session.add(art)
        db1.session.commit()
        print('listdir >>>', os.listdir())

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        id = str(int(id) + 1)
        cur.execute("""UPDATE article SET number_of_adds = number_of_adds + 1 WHERE id = (? )""", (id,))
        con.commit()

        return render_template("add_success.html", art=model, id=id, art1=model2)
    else:
        file = 'static/img/original.jpg'

        return render_template("add_buy.html", art=model, art1=model2, id=int(id), file=file)


@app.route('/add/del/<int:add_id>')
def add_del(add_id):
    print('add_id >>>', add_id)
    add_id = str(int(add_id) + 1)
    with open('user.txt', 'r') as f:
        a = f.read()
    id = str(int(a) + 1)

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    cur.execute("""UPDATE adds SET actual = 0 WHERE id = (? )""", (add_id,))
    cur.execute("""UPDATE article SET number_of_adds = number_of_adds - 1 WHERE id = (?)""", (id,))
    con.commit()

    model = Article.query.all()
    model1 = Adds.query.all()
    add_id = int(int(add_id) - 1)
    model2 = Article.query.get(int(id))

    return render_template("add_del_success.html", art=model, adds=model1, id=id, add_id=add_id, art1=model2)

@app.route('/add/edit/<int:add_id>')
def edit_add(add_id):
    with open('add_id.txt', 'w') as f:
        f.write(str(add_id))

    return redirect('/add_edit')


@app.route('/add_edit_new')
def add_edit():
    if request.method == 'GET':
        with open('add_id.txt', 'r') as f:
            add_id = int(f.read())
        adds = Adds.query.all()

        model = Article.query.all()
        id = (int(model[adds[add_id].host_id].id) - 1)
        model2 = Article.query.get(int(id) + 1)
        file = f'static/img/{add_id}/original.jpg'

        return render_template("add_edit.html", art=model, adds=adds, add_id=add_id, id=id, art1=model2, file=file)
    elif request.method == 'POST':
        with open('add_id.txt', 'r') as f:
            add_id = int(f.read())


@app.route('/add_edit', methods=['POST', 'GET'])
def add_edit_old():
    if request.method == 'GET':
        with open('add_id.txt', 'r') as f:
            add_id = int(f.read())

        adds = Adds.query.all()
        model = Article.query.all()

        id = (int(model[adds[add_id].host_id].id) - 1)
        model2 = Article.query.get(int(id) + 1)
        file = f'static/img/{add_id}/original.jpg'
        cat_id = adds[add_id].category
        print('category id >>>', cat_id)

        return render_template("add_edit.html", art=model, adds=adds, add_id=add_id, id=id, art1=model2, file=file,
                               cat_id=int(cat_id))

    elif request.method == 'POST':
        with open('add_id.txt', 'r') as f:
            add_id = int(f.read())
        p = request.form.to_dict()
        print('request form >>>', p)

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        model = Article.query.all()
        adds = Adds.query.all()

        id = (int(model[adds[add_id].host_id].id) - 1)

        try:
            f = request.files['file']
            print('FILENAME', f.filename)
            with open(f'static/img/{f.filename}', 'wb') as file:
                file.write(f.read())
            file = url_for('static', filename=f'img/{user_id}/{f.filename}')
            os.chdir("/Users/uraseregin/PycharmProjects/buy-sell-update 2")
            source_path = f"static/img/{f.filename}"
            path1 = f"static/img/{add_id}"

            if path.exists(source_path):
                destination_path = f"static/img/{add_id}/original.jpg"
                new_location = shutil.move(source_path, destination_path)
                print("{0} перемещается в нужное место, {1}".format(source_path, new_location))

            else:
                print("Неверный путь к файлу.")

        except Exception as E:
            print(E)

        print('request form >>>', p)
        cur.execute("""UPDATE adds SET title = (? ) WHERE id = (? )""", (str(p['name']), add_id + 1))
        print('SAVE NAME -', str(p['name']))
        cur.execute("""UPDATE adds SET message = (? ) WHERE id = (? )""", (str(p['message']), add_id + 1))
        print('SAVE MESSAGE -', str(p['message']))
        cur.execute("""UPDATE adds SET address = (? ) WHERE id = (? )""", (str(p['address']), add_id + 1))
        cur.execute("""UPDATE adds SET cost = (? ) WHERE id = (? )""", (str(p['cost']), add_id + 1))
        cur.execute("""UPDATE adds SET category = (? ) WHERE id = (? )""", (str(p['category_id']), add_id + 1))
        print('SAVE CATEGORY_ID -', str(p['category_id']))
        print('CONDITION >>>', str(p['condition']))
        if str(p['condition']) != '':
            cur.execute("""UPDATE adds SET condition = (? ) WHERE id = (? )""", (str(p['condition']), add_id + 1))
            print('SAVE CONDITION -', str(p['condition']))
        con.commit()
        model2 = Article.query.get(int(id) + 1)
        return render_template("edit_success.html", title=p[str(p.keys()).split("'")[1]], id=id, art1=model2)


@app.route('/add/del_cancel/<int:add_id>', methods=['POST', 'GET'])
def cancel_delete(add_id):
    with open('user.txt', 'r') as f:
        a = f.read()
    id = str(int(a) + 1)

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    cur.execute("""UPDATE adds SET actual = 1 WHERE id = (? )""", (add_id + 1,))
    cur.execute("""UPDATE article SET number_of_adds = number_of_adds + 1 WHERE id = (?)""", (id,))
    con.commit()

    true_adds = []

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM adds""").fetchall()
    con.commit()

    for i in range(len(result)):
        if str(result[i][1]) == str(id):
            true_adds.append(int(result[i][0]) - 1)
    model2 = Article.query.get(int(id))
    art1 = model2

    return redirect(f'/my_adds/{id}')


@app.route('/search', methods=['POST', 'GET'])
def search():
    p = request.form.to_dict()
    print(f"P - {p}")
    # {'category_id': '5', 'search_input': 'название'}
    model = Article.query.all()
    model1 = Adds.query.all()

    true_adds = []

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM adds""").fetchall()
    con.commit()
    # p = {'category_id': '9'}
    # p = {'search_input': 'ss'}
    months = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря'
    }
    with open('user.txt', 'r') as f:
        a = f.read()
    id = str(int(a) + 1)
    print(result)
    model2 = Article.query.get(int(id))
    # try:

    if p['category_id'] != '0' and p['search_input'] != '':
        print('sort and search were called')

        req_name = list(p["search_input"].lower())
        req_cat = list(p["category_id"].lower())
        req_name1 = p["search_input"]
        req_cat1 = p["category_id"]

        for i in range(len(result)):
            title = list(result[i][2].lower())
            category = list(str(result[i][10]).lower())

            if set(req_name).issubset(title) and set(req_cat).issubset(category):
                print(f"title >>> {title}")
                print(f"request >>> {req_name}")
                true_adds.append(i)
                print(f"id >>> {i}")

        true_dates = []
        print(f"TRUE_ADDS >>> {true_adds}")

        for i in true_adds:
            true_dates.append(cur.execute("""SELECT public_date FROM adds WHERE id = (?)""", (i + 1,)).fetchall())
        con.commit()

        print(f"truedates: {true_dates}")
        output = true_adds
        dates = []

        for i in true_dates:
            if i[0][0] == str(date.today() - datetime.timedelta(days=1)):
                dates.append('Вчера')

            elif i[0][0] == str(date.today()):
                dates.append('Сегодня')

            else:
                dates.append(str(i[0][0].split('-')[2]) + ' ' + str(months[i[0][0].split('-')[1]]))

        dates_to_output = {}
        for i in range(len(dates)):
            dates_to_output[int(true_adds[i])] = dates[i]

        if len(true_adds) == 0:
            flag = False
        else:
            flag = True

        phone_number = []

        for i in range(len(true_adds)):
            num = model[model1[true_adds[i]].host_id].phone_number
            phone_number.append(
                str("+" + str(num)[0] + ' ' + str(num)[1:4] + ' ' + str(num)[4:7] + '-' + str(num)[7:9] + '-' + str(
                    num)[9:]))
        print(phone_number)

        return render_template("add_search.html", adds=model1, art=model, true_adds=true_adds,
                               dates=dates_to_output, flag=flag, art1=model2, id=id,
                               cat_search=req_cat1, name_search=req_name1,
                               phone_number=phone_number)

    elif p['category_id'] == '0':
        req = list(p["search_input"].lower())
        # print(result)
        for i in range(len(result)):
            title = list(result[i][2].lower())
            if set(req).issubset(title):
                print(f"title >>> {title}")
                print(f"request >>> {req}")
                true_adds.append(i)
                print(f"id >>> {i}")

        true_dates = []

        for i in true_adds:
            true_dates.append(cur.execute("""SELECT public_date FROM adds WHERE id = (?)""", (i + 1,)).fetchall())
        con.commit()

        print(f"truedates >>> {true_dates}")
        output = true_adds
        dates = []

        for i in true_dates:
            if i[0][0] == str(date.today() - datetime.timedelta(days=1)):
                dates.append('Вчера')

            elif i[0][0] == str(date.today()):
                dates.append('Сегодня')

            else:
                dates.append(str(i[0][0].split('-')[2]) + ' ' + str(months[i[0][0].split('-')[1]]))

        dates_to_output = {}
        for i in range(len(dates)):
            dates_to_output[int(true_adds[i])] = dates[i]

        if len(true_adds) == 0:
            flag = False

        else:
            flag = True
        print(f"trueadds - {true_adds}")

        phone_number = []
        for i in range(len(true_adds)):
            num = model[model1[true_adds[i]].host_id].phone_number
            phone_number.append(
                str("+" + str(num)[0] + ' ' + str(num)[1:4] + ' ' + str(num)[4:7] + '-' + str(num)[7:9] + '-' + str(
                    num)[9:]))
        print(phone_number)

        return render_template("add_search.html", adds=model1, art=model, true_adds=true_adds, dates=dates_to_output,
                               flag=flag, art1=model2, id=id, phone_number=phone_number)

    elif p['search_input'] == '':
        print('sort was called')

        categories = {
            '0': 'Не выбрано...',
            '1': 'Транспорт',
            '2': 'Недвижимость',
            '3': 'Личные вещи',
            '4': 'Для дома и дачи',
            '5': 'Электроника',
            '6': 'Хобби и отдых',
            '7': 'Другое'
        }
        req = int(p["category_id"])
        print('category >>>', req)

        for i in result:
            if i[10] == req:
                true_adds.append(i[0])

                print(f'    РЕЗУЛЬТАТ ПОИСКА  {i[0]}')
        print(f"ОБЪЯВЛЕНИЯ НА ВЫХОД >>> {true_adds}")

        true_dates = []
        for i in true_adds:
            true_dates.append(cur.execute("""SELECT public_date FROM adds WHERE id = (?)""", (i + 1,)).fetchall())
        con.commit()

        print(f"truedates >>> {true_dates}")
        output = true_adds
        dates = []

        print(f"TRUEDATES >>> {true_dates}")
        true_dates = true_dates[:-1:]
        true_adds = true_adds[:-1:]

        for i in true_dates:

            if i[0][0] == str(date.today() - datetime.timedelta(days=1)):
                dates.append('Вчера')

            elif i[0][0] == str(date.today()):
                dates.append('Сегодня')

            else:
                dates.append(str(i[0][0].split('-')[2]) + ' ' + str(months[i[0][0].split('-')[1]]))

        dates_to_output = {}
        for i in range(len(dates)):
            dates_to_output[int(true_adds[i])] = dates[i]

        if len(true_adds) == 0:
            flag = False

        else:
            flag = True
        print(f"true_dates >>> {true_dates}")

        phone_number = []
        for i in range(len(true_adds)):
            num = model[model1[true_adds[i]].host_id].phone_number
            phone_number.append(
                str("+" + str(num)[0] + ' ' + str(num)[1:4] + ' ' + str(num)[4:7] + '-' + str(num)[7:9] + '-' + str(
                    num)[9:]))
        print('phone_number >>>', phone_number)

        return render_template("add_search.html", adds=model1, art=model, true_adds=true_adds, dates=dates_to_output,
                               flag=flag, art1=model2, id=id, phone_number=phone_number)


# БЛОК ОШИБОК

# ОШИБКИ ЛОГИНА

@app.route('/login_error1', methods=['POST', 'GET'])
def error1():
    if request.method == "POST":
        p = request.form.to_dict()
        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        id = False
        for i in range(len(result)):
            try:
                if result[i].index(p['email']):
                    if result[i][3] == p['password']:
                        print('Успешный вход!')
                        id = i

                    else:
                        print('Неправильный пароль при входе')
                        print("Error 02")
                        return redirect('/login_error2')

            except Exception as E:
                print('Error 01', E)
        if id:
            print(id, 'was wrote')

            with open('user.txt', 'w') as f:
                f.write(str(id))

            return redirect(f'/profile/{id}')
        else:
            return redirect('/login_error1')
    else:
        with open('user.txt', 'r') as f:
            a = f.read()
        id = a

        model2 = Article.query.get(int(id) + 1)
        return render_template('error1.html', id=id, art1=model2)


@app.route('/login_error2', methods=['POST', 'GET'])
def error2():
    if request.method == "POST":
        p = request.form.to_dict()
        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        id = False
        for i in range(len(result)):
            try:
                if result[i].index(p['email']):
                    if result[i][3] == p['password']:
                        print('Успешный вход!')
                        id = i
                    else:
                        print('Неправильный пароль')
                        print("Error 02")
                        return redirect('/login_error2')
            except Exception as E:
                print('Error 02', E)

        if id:
            print(id, 'was wrote')
            with open('user.txt', 'w') as f:
                f.write(str(id))

            return redirect(f'/profile/{id}')
        else:
            return redirect('/login_error1')
    else:
        with open('user.txt', 'r') as f:
            a = f.read()
        id = a

        model2 = Article.query.get(int(id) + 1)
        return render_template('error2.html', id=id, art1=model2)


#    ОШИБКИ РЕГИСТРАЦИИ


@app.route('/reg_error8', methods=['POST', 'GET'])
def error8():
    if request.method == "POST":
        p = request.form.to_dict()

        name, email, ps1, ps2, phone_number = p['Name'], p['email'], p['password1'], p['password2'], p['phone_number']
        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        print('result >>>', result)
        print('request form', p)
        if ps1 != ps2:
            print('Error 03')
            return redirect('/reg_error3')

        for i in range(len(result)):
            if result[i][1] == name:
                print('Error 04')
                return redirect('/reg_error4')

            elif result[i][2] == email:
                print('Error 05')
                return redirect('reg_error5')

            elif result[i][4] == phone_number:
                print("Error 06")
                return redirect('reg_error6')

            elif phone_number == '' or name == '' or email == '' or ps1 == '':
                print("Error 07")
                return redirect('reg_error7')

            elif (str(phone_number)[0] == '+' and len(str(phone_number)) == 12) or (
                    str(phone_number) == '8' and len(str(phone_number)) == 11):
                print("Error 08")
                return redirect('reg_error8')

        art = Article(name=name, email=email, password=ps1, phone_number=phone_number)
        db.session.add(art)
        db.session.commit()

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        for i in result:
            if i[2] == email:
                print('success login')
                print("user's email", email)
                id = i[0]

            else:
                id = 1
                print("user's email", email)

        print(id, 'was wrote')
        with open('user.txt', 'w') as f:
            f.write(str(int(id) - 1))
        print('go to profile >>>', id)

        return redirect(f'/profile/{id}')
    else:
        model = Article.query.all()
        with open('user.txt', 'r') as f:
            a = f.read()
        id_user = a

        model2 = Article.query.get(int(id_user) + 1)
        return render_template("error8.html", art=model, id=id_user, art1=model2)


@app.route('/reg_error7', methods=['POST', 'GET'])
def error7():
    if request.method == "POST":
        p = request.form.to_dict()
        name, email, ps1, ps2, phone_number = p['Name'], p['email'], p['password1'], p['password2'], p['phone_number']
        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        print('request form >>>', p)
        print('result >>>', result)

        if ps1 != ps2:
            print('Error 03')
            return redirect('/reg_error3')

        for i in range(len(result)):
            if result[i][1] == name:
                print('Error 04')
                return redirect('/reg_error4')

            elif result[i][2] == email:
                print('Error 05')
                return redirect('reg_error5')

            elif result[i][4] == phone_number:
                print("Error 06")
                return redirect('reg_error6')

            elif phone_number == '' or name == '' or email == '' or ps1 == '':
                print("Error 07")
                return redirect('reg_error7')

            elif (str(phone_number)[0] == '+' and len(str(phone_number)) == 12) or (
                    str(phone_number) == '8' and len(str(phone_number)) == 11):
                print("Error 08")
                return redirect('reg_error8')

        art = Article(name=name, email=email, password=ps1, phone_number=phone_number)
        db.session.add(art)
        db.session.commit()

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        for i in result:
            if i[2] == email:
                print('success login')
                print("user's email", email)
                id = i[0]
            else:
                id = 1
                print("user's email", email)

        print(id, 'was wrote')
        with open('user.txt', 'w') as f:
            f.write(str(int(id) - 1))
        print('go to profile >>>', id)

        return redirect(f'/profile/{id}')
    else:
        model = Article.query.all()
        with open('user.txt', 'r') as f:
            a = f.read()
        id_user = a

        model2 = Article.query.get(int(id) + 1)
        return render_template("error7.html", art=model, id=id_user, art1=model2)


@app.route('/reg_error6', methods=['POST', 'GET'])
def error6():
    if request.method == "POST":
        p = request.form.to_dict()
        name, email, ps1, ps2, phone_number = p['Name'], p['email'], p['password1'], p['password2'], p['phone_number']
        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        print('request form >>>', p)
        print('result >>>', result)

        if ps1 != ps2:
            print('Error 03')
            return redirect('/reg_error3')

        for i in range(len(result)):
            if result[i][1] == name:
                print('Error 04')
                return redirect('/reg_error4')

            elif result[i][2] == email:
                print('Error 05')
                return redirect('reg_error5')

            elif result[i][4] == phone_number:
                print("Error 06")
                return redirect('reg_error6')

            elif phone_number == '' or name == '' or email == '' or ps1 == '':
                print("Error 07")
                return redirect('reg_error7')

            elif (str(phone_number)[0] == '+' and len(str(phone_number)) == 12) or (
                    str(phone_number) == '8' and len(str(phone_number)) == 11):
                print("Error 08")
                return redirect('reg_error8')

        art = Article(name=name, email=email, password=ps1, phone_number=phone_number)
        db.session.add(art)
        db.session.commit()

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        for i in result:
            if i[2] == email:
                print('success')
                print("user's email", email)
                id = i[0]

            else:
                id = 1
                print("user's email", email)

        print(id, 'was wrote')
        with open('user.txt', 'w') as f:
            f.write(str(int(id) - 1))
        print('go to profile >>>', id)

        return redirect(f'/profile/{id}')
    else:
        model = Article.query.all()
        with open('user.txt', 'r') as f:
            a = f.read()

        id_user = a
        model2 = Article.query.get(int(id) + 1)
        return render_template("error6.html", art=model, id=id_user, art1=model2)


@app.route('/reg_error5', methods=['POST', 'GET'])
def error5():
    if request.method == "POST":
        p = request.form.to_dict()
        name, email, ps1, ps2, phone_number = p['Name'], p['email'], p['password1'], p['password2'], p['phone_number']

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        print('request form >>>', p)
        print('result >>>', result)

        if ps1 != ps2:
            print('Error 03')
            return redirect('/reg_error3')

        for i in range(len(result)):
            if result[i][1] == name:
                print('Error 04')
                return redirect('/reg_error4')

            elif result[i][2] == email:
                print('Error 05')
                return redirect('reg_error5')

            elif result[i][4] == phone_number:
                print("Error 06")
                return redirect('reg_error6')

            elif phone_number == '' or name == '' or email == '' or ps1 == '':
                print("Error 07")
                return redirect('reg_error7')

            elif (str(phone_number)[0] == '+' and len(str(phone_number)) == 12) or (
                    str(phone_number) == '8' and len(str(phone_number)) == 11):
                print("Error 08")
                return redirect('reg_error8')

        art = Article(name=name, email=email, password=ps1, phone_number=phone_number)
        db.session.add(art)
        db.session.commit()

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()
        for i in result:
            if i[2] == email:
                print('success login')
                print("user's email", email)
                id = i[0]

            else:
                id = 1
                print("user's email", email)
        print(id, 'was wrote')

        with open('user.txt', 'w') as f:
            f.write(str(int(id) - 1))
        print('go to profile >>>', id)

        return redirect(f'/profile/{id}')
    else:
        model = Article.query.all()
        with open('user.txt', 'r') as f:
            a = f.read()
        id = a

        model2 = Article.query.get(int(id) + 1)
        return render_template('error5.html', id=id, art=model, art1=model2)


@app.route('/reg_error4', methods=['POST', 'GET'])
def error4():
    if request.method == "POST":
        p = request.form.to_dict()
        name, email, ps1, ps2, phone_number = p['Name'], p['email'], p['password1'], p['password2'], p['phone_number']

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        print('result >>>', result)
        print('request form >>>', p)
        if ps1 != ps2:
            print('Error 03')
            return redirect('/reg_error3')

        for i in range(len(result)):
            if result[i][1] == name:
                print('Error 04')
                return redirect('/reg_error4')

            elif result[i][2] == email:
                print('Error 05')
                return redirect('reg_error5')

            elif result[i][4] == phone_number:
                print("Error 06")
                return redirect('reg_error6')

            elif phone_number == '' or name == '' or email == '' or ps1 == '':
                print("Error 07")
                return redirect('reg_error7')

            elif (str(phone_number)[0] == '+' and len(str(phone_number)) == 12) or (
                    str(phone_number) == '8' and len(str(phone_number)) == 11):
                print("Error 08")
                return redirect('reg_error8')

        art = Article(name=name, email=email, password=ps1, phone_number=phone_number)
        db.session.add(art)
        db.session.commit()

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        for i in result:
            if i[2] == email:
                print('success')
                print(i[2])
                print("user's email", email)

            else:
                id = 1
                print("user's email", email)
        print(id, 'was wrote')

        with open('user.txt', 'w') as f:
            f.write(str(int(id) - 1))
        print('go to profile >>>', id)

        return redirect(f'/profile/{id}')
    else:
        model = Article.query.all()
        with open('user.txt', 'r') as f:
            a = f.read()
        id = a

        model2 = Article.query.get(int(id) + 1)
        return render_template('error4.html', id=id, art=model, art1=model2)


@app.route('/reg_error3', methods=['POST', 'GET'])
def error3():
    if request.method == "POST":
        p = request.form.to_dict()
        name, email, ps1, ps2, phone_number = p['Name'], p['email'], p['password1'], p['password2'], p['phone_number']

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        print('result >>>', result)
        print('request form >>>', p)
        if ps1 != ps2:
            print('Error 03')
            return redirect('/reg_error3')

        for i in range(len(result)):
            if result[i][1] == name:
                print('Error 04')
                return redirect('/reg_error4')

            elif result[i][2] == email:
                print('Error 05')
                return redirect('reg_error5')

            elif result[i][4] == phone_number:
                print("Error 06")
                return redirect('reg_error6')

            elif phone_number == '' or name == '' or email == '' or ps1 == '':
                print("Error 07")
                return redirect('reg_error7')

            elif (str(phone_number)[0] == '+' and len(str(phone_number)) == 12) or (
                    str(phone_number) == '8' and len(str(phone_number)) == 11):
                print("Error 08")
                return redirect('reg_error8')

        art = Article(name=name, email=email, password=ps1, phone_number=phone_number)
        db.session.add(art)
        db.session.commit()

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM article""").fetchall()
        con.commit()

        for i in result:
            if i[2] == email:
                print('success')
                print("user's email", email)
                id = i[0]

            else:
                id = 1
                print("user's email", email)

        print(id, 'was wrote')
        with open('user.txt', 'w') as f:
            f.write(str(int(id) - 1))
        print('go to profile >>>', id)

        return redirect(f'/profile/{id}')
    else:
        model = Article.query.all()
        with open('user.txt', 'r') as f:
            a = f.read()
        id = a

        model2 = Article.query.get(int(id) + 1)
        return render_template('error3.html', id=id, art=model, art1=model2)


#    ОШИБКИ ПРИ СОЗДАНИИ ОБЪЯВЛЕНИЯ


@app.route('/add_error9', methods=['POST', 'GET'])
def error9():
    with open('user.txt', 'r') as f:
        a = f.read()
    id = int(a)
    model = Article.query.get(id + 1)
    model2 = Article.query.get(int(id) + 1)

    if request.method == "POST":
        f = request.files['file']

        print('error 09')
        if f.filename != '':
            try:
                # Загрузка изображения

                print("FILENAME >>>", f.filename)
                with open(f'static/img/{f.filename}', 'wb') as file:
                    file.write(f.read())

                file = url_for('static', filename=f'img/{user_id}/{f.filename}')

                # ПЕРЕМЕЩЕНИЕ ФАЙЛА В СООТВЕТСТВУЮЩИЙ КАТАЛОГ

                # Определение максимального значения среди объявлений

                # start

                os.chdir("static/img")
                images = []

                for root, dirs, files in os.walk(".", topdown=False):
                    for name in files:
                        # print(os.path.join(root, name))
                        pass

                    for name in dirs:
                        print(os.path.join(root, name))
                        images.append(int(name))

                # РЕЗУЛЬТАТ
                max_add_id = (max(images))

                # os.chdir("/")
                os.chdir("/Users/uraseregin/PycharmProjects/buy-sell-update 2")
                source_path = f"static/img/{f.filename}"
                path1 = f"static/img/{max_add_id + 1}"

                try:
                    os.mkdir(path1)

                except OSError as E:
                    print("Создать директорию %s не удалось" % path1, E)

                else:
                    print("Успешно создана директория %s " % path1)

                if path.exists(source_path):
                    destination_path = f"static/img/{max_add_id + 1}/original.jpg"
                    new_location = shutil.move(source_path, destination_path)
                    print("{0} перемещается в нужное место, {1}".format(source_path, new_location))

                else:
                    print("Неверный путь к файлу.")

            except Exception as E:
                print(E)
                return redirect('/add_error9')

        else:
            return redirect('/add_error9')

        #       end
        # end
        text = request.form['message']
        p = request.form.to_dict()
        print('request form >>>', p)
        for i in p:
            if p[i] == '':
                print('Error9')
                return redirect("/add_error9")

        # Добавление в бд

        art = Adds(host_id=id, title=p['title'], message=p['message'], address=p['address'], condition=p['condition'],
                   type='Куплю', cost=p['cost'], category=p['category_id'])
        db1.session.add(art)
        db1.session.commit()

        print('listdir', os.listdir())

        con = sqlite3.connect("article.db")
        cur = con.cursor()
        id = str(int(id) + 1)
        cur.execute("""UPDATE article SET number_of_adds = number_of_adds + 1 WHERE id = (? )""", (id,))
        con.commit()

        return render_template("add_success.html", art=model, id=id, art1=model2)
    else:
        file = 'static/img/original.jpg'

        return render_template("error9.html", art=model, art1=model2, id=int(id), file=file)


@app.route("/my_adds/<int:id>")
def error(id):
    # print(date.today())
    # model = Article.query.all()
    # model1 = Adds.query.all()
    # with open('user.txt', 'r') as f:
    #     a = f.read()
    # id_user = a
    # id = id_user
    # id_user = int(id_user) + 1
    # model2 = Article.query.get(int(id) + 1)
    # return render_template("error_message.html", art1=model2, id=id_user)
    return redirect('/my_adds')


# проверка количества активных объявлений пользователя
def check_adds_amount(id):
    model = Article.query.all()
    model1 = Adds.query.all()

    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM adds WHERE host_id = (? ) AND actual = 1""", (id,)).fetchall()
    cur.execute("""UPDATE article SET number_of_adds = (? ) WHERE id = (? )""", (len(result), id + 1))
    con.commit()


main_directory = '/Users/uraseregin/PycharmProjects/buy-sell-update 2'
random_port = True
if __name__ == '__main__':
    con = sqlite3.connect("article.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM article""").fetchall()
    con.commit()

    for i in range(len(result)):
        check_adds_amount(i)

    with open('main_directory.txt', 'w') as f:
        f.write(main_directory)
    print('Running...')

    if random_port:
        print('Randomport=True')
        port=random.randint(1000, 9999)
    else:
        print("RandomPort=False")
        port=5573

    print('today is', date.today())
    app.run(port=port, host='127.0.0.1')
