from flask import Flask, render_template, Response, flash
from stream import *

app = Flask(__name__)
app.secret_key = "alpha"


@app.route('/')
def index():
    if isinstance(gen(VideoCamera(), 0), str):
        flash('Looks like you have changed your name!')
    return render_template('index.html')


def gen(camera, var):
    while True:
        if var == 1:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame[1] + b'\r\n\r\n')
        elif var == 0:
            return camera.get_frame()[0]


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera(), 1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
