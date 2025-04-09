import streamlit as st
from loai.upload_part import detect_face_from_upload
from loai.camera_part import detect_face_from_camera
from loai.webcam_part import detect_face_from_webcam  # bạn sẽ tạo thêm file này

# Tiêu đề ứng dụng
st.title(":white_check_mark:Ứng dụng Nhận diện Khuôn mặt")

# Thêm tùy chọn
option = st.selectbox("Chọn cách nhận diện khuôn mặt:", ["Tải ảnh lên", "Sử dụng camera", "Video trực tiếp (webcam)"])

if option == "Tải ảnh lên":
    uploaded_file = st.file_uploader("Chọn hình ảnh...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_rgb = detect_face_from_upload(uploaded_file)

        cols = st.columns([1, 2, 1])  # Chia giao diện thành 3 cột: trái (1), giữa (2), phải (1)
        with cols[1]:  # Cột ở giữa
            st.image(image_rgb, caption='Khuôn mặt được nhận diện', width=300)

elif option == "Sử dụng camera":
    camera_input = st.camera_input("Chụp ảnh từ camera")
    if camera_input is not None:
        image_rgb = detect_face_from_camera(camera_input)
        st.image(image_rgb, caption='Khuôn mặt được nhận diện từ camera', use_container_width=True)

elif option == "Video trực tiếp (webcam)":
    status = st.empty()  # tạo một placeholder
    if st.button("Bắt đầu webcam"):
        status.info("📹 Đang sử dụng webcam, nhấn Enter để thoát.")
        detect_face_from_webcam()  # chạy luôn code OpenCV
        status.empty()
    