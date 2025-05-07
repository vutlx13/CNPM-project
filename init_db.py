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
CREATE TABLE IF NOT EXISTS history_images_new (
    filename TEXT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public INTEGER DEFAULT 0,
    username TEXT,
    created_at
)
''')

cursor.execute('''
INSERT INTO history_images_new (filename, upload_time, is_public, created_at)
SELECT filename, upload_time, is_public, created_at FROM history_images
''')

cursor.execute('DROP TABLE history_images')

cursor.execute('ALTER TABLE history_images_new RENAME TO history_images')

conn.commit()
conn.close()
