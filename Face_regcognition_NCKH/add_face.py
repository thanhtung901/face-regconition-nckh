import pickle
import numpy as np
import cv2
import os
import time
import random
from facedetaction import FaceDetector
import face_recognition
# from cvzone.FaceDetectionModule import FaceDetector
id = random.randint(0, 10000000)
id2 = random.randint(0, 20000000)
def create_filename(name):
    time.sleep(3)
    folder = f'./addface/{str(name)}'
    os.mkdir(folder)
    time.sleep(3)
    print("Add file oke")
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

def add_face(name):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    detector = FaceDetector()
    count = 0
    while(True):
        ret, img = cam.read()
        img, bboxs = detector.findFaces(img)
        url_save = ""
        if bboxs:
            x, y, w, h = bboxs[0]['bbox']
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            url_save = f"./addface/{str(name)}/user." + str(id) + str(id2) +'.' + str(count) + ".jpg"
            cv2.imwrite(url_save, img)
            print("adđ oke")
            cv2.imshow('image', img)
        if count >= 1:
            print("successfully")
            TrainLastImage(url_save, name)
            print("train last okee")
            break



