from flask import Flask, render_template, Response, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
import re
from ai_imports import object_detect, head_pos
import cv2

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="raksha"
)

mycursor = mydb.cursor()


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        return image


app = Flask(__name__)

app.secret_key = 'alpha'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'raksha'

mysql = MySQL(app)

user_data = ""


@app.route('/home.html')
def home():
    if not session['loggedin']:
        return render_template('home.html')
    else:
        return render_template('error.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    global user_data
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            user_data = account['username']
            return render_template('home.html')
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


def get_frame(img):
    ret, jpeg = cv2.imencode('.jpg', img)
    return jpeg.tobytes()


def gen(camera):
    global user_data
    count1 = 0
    count2 = 0
    while True:
        val = ""
        img = camera.get_frame()
        ret, frame = cv2.imencode('.jpg', img)
        frame = frame.tobytes()
        val = object_detect(img)
        if val != "":
            print("count1 : " + str(count1))
            count1 = count1 + 1
            if count1 > 10:
                count1 = 0
                mycursor.execute('INSERT INTO log(`username`, `issue`) VALUES (%s,%s)', (user_data, val))
                mydb.commit()
            val = ""
        val = head_pos(img)
        if val != "":
            print("count2 : " + str(count2))
            count2 = count2 + 1
            if count2 > 10:
                count2 = 0
                mycursor.execute('INSERT INTO log(`username`, `issue`) VALUES (%s,%s)', (user_data, val))
                mydb.commit()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
