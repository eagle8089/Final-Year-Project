from ai_imports import *

# noinspection PyUnresolvedReferences
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


class VideoCamera(object):
    def __init__(self):
        # noinspection PyUnresolvedReferences
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        validate = []
        success, image = self.video.read()
        response = object_detect(image)
        response2 = head_pos(image)
        validate.append(response)

        # noinspection PyUnresolvedReferences
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(img_gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # noinspection PyUnresolvedReferences
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # noinspection PyUnresolvedReferences
        ret, jpeg = cv2.imencode('.jpg', image)
        validate.append(jpeg.tobytes())
        return validate
