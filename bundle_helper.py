import os
import json

# Script này giúp bạn gom tất cả nội dung file .md vào một biến JavaScript
# để bạn có thể chạy ứng dụng trực tiếp trên Chrome mà không cần Server.

def generate_bundle():
    base_path = "memory-bank"
    db = {}
    
    if not os.path.exists(base_path):
        print(f"Lỗi: Không tìm thấy thư mục '{base_path}'. Hãy đảm bảo script nằm cùng cấp với thư mục này.")
        return

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                folder = os.path.basename(root)
                slug = os.path.splitext(file)[0]
                # Tạo key theo định dạng "Tên thư mục/Tên file"
                key = f"{folder}/{slug}"
                
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    db[key] = f.read()
    
    # In kết quả ra màn hình để bạn copy
    print(json.dumps(db, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    generate_bundle()