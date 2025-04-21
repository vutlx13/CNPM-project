import cv2
import numpy as np
from io import BytesIO
from PIL import Image

def detect_face_from_upload(file):
    # Đọc ảnh từ file
    img = np.array(file)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # Chuyển ảnh từ BGR sang RGB
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Sử dụng CascadeClassifier để nhận diện khuôn mặt
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Vẽ hình chữ nhật quanh khuôn mặt
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb
