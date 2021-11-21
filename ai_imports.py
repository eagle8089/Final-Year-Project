from person_and_phone import *


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
    return 'None'
