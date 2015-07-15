from flask import Flask, request, jsonify
from freq_word import analyze
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
    cur.execute("SELECT id, name, twitter as screen_name, comment from users where " + request.form['user_id'] + " = id")
    result = cur.fetchone()
    cur.close()
    conn.commit()
    conn.close()

    if result is None:
        return jsonify(result='')
    print(result)
    result['twitetr'] = analyze(result['screen_name'])
    return jsonify(result=result)


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


@app.route('/register_profile', methods=["POST"])
def register_profile():
    conn = connect_db()
    cur = conn.cursor()
    if request.form['twitter'] is not None:
        twitter = request.form['twitter']
    else:
        twitter = ''
    if request.form['comment'] is not None:
        comment = request.form['comment']
    else:
        comment = ''
    cur.execute("UPDATE users SET twitter = %s, comment = %s WHERE id = %s",
                (twitter, comment, request.form['user_id']))
    conn.commit()
    cur.close()
    conn.close
    return jsonify(status='success')


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
    cur.execute("DELETE FROM yahhos WHERE id = %s", (result['id'],))

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
    cur.execute("SELECT name, user_id, Y(position) as lat, X(position) as lng from locations LEFT JOIN users ON locations.user_id = users.id where user_id != " + request.form['user_id'] + " and MBRContains(GeomFromText('LINESTRING(" + lng1 +" " + lat1 + ","  +  lng2 + " " + lat2 + ")'), position)")
    result = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
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


@app.route('/get_tags', methods=["POST"])
def get_tags():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * from user_tags where user_id = %s",
                (request.form['user_id'],))
    result = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    user_tags = []
    for r in result:
        user_tags.append(r['name'])
    return jsonify(tags=TAGS, user_tags=user_tags)


@app.route('/set_tag', methods=["POST"])
def set_tag():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_tags (user_id, name) VALUES (%s, %s)",
                (request.form['user_id'], request.form['name']))
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(status='success')


@app.route('/remove_tag', methods=["POST"])
def remove_tag():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_tags WHERE user_id = %s and name = %s",
                (request.form['user_id'], request.form['name']))
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(status='success')


@app.route('/enter_ibeacon', methods=["POST"])
def enter_ibeacon():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO ibeacons (user_id) VALUES (%s)",
                (request.form['user_id'],))
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(status='success')


@app.route('/exit_ibeacon', methods=["POST"])
def exit_ibeacon():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM ibeacons WHERE user_id = %s",
                (request.form['user_id'],))
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(status='success')


@app.route('/get_ibeacons')
def get_ibeacons():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name from ibeacons LEFT JOIN users ON ibeacons.user_id = users.id")
    result = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return jsonify(result=result)

TAGS = ['スポーツ', 'ゲーム', 'ラーメン', '車', 'バイク', 'タバコ', 'IT',
        'アニメ', 'ルイズ', 'ゼロの使い魔']

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
