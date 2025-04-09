import streamlit as st
from loai.upload_part import detect_face_from_upload
from loai.camera_part import detect_face_from_camera
from loai.webcam_part import detect_face_from_webcam 

# Giao diện !!!!
cols = st.columns([37.5,37.5,25])  
with cols[1]: 
    st.image("https://scontent.fhan3-5.fna.fbcdn.net/v/t1.15752-9/489472228_522632914254632_2326154109128453559_n.png?stp=dst-png_s2048x2048&_nc_cat=108&ccb=1-7&_nc_sid=9f807c&_nc_ohc=aYpNtBcV9DgQ7kNvwFAf2C9&_nc_oc=Adm5NmvGFQnb_NffAIgbhI7_qDN0X7JT6Sspy9FldXH0wLX6c9KmpM4B65j1GeKazP7hs2cRtEyb_jHk0Dy1e5R_&_nc_zt=23&_nc_ht=scontent.fhan3-5.fna&oh=03_Q7cD2AF3m6S43Ed_tjeQ4cUFElWk0CuHuCaZk5arTc6DUt_lFQ&oe=681E1A50", width=125)

st.title(":white_check_mark:Ứng dụng Nhận diện Khuôn mặt")

# ====== Các chức năng ======
cols = st.columns([35,40,25])

with cols[0]:
    nut_upload = st.button("📁 Tải ảnh lên")
with cols[1]:
    nut_camera = st.button("📷 Sử dụng camera")
with cols[2]:
    nut_webcam = st.button("🎥 Video trực tiếp")

if "mode" not in st.session_state:
    st.session_state.mode = None

if nut_upload:
    st.session_state.mode = "ảnh"
if nut_camera:
    st.session_state.mode = "camera"
if nut_webcam:
    st.session_state.mode = "webcam"

#================>Chức Năng nhận diện từ ảnh tải lên<================
if st.session_state.mode == "ảnh":
    uploaded_file = st.file_uploader("Chọn hình ảnh...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_rgb = detect_face_from_upload(uploaded_file)

        cols = st.columns([1, 2, 1])  
        with cols[1]: 
            st.image(image_rgb, caption='Khuôn mặt được nhận diện', width=300)

#================>Chức năng nhận diện từ ảnh chụp<================
if st.session_state.mode == "camera":
    camera_input = st.camera_input("Chụp ảnh từ camera")
    if camera_input is not None:
        image_rgb = detect_face_from_camera(camera_input)
        st.image(image_rgb, caption='Khuôn mặt được nhận diện từ camera', use_container_width = True)

#================>Chức năng nhận diện từ video webcam trực tiếp<================
if st.session_state.mode == "webcam":
    status = st.empty()  
    if st.button("Mở webcam"):
        status.info("📹 Đang sử dụng webcam, nhấn Enter để thoát.")
        detect_face_from_webcam()  
        status.empty()
    
