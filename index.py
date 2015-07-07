from flask import Flask, render_template, request, jsonify
import pymysql.cursors

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user_form')
def user_form():
    return render_template('form.html')


@app.route('/get_user', methods=["POST"])
def get_user():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, email from users where " + request.form['id'] + " = id")
    result = cur.fetchone()

    cur.close()
    conn.commit()
    conn.close()
    return result["email"]


@app.route('/register_user', methods=["POST"])
def register_user():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)", (request.form['email'], request.form['password']))
    conn.commit()
    cur.execute("SELECT id FROM users WHERE email = '" + request.form['email'] + "'")
    user = cur.fetchone()
    cur.execute("INSERT INTO `locations` (`user_id`, `position`) VALUES (%s, GeomFromText('POINT(0 0)'))", user['id'])
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(status='success', user_id=user['id'])


@app.route('/post_location', methods=["POST"])
def post_location():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("update `locations` set position = GeomFromText('POINT(" + request.form['lat'] + " " + request.form['lng'] + ")') where user_id=%s", request.form['user_id'])
    conn.commit()
    cur.close()
    conn.close

    #一旦コメントアウト to Shimoyan from Say
    #conn = connect_db()
    #cur = conn.cursor()

    #cur.execute("SELECT * FROM yahhos WHERE pushed_user_id = " + request.form['user_id'])

    # cur.close()
    # conn.commit()
    # conn.close

    return jsonify(status='success')


@app.route('/get_near_location_users', methods=["POST"])
def get_near_location_users():
    conn = connect_db()
    cur = conn.cursor()

    #cur.execute("SELECT `user_id`, `position` FROM `locations` WHERE ST_Intersects(`position`, Buffer(POINT(35, 139), 2))")

    cur.execute("SELECT user_id, X(position) as lat, Y(position) as lng from locations where MBRContains(GeomFromText('LINESTRING(" + request.form['lat'] +" " + request.form['lng'] + ","  +  request.form['lat'] + " " + request.form['lng'] + ")'), position)")
    result = cur.fetchall()
    # print(type(result), type(result[0]))
    # for raw in result:
        # print (raw)
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(locations=result)


@app.route('/yahho_push', methods=["POST"])
def yahho_push():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO yahhos (name, position,pushing_user_id,pushed_user_id) VALUES (%s, GeomFromText('POINT(" + request.form['lat'] + " " + request.form['lng'] + ")')," + request.form['pushing_user_id'] + "," + request.form['pushed_user_id'] + ")", request.form['name'])

    cur.close()
    conn.commit()
    conn.close()
    return "success"


HOST = '133.2.37.129'
# HOST = 'localhost'
USER = 'tabakomi'
PASSWD = 'tabakomitabakomi'
DB = 'tabakomi'
CHARSET = 'utf8'


def connect_db():
    return pymysql.connect(host=HOST,
                           user=USER,
                           passwd=PASSWD,
                           db=DB,
                           charset=CHARSET,
                           cursorclass=pymysql.cursors.DictCursor)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
    # app.run()
