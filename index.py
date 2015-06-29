from flask import Flask, render_template, request
import pymysql.cursors

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user_form')
def user_form():
    return render_template('form.html')

@app.route('/register_user', methods=["POST"])
def register_user():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)", (request.form['email'], request.form['password']))

    cur.close()
    conn.commit()
    conn.close()
    return request.form['email'] + request.form['password']

@app.route('/test_db')
def test_db():
    # Connect to the database
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO `users` (`email`, `password`) VALUES ('test', 'test')")

    cur.close()
    conn.commit()
    conn.close()
    return 'TEST DB!'


def connect_db():
    return pymysql.connect(host='133.2.37.129',
                           user='tabakomi',
                           passwd='tabakomitabakomi',
                           db='tabakomi',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
