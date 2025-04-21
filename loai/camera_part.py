import cv2
import numpy as np

def detect_face_from_camera():
    # Mở webcam (0 là chỉ số của webcam mặc định)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise ValueError("Không thể mở camera. Vui lòng kiểm tra lại thiết bị.")

    # Chụp một ảnh từ camera
    ret, frame = cap.read()
    cap.release()  # Đóng kết nối camera

    if not ret:
        raise ValueError("Không thể chụp ảnh từ camera.")

    # Chuyển ảnh sang grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Sử dụng CascadeClassifier để nhận diện khuôn mặt
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Vẽ hình chữ nhật quanh khuôn mặt
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame
