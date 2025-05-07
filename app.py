from flask import g, Flask, render_template, session, request, jsonify, send_file, Response, url_for
from loai.upload_part import detect_face_from_upload
from loai.camera_part import detect_face_from_camera
from loai.webcam_part import detect_face_from_webcam
from PIL import Image
import io
import sqlite3
import requests
import random
import string
import os
from werkzeug.utils import secure_filename
from datetime import datetime  
from base64 import b64encode
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key' #định dạng người dùng

UPLOAD_FOLDER = 'static/uploads'  # Thư mục lưu ảnh
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Hàm kiểm tra định dạng ảnh hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Hàm kiểm tra sự tồn tại của ảnh
def is_image_exists(filename):
    return os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# quyền truy cập các trang giao diện
@app.route('/')
def index():
    if 'user_id' not in session:
        # Tạo user_id dạng guest1234
        random_id = ''.join(random.choices(string.digits, k=4))
        session['user_id'] = f"guest{random_id}"
    print(f"Người dùng hiện tại: {session['user_id']}")
    return render_template('Trangchu.html', user_id=session['user_id'])

@app.route('/Thu_vientt')
def Thu_vientt():
    return render_template('chuc_nang/Thu_vien.html', user_id=session['user_id'])

@app.route('/Lich_sutt')
def Lich_sutt():
    return render_template('chuc_nang/Lich_su.html', user_id=session['user_id'])

@app.route('/Upload_anhtt')
def Upload_anhtt():
    return render_template('chuc_nang/Upload_anh.html', user_id=session['user_id'])

@app.route('/Cameratt')
def Cameratt():
    return render_template('chuc_nang/Camera.html', user_id=session['user_id'])

@app.route('/Webcamtt')
def Webcamtt():
    return render_template('chuc_nang/Webcam.html', user_id=session['user_id'])

# nối tới các backend chức năng
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    username = session.get('user_id', 'unknown')

    # xử lý ảnh
    img = Image.open(file).convert('RGB')
    image = detect_face_from_upload(img)

    # Tạo tên file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{username}_{timestamp}.png"

    # trả ảnh về
    img_io = io.BytesIO()
    Image.fromarray(image).save(img_io, 'PNG')
    img_io.seek(0)
    base64_img = b64encode(img_io.getvalue()).decode('utf-8')

    return jsonify({
    'filename': filename,
    'image': f"data:image/png;base64,{base64_img}"
})

@app.route('/camera', methods=['POST'])
def camera():
    try:
        file = request.files['camera_image']
        is_public = 1 if 'public' in request.form else 0
        username = session.get('user_id', 'unknown')

        # xử lý ảnh
        img = Image.open(file).convert('RGB')
        image = detect_face_from_camera(img)

        # Tạo tên file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{username}_{timestamp}.png"

        # lưu vào database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO history_images (filename, is_public, username)
            VALUES (?, ?, ?)
        ''', (filename, is_public, username))
        conn.commit()
        conn.close()

        # trả ảnh về
        img_io = io.BytesIO()
        Image.fromarray(image).save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/video')
def video():
    return Response(detect_face_from_webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Lấy ảnh từ thư viện
@app.route('/get_library_images', methods=['GET'])
def get_library_images():
    
    images = fetch_library_images()  
    image_urls = [{"name": name, "url": url} for name, url in images]  
    return jsonify(image_urls)

@app.route('/library_select', methods=['POST'])
def library_select():
    data = request.get_json()
    image_url = data.get('image_url')

    if not image_url:
        return jsonify({'error': 'Thiếu URL ảnh'}), 400

    try:
        # Đọc ảnh từ URL
        response = requests.get(image_url)
        img = Image.open(io.BytesIO(response.content)).convert('RGB')

        # Xử lý khuôn mặt
        processed_image = detect_face_from_upload(img)

        # Tạo tên file
        username = session.get('user_id', 'unknown')
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{username}_{timestamp}.png"

        # Trả ảnh dạng base64
        img_io = io.BytesIO()
        Image.fromarray(processed_image).save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
        img_data_uri = f"data:image/png;base64,{img_base64}"

        return jsonify({
            'image': img_data_uri,
            'filename': filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


 # Cơ sở dữ liệu!!!!
            # Thư viện
def add_to_library(name, url): # Cho ảnh vào thư viện
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO library_images (name, url) VALUES (?, ?)", (name, url))
    conn.commit()
    conn.close() 
def fetch_library_images():      # Xem những ảnh chứa trong thư viện
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, url FROM library_images")
    images = cursor.fetchall()  
    conn.close()
    return images
def delete_from_library(name): # Xoá ảnh khỏi thư viện
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM library_images WHERE name = ?", (name,))
    conn.commit()
    conn.close()

        # Lịch sử
@app.route('/public_image', methods=['POST'])
def public_image():
    data = request.get_json()
    filename = data.get('filename')
    username = session.get('user_id', 'unknown')

    if not filename or not allowed_file(filename):
        return jsonify({'error': 'Ảnh không hợp lệ'}), 400

    created_at = datetime.now().isoformat()

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO history_images (filename, is_public, username, created_at)
            VALUES (?, ?, ?, ?)
        ''', (filename, 1, username, created_at))

        # Giới hạn 30 bản ghi
        cursor.execute("SELECT COUNT(*) FROM history_images")
        count = cursor.fetchone()[0]

        if count > 30:
            cursor.execute('''
                DELETE FROM history_images
                WHERE created_at = (
                    SELECT created_at FROM history_images
                    ORDER BY created_at ASC
                    LIMIT 1
                )
            ''')

        conn.commit()
        return jsonify({'message': 'Đã công khai ảnh thành công'})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Lỗi khi lưu vào database: {str(e)}'}), 500

    finally:
        conn.close()

#liệt kê trong trang lịch sử
@app.route('/get_history_images', methods=['GET'])
def get_history_images():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Lấy tất cả ảnh từ history_images
    cursor.execute("SELECT filename, username, created_at FROM history_images ORDER BY created_at DESC")
    rows = cursor.fetchall()

    # Chỉ trả về thông tin cần thiết (không cần image_url)
    images = [{'filename': row[0],
               'username': row[1],
               'created_at': row[2]} for row in rows]

    conn.close()

    return jsonify({'history_images': images})

if __name__ == '__main__':
    app.run(debug=True)
