
import pickle
import face_recognition
import numpy as np
import time
import os
from facedetaction import FaceDetector

import cv2
def TrainLastImage(url,name):

    with open('dataface.dat', 'rb') as f:
        all_face_encodings = pickle.load(f)
    known_face_names = list(all_face_encodings.keys())
    known_face_encodings = np.array(list(all_face_encodings.values()))
    image = face_recognition.load_image_file(url)
    known_face_encodings2=dict(zip(known_face_names, known_face_encodings))
    known_face_encodings2[name]=face_recognition.face_encodings(image)[0]
    with open('dataface.dat', 'wb') as f:
        pickle.dump(known_face_encodings2, f)


def create_filename(name):
    time.sleep(3)
    folder = f'./addface/{str(name)}'
    os.mkdir(folder)
    time.sleep(2)
    print("create file oke")


name = input('nhap name')
cap = cv2.VideoCapture(0)
_ ,frame = cap.read()
def createNewface(mssv, frame):
    check = 0
    if mssv:
        time.sleep(2)
        create_filename(mssv)
        detector = FaceDetector()
        count = 0
        while (True):
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img, bboxs = detector.findFaces(imgRGB)
            url_save = ""
            if bboxs:
                count += 1
                url_save = f"./addface/{str(mssv)}/user." + ".jpg"
                cv2.imwrite(url_save, img)
                print("adđ oke")
            if count >= 1:
                print("successfully")
                TrainLastImage(url_save, mssv)
                print("train last okee")
                check = 1
                break
        return check
    return check

a = createNewface(name, frame)
print(a)