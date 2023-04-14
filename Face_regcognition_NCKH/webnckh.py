# importing Flask and other modules
import face_recognition
import numpy as np
from flask import Flask, request, render_template, flash, url_for, redirect, Response
import time
import cv2
import pickle
import random
import os
ids = random.randint(0, 10000000)
# Flask constructor



from facedetaction import FaceDetector

app = Flask(__name__, template_folder='./templates')
with open('dataface.dat', 'rb') as f:
    all_face_encodings = pickle.load(f)
known_face_names = list(all_face_encodings.keys())
known_face_encodings = np.array(list(all_face_encodings.values()))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
time.sleep(1)

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

# faceregistration

name = ''
frame = 0
ret = 0

mssv = ''
pass1 = ''
pass2 = ''
def cam_predict(frame):
    global name
    while True:
        imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(known_face_encodings, encodeFace, tolerance=0.43)
            name = "unknown"
            faceDis = face_recognition.face_distance(known_face_encodings, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = known_face_names[matchIndex]
                print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 ), (x2, y2), (0, 255, 0), cv2.FILLED)
            # cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        return frame

signup = 0
error = []
def createNewface(pass1, pass2, mssv, frame):
    global signup, error
    if pass1 != pass2:
        error.append('Mật khẩu không khớp')
    else:
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
                url_save = f"./addface/{str(mssv)}/user." + str(ids) + '.' + str(count) + ".jpg"
                cv2.imwrite(url_save, img)
                print("adđ oke")
            if count >= 1:
                print("successfully")
                TrainLastImage(url_save, mssv)
                print("train last okee")
                signup = 1
                break
        return frame


@app.route('/faceregistration', methods=['POST'])
def faceregistration():

    global mssv, pass1, pass2, signup, frame, error
    if request.method == 'POST':
        if request.form['btdangky']== 'SIGN UP':
            mssv = request.form.get('mssv')
            pass1 = request.form.get('pass1')
            pass2 = request.form.get('pass2')
            _ = createNewface(pass1, pass2, mssv, frame)
            print("face createNewface")
            if signup == 1:
                print("render login")
                return render_template('Dangnhap.html')
            else:
                print("render false")
                flash('Mat khau khong khop')
                return render_template('Dangky.html', error=error)

@app.route('/signup')
def signup():
    return render_template('Dangky.html')


@app.route('/login', methods=['POST'])
def button():
    global name
    if request.method == "POST":
        if request.form['btlogin'] == 'LOGIN':
            print("Please login")
            username = request.form['username']
            password = request.form['password']
            print('oke')
            if username == name:
                return render_template('home.html')
            else:
                return render_template('Dangnhap.html')
        else:
            print('bt chua duoc nhan')
            return render_template('Dangnhap.html')
    else:
        print('chua nhan duoc POST')
        return render_template('Dangnhap.html')


@app.route('/')
def home():
    return render_template('Dangnhap.html')

def generate_frames():
    global frame, ret
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cam_predict(frame)
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass



@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_signup')
def video_signup():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.debug = True
    app.run()