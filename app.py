from flask import Flask, render_template, request, jsonify, send_file, Response
from loai.upload_part import detect_face_from_upload
from loai.camera_part import detect_face_from_camera
from loai.webcam_part import detect_face_from_webcam
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Trangchu.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    image = detect_face_from_upload(file)
    img_io = io.BytesIO()
    Image.fromarray(image).save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/camera', methods=['POST'])
def camera():
    try:
        file = request.files['camera_image']
        image = detect_face_from_upload(file)  # Tái sử dụng hàm xử lý ảnh upload
        img_io = io.BytesIO()
        Image.fromarray(image).save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/video')
def video():
    return Response(detect_face_from_webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
