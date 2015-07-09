from flask import Flask, render_template, request, jsonify
import pymysql.cursors

app = Flask(__name__)

RANGE = 0.001


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_user', methods=["POST"])
def get_user():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name from users where " + request.form['user_id'] + " = id")
    r = cur.fetchone()

    cur.close()
    conn.commit()
    conn.close()
    if r is None:
        return jsonify(result='')
    return jsonify(result=dict(id=r['id'], name=r['name'].decode('utf-8')))


@app.route('/register_user', methods=["POST"])
def register_user():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, password) VALUES ('" + request.form['name'] + "', '" + request.form['password'] + "')")
    conn.commit()
    cur.execute("SELECT id FROM users WHERE name = '" + request.form['name'] + "' and password = '" + request.form['password'] + "'")
    user = cur.fetchone()
    cur.execute("INSERT INTO `locations` (`user_id`, `position`) VALUES (%s, GeomFromText('POINT(0 0)'))", user['id'])
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(user_id=user['id'])


@app.route('/post_location', methods=["POST"])
def post_location():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("update `locations` set position = GeomFromText('POINT(" + request.form['lng'] + " " + request.form['lat'] + ")') where user_id=%s", request.form['user_id'])
    conn.commit()
    cur.close()
    conn.close

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * , X(position) AS lng, Y(position) AS lat FROM yahhos WHERE pushed_user_id = " + request.form['user_id'])
    result = cur.fetchone()

    cur.close()
    conn.commit()
    conn.close

    if result is not None:
        return jsonify(result=result)
    else:
        return jsonify(result="")


@app.route('/get_near_location_users', methods=["POST"])
def get_near_location_users():
    conn = connect_db()
    cur = conn.cursor()

    lat1 = str(float(request.form['lat']) + RANGE)
    lng1 = str(float(request.form['lng']) - RANGE)
    lat2 = str(float(request.form['lat']) - RANGE)
    lng2 = str(float(request.form['lng']) + RANGE)
    cur.execute("SELECT user_id, Y(position) as lat, X(position) as lng from locations where user_id != " + request.form['user_id'] + " and MBRContains(GeomFromText('LINESTRING(" + lng1 +" " + lat1 + ","  +  lng2 + " " + lat2 + ")'), position)")
    result = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    print(result)
    return jsonify(locations=result)


@app.route('/push_yahho', methods=["POST"])
def push_yahho():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name from users where " + request.form['pushing_user_id'] + " = id")
    r = cur.fetchone()

    cur.execute("INSERT INTO yahhos (name, position,pushing_user_id,pushed_user_id) VALUES (%s, GeomFromText('POINT(" + request.form['lat'] + " " + request.form['lng'] + ")')," + request.form['pushing_user_id'] + "," + request.form['pushed_user_id'] + ")", r['name'])

    cur.close()
    conn.commit()
    conn.close()
    return jsonify(status='success')


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
