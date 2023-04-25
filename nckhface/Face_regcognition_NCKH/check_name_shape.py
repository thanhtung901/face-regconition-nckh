import pickle

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pandas as pd

with open('dataface.dat', 'rb') as f:
    all_face_encodings = pickle.load(f)

# Grab the list of names and the list of encodings
    known_face_names = list(all_face_encodings.keys())
    known_face_encodings = np.array(list(all_face_encodings.values()))
    print(known_face_names)
    print(known_face_encodings.shape)


