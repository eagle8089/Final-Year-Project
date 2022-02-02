from person_and_phone import *
from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model, detect_marks
from head_track import *
# import pyaudio
import math


def object_detect(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (320, 320))
    img = img.astype(np.float32)
    img = np.expand_dims(img, 0)
    img = img / 255
    boxes, scores, classes, nums = yolo(img)
    count = 0
    for i in range(nums[0]):
        if int(classes[0][i] == 0):
            count += 1
        if int(classes[0][i] == 67):
            print('Mobile Phone detected')
            return 'Mobile Phone detected'
        if count == 0:
            print('No person detected')
            return 'No person detected'
        elif count > 1:
            print('More than one person detected')
            return 'More than one person detected'
    return ''


def head_pos(img):
    face_model = get_face_detector()
    landmark_model = get_landmark_model()
    size = img.shape
    # 3D model points.
    model_points = np.array([
        (0.0, 0.0, 0.0),  # Nose tip
        (0.0, -330.0, -65.0),  # Chin
        (-225.0, 170.0, -135.0),  # Left eye left corner
        (225.0, 170.0, -135.0),  # Right eye right corner
        (-150.0, -150.0, -125.0),  # Left Mouth corner
        (150.0, -150.0, -125.0)  # Right mouth corner
    ])

    # Camera internals
    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )
    faces = find_faces(img, face_model)
    for face in faces:
        marks = detect_marks(img, landmark_model, face)
        # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
        image_points = np.array([
            marks[30],  # Nose tip
            marks[8],  # Chin
            marks[36],  # Left eye left corner
            marks[45],  # Right eye right corner
            marks[48],  # Left Mouth corner
            marks[54]  # Right mouth corner
        ], dtype="double")
        dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                      dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

        (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                         translation_vector, camera_matrix, dist_coeffs)

        for p in image_points:
            p1 = (int(image_points[0][0]), int(image_points[0][1]))
            p2 = (int(nose_end_point2D[0][0][0]),
                  int(nose_end_point2D[0][0][1]))
            x1, x2 = head_pose_points(
                img, rotation_vector, translation_vector, camera_matrix)
            # for (x, y) in marks:
            #     cv2.circle(img, (x, y), 4, (255, 255, 0), -1)
            # cv2.putText(img, str(p1), p1, font, 1, (0, 255, 255), 1)
            try:
                m = (p2[1] - p1[1]) / (p2[0] - p1[0])
                ang1 = int(math.degrees(math.atan(m)))
            except:
                ang1 = 90

            try:
                m = (x2[1] - x1[1]) / (x2[0] - x1[0])
                ang2 = int(math.degrees(math.atan(-1 / m)))
            except:
                ang2 = 90

            if ang1 >= 48:
                print('Head down')
                return 'Head down'
            elif ang1 <= -48:
                print('Head up')
                return 'Head up'

            if ang2 >= 48:
                print('Head right')
                return 'Head right'
            elif ang2 <= -48:
                print('Head left')
                return 'Head left'
            return ''
