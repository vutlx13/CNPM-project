import cv2
import numpy as np
import streamlit as st

def detect_face_from_camera(camera_input):
    # Đọc hình ảnh từ camera
    image = cv2.imdecode(np.frombuffer(camera_input.read(), np.uint8), 1)
    
    # Chuyển đổi sang màu RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Nhận diện khuôn mặt
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Vẽ hình chữ nhật quanh khuôn mặt
    for (x, y, w, h) in faces:
        cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return image_rgb
