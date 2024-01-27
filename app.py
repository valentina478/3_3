import sqlite3
from flask import Flask, render_template, g, request


app = Flask('Pizzeria', template_folder="templates", static_folder="static")

DATABASE = 'db.db'
pizzas = {
    1: "Маргарита",
    2: "Пепероні",
    3: "Чотири сира",
    4: "Гавайська",
    5: "Вегетеріанська",
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_db():
    cr = sqlite3.connect(DATABASE)
    cr.execute('''CREATE TABLE IF NOT EXISTS order_info
            (name VARCHAR(128), order_composition VARCHAR(128), address VARCHAR(128), phone VARCHAR(32))''')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/')
@app.route('/index')
def main_page():
    return render_template("main_page.html")

@app.route('/menu')
def menu():
    return render_template("menu.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

@app.route('/order/', methods=['GET', 'POST'])
def order():
    if request.method == "POST":
        name = request.form.get("name")
        order_composition = request.form.get("order")
        address = request.form.get("address")
        phone = request.form.get("phone")


        cr = get_db()
        cr.execute('INSERT INTO order_info (name, order_composition, address, phone) VALUES (?, ?, ?, ?)', (name, order_composition, address, phone))
        cr.commit()
        return render_template("main_page.html")

    else:
        return render_template("order.html", for_order=pizzas)

@app.route('/db')
def db():
    cr = get_db()
    cr.row_factory = sqlite3.Row
    cr = cr.cursor()
    cr.execute("SELECT * FROM order_info")
    data = cr.fetchall()
    cr.close()
    return render_template("db.html", data=data)

if __name__ == "__main__":
    create_db()
    app.run(debug=True)