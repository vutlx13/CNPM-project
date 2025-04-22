import sqlite3

# Kết nối hoặc tạo mới file CSDL
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Tạo bảng thư viện ảnh (ảnh có sẵn để test)
cursor.execute('''
CREATE TABLE IF NOT EXISTS library_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    url TEXT
)
''')

# Tạo bảng lịch sử người dùng
cursor.execute('''
CREATE TABLE IF NOT EXISTS history_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()