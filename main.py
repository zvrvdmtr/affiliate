from flask import Flask, render_template, request
from functions import execute_in_sqlite, return_from_sqlite

DB_NAME = 'users.db'
SQL_WHAT_TABLES = "SELECT name FROM sqlite_master WHERE type='table';"
SQL_CREATE_TABLES = "CREATE TABLE users" \
                    " (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL," \
                    " email TEXT UNIQUE NOT NULL," \
                    " password TEXT NOT NULL);"
SQL_CREATE_TESTER = "INSERT INTO users (email, password) VALUES ( 'tester', 'testerpass' );"

app = Flask(__name__, template_folder='app/templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/check_login_pass', methods=['GET', 'POST'])
def check_login_pass():
    if request.method == 'POST':
        print(dict(request.form))
        return render_template('cabinet.html')
    else:
        return 'method must be POST!'


@app.route('/write_to_database', methods=['GET', 'POST'])
def write_to_database():
    if request.method == 'POST':
        pair_key_value_from_request = dict(request.form)
        email = pair_key_value_from_request['email']
        password = pair_key_value_from_request['password']
        new_query = "SELECT email FROM users WHERE email = '{0}';".format(email)
        print(bool(return_from_sqlite(DB_NAME, new_query)))
        if return_from_sqlite(DB_NAME, new_query):
            return render_template('cabinet.html', email=email, password=password)
        return 'надо писать в таблицу'
    else:
        return 'method must be POST!'


if __name__ == '__main__':
    # TODO проверять не только существование, но и структуру
    if not return_from_sqlite(DB_NAME, SQL_WHAT_TABLES):
        execute_in_sqlite(DB_NAME, SQL_CREATE_TABLES)
        execute_in_sqlite(DB_NAME, SQL_CREATE_TESTER)

    app.run(debug=False)
