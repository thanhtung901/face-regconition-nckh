import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pickle
def Predict():
    with open('dataface.dat', 'rb') as f:
        all_face_encodings = pickle.load(f)

    known_face_names = list(all_face_encodings.keys())
    known_face_encodings = np.array(list(all_face_encodings.values()))

    cap = cv2.VideoCapture(0)
    name = ""
    while True:
        success, img = cap.read()
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(known_face_encodings, encodeFace,tolerance=0.43)
            name = "unknown"
            faceDis = face_recognition.face_distance(known_face_encodings, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = known_face_names[matchIndex].upper()
                # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if __name__ == '__main__':
    Predict()