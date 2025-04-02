import streamlit as st
from loai.upload_part import detect_face_from_upload
from loai.camera_part import detect_face_from_camera

# Tiêu đề ứng dụng
st.title(":white_check_mark:Ứng dụng Nhận diện Khuôn mặt")

# Tùy chọn để người dùng chọn ảnh tải lên hoặc sử dụng camera
option = st.selectbox("Chọn cách nhận diện khuôn mặt:", ["Tải ảnh lên", "Sử dụng camera"])

if option == "Tải ảnh lên":
    # Tải lên hình ảnh
    uploaded_file = st.file_uploader("Chọn hình ảnh...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Gọi hàm nhận diện khuôn mặt từ ảnh tải lên
        image_rgb = detect_face_from_upload(uploaded_file)

        # Hiển thị hình ảnh với khuôn mặt được nhận diện
        st.image(image_rgb, caption='Khuôn mặt được nhận diện', use_container_width=True)

elif option == "Sử dụng camera":
    # Nhận đầu vào từ camera
    camera_input = st.camera_input("Chụp ảnh từ camera")

    if camera_input is not None:
        # Gọi hàm nhận diện khuôn mặt từ camera
        image_rgb = detect_face_from_camera(camera_input)

        # Hiển thị hình ảnh với khuôn mặt được nhận diện
        st.image(image_rgb, caption='Khuôn mặt được nhận diện từ camera', use_container_width=True)