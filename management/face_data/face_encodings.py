import face_recognition
import cv2
import numpy as np

# Load a sample picture and learn how to recognize it.
CUONG_image = face_recognition.load_image_file("/home/cuong/Project2/image/2023-05-23-150038.jpg")
CUONG_face_encoding = face_recognition.face_encodings(CUONG_image)[0]

# Load a second sample picture and learn how to recognize it.
DONG_image = face_recognition.load_image_file("/home/cuong/Project2/image/2023-05-23-150053.jpg")
DONG_face_encoding = face_recognition.face_encodings(DONG_image)[0]

DCuong_image = face_recognition.load_image_file("/home/cuong/Project2/image/2023-05-23-162119.jpg")
DCuong_face_encoding = face_recognition.face_encodings(DCuong_image)[0]

Nguyet_image = face_recognition.load_image_file("/home/cuong/Project2.1/image_data/2023-05-26-094354.jpg")
Nguyet_face_encoding = face_recognition.face_encodings(Nguyet_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    
    CUONG_face_encoding,
    DONG_face_encoding,
    DCuong_face_encoding,
    Nguyet_face_encoding,
]
known_face_names = [
    "NGUYEN DUY CUONG 20195845",
    "TRAN PHUONG DONG 20194954",
    "NGUYEN DUY CUONG 20191714",
    "NGUYEN THI NGUYET 20193043",
]

# Save known face encodings and names as Numpy arrays
np.save("known_face_encodings.npy", known_face_encodings)
np.save("known_face_names.npy", known_face_names)

