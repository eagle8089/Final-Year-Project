from flask import Flask, render_template, Response
from ai_imports import object_detect, head_pos
import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        return image


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def get_frame(img):
    ret, jpeg = cv2.imencode('.jpg', img)
    return jpeg.tobytes()


def gen(camera):
    while True:
        img = camera.get_frame()
        ret, frame = cv2.imencode('.jpg', img)
        frame = frame.tobytes()
        object_detect(img)
        head_pos(img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)