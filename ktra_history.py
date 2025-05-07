import sqlite3

# Kết nối tới database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# Truy vấn tất cả dữ liệu trong bảng history_images
cursor.execute('SELECT * FROM history_images')

# Lấy tất cả dữ liệu
rows = cursor.fetchall()

# In kết quả
for row in rows:
    print(row)
# Đóng kết nối
conn.close()