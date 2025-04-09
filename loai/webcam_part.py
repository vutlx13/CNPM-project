import cv2

def detect_face_from_webcam():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Không mở được webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không đọc được frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Live Webcam - nhan dien khuon mat', frame)

        if cv2.waitKey(1) & 0xFF == 13:
            break
# Nếu người dùng đóng cửa sổ (ấn dấu X), frame sẽ bị mất
        if cv2.getWindowProperty('Live Webcam - nhan dien khuon mat', cv2.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    cv2.destroyAllWindows()
