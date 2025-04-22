import sqlite3

def add_to_library(name, url):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO library_images (name, url) VALUES (?, ?)", (name, url))
    conn.commit()
    conn.close()

def get_library_images():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, url FROM library_images")
    images = cursor.fetchall()
    conn.close()
    return images

def delete_from_library(name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM library_images WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def delete_from_librarya(url):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM library_images WHERE url = ?", (url,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    while True:
        print("\n📌 Chọn chức năng:")
        print("1. Thêm ảnh vào thư viện")
        print("2. Xem ảnh trong thư viện")
        print("3. Xoá ảnh khỏi thư viện")
        print("4. Thoát")

        choice = input("👉 Nhập số: ")

        if choice == "1":
            name = input("🖼️ Nhập tên ảnh: ")
            url = input("🔗 Nhập đường dẫn ảnh: ")
            add_to_library(name, url)
            print("✅ Đã thêm ảnh!")

        elif choice == "2":
            images = get_library_images()
            if images:
                print("\n📚 Thư viện ảnh:")
                for name, url in images:
                    print(f"- {name}: {url}")
            else:
                print("📭 Thư viện trống.")

        elif choice == "3":
            print("1. Xoá ảnh bằng tên")
            print("2. Xoá ảnh bằng nguồn")
            choice = input("👉 Nhập số: ")
            if choice == "1":
                name = input("🗑️ Nhập tên ảnh cần xoá: ")
                delete_from_library(name)
            elif choice == "2":
                url = input("🗑️ Nhập nguồn ảnh cần xoá: ")
                delete_from_librarya(url)
            else: print("❌ Lựa chọn không hợp lệ. Nhập lại.")
            print("🧹 Đã xoá ảnh (nếu tồn tại)!")
            images = get_library_images()
            if images:
                print("\n📚 Thư viện ảnh:")
                for name, url in images:
                    print(f"- {name}: {url}")
            else:
                print("📭 Thư viện trống.")

        elif choice == "4":
            print("👋 Thoát chương trình.")
            break

        else:
            print("❌ Lựa chọn không hợp lệ. Nhập lại.")
