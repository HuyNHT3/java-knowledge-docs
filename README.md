# Java Knowledge Bank - Hướng Dẫn Sử Dụng & Thêm Tài Liệu Mới

Dự án này là một ứng dụng Single Page Application (SPA) siêu nhẹ chạy bằng HTML, Tailwind CSS (qua CDN), và Javascript thuần. Nó tự động đọc và hiển thị các tài liệu dạng Markdown (`.md`) từ thư mục `memory-bank` dựa trên danh mục được cấu hình trong `registry.json`.

---

## 🚀 Hướng Dẫn Chạy Ứng Dụng Dưới Local

Do cơ chế bảo mật của các trình duyệt hiện đại (CORS Policy), bạn **không thể** mở trực tiếp file `index.html` bằng Chrome/Edge thông qua giao thức `file://` vì tính năng `fetch()` dữ liệu động `.md` và `registry.json` sẽ bị chặn. 

Dưới đây là 3 cách chạy ứng dụng ở máy cá nhân:

### Cách 1: Sử dụng Live Server trong VS Code (Khuyên dùng)
1. Cài đặt extension **Live Server** trong VS Code.
2. Mở thư mục dự án bằng VS Code.
3. Nhấp chuột phải vào file [index.html](file:///d:/AI%20Promting/Java%20EcoSystem%20Consultant/java-knowledge-docs/index.html) và chọn **Open with Live Server** (hoặc nhấn tổ hợp phím `Alt + L, Alt + O`).
4. Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ `http://127.0.0.1:5500/index.html`.

### Cách 2: Sử dụng Python HTTP Server
Nếu máy bạn đã cài sẵn Python:
1. Mở Terminal/Command Prompt và di chuyển vào thư mục chứa dự án.
2. Chạy lệnh:
   ```bash
   python -m http.server 8000
   ```
3. Truy cập địa chỉ `http://localhost:8000` trên trình duyệt của bạn.

### Cách 3: Sử dụng Trình duyệt Firefox
* Trình duyệt **Firefox** cho phép đọc các file cục bộ (`file://`) mà không bị chặn CORS. Bạn chỉ cần click đúp vào file [index.html](file:///d:/AI%20Promting/Java%20EcoSystem%20Consultant/java-knowledge-docs/index.html) và chọn mở bằng Firefox.

---

## 📝 Hướng Dẫn Thêm Tài Liệu Mới (Onboard Document)

Khi bạn muốn thêm một tài liệu mới vào hệ thống, hãy thực hiện theo quy trình 2 bước dưới đây:

### Bước 1: Chuẩn bị và lưu file Markdown (`.md`)
1. Chuyển đổi tài liệu của bạn sang định dạng **Markdown (`.md`)**.
   * *Nếu tài liệu gốc là `.docx` hoặc PDF:* Bạn có thể sử dụng các công cụ chuyển đổi trực tuyến hoặc tự viết lại bằng cú pháp Markdown chuẩn để đảm bảo hiển thị đẹp mắt (tiêu đề `#`, danh sách `-`, code block ` ```java `).
2. Lưu file tài liệu vào thư mục mong muốn bên trong [memory-bank](file:///d:/AI%20Promting/Java%20EcoSystem%20Consultant/java-knowledge-docs/memory-bank).
   * **Hỗ trợ thư mục phân cấp (Subfolders):** Bạn hoàn toàn có thể tạo các thư mục con lồng nhau để phân chia sâu hơn. Ví dụ: Tạo thư mục `memory-bank/Database/DatabaseDetail/` và lưu file `MySQL_Optimization.md` vào đó.
3. **Quy tắc đặt tên file:** Tên file nên viết liền không dấu hoặc dùng gạch dưới, không chứa khoảng trắng (ví dụ: `MySQL_Optimization.md`).

### Bước 2: Đăng ký tài liệu vào [registry.json](file:///d:/AI%20Promting/Java%20EcoSystem%20Consultant/java-knowledge-docs/registry.json)
Để tài liệu mới xuất hiện trên thanh Sidebar (thanh bên trái), bạn phải khai báo nó trong file cấu hình danh mục.

1. Mở file [registry.json](file:///d:/AI%20Promting/Java%20EcoSystem%20Consultant/java-knowledge-docs/registry.json).
2. Tìm hoặc tự thêm một đối tượng danh mục mới.
3. Cấu hình thuộc tính `"folder"` trỏ đến đường dẫn thư mục tính từ `memory-bank/` (dùng dấu `/` để phân tách các thư mục con).
4. Thêm đối tượng bài viết mới vào mảng `items`:
   ```json
   {
     "slug": "Ten_File_Khong_Co_Duoi_MD",
     "title": "Tiêu đề hiển thị trực quan trên Sidebar"
   }
   ```
   * **`slug`**: Phải trùng khớp **chính xác 100%** (kể cả chữ hoa/chữ thường) với tên file `.md` mà bạn đã tạo ở Bước 1 (không viết phần mở rộng `.md` vào slug).
   * **`title`**: Tiêu đề hiển thị thân thiện với người đọc trên menu ứng dụng.

#### 💡 Ví dụ cụ thể với Thư mục Phân cấp (`Database/DatabaseDetail`):
Nếu bạn vừa thêm file `MySQL_Optimization.md` vào thư mục `memory-bank/Database/DatabaseDetail/`, bạn sẽ thêm một danh mục mới vào [registry.json](file:///d:/AI%20Promting/Java%20EcoSystem%20Consultant/java-knowledge-docs/registry.json) như sau:

```json
  {
    "category": "Database > MySQL Details",
    "folder": "Database/DatabaseDetail",
    "items": [
      {
        "slug": "MySQL_Optimization",
        "title": "MySQL Query Optimization"
      }
    ]
  }
```
*(Đừng quên dấu phẩy `,` phân tách giữa các nhóm danh mục JSON để tránh bị lỗi cú pháp!)*

---

## 🛠️ Công cụ hỗ trợ Gom Dữ Liệu (`bundle_helper.py`)

Nếu bạn muốn tạo một gói dữ liệu tĩnh chứa tất cả nội dung của các file `.md` trong thư mục `memory-bank/` thành một file JSON/JS duy nhất (ví dụ để dùng cho các mục đích chạy offline hoàn toàn trên Chrome không cần server), bạn có thể chạy:

```bash
python bundle_helper.py
```
Script sẽ quét toàn bộ thư mục `memory-bank/` và xuất ra file `bundle.json` chứa nội dung của toàn bộ các file `.md` để bạn có thể tích hợp thêm.

---

## 🌐 Triển khai lên GitHub Pages (Đưa lên Online)

Nếu bạn muốn chia sẻ trang tài liệu này cho người khác xem online mà không cần tự chạy local server, GitHub Pages là giải pháp miễn phí tốt nhất:

1. **Khởi tạo repo và commit code:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Lightweight Java Docs"
   ```
2. **Liên kết và đẩy lên GitHub:**
   ```bash
   git remote add origin https://github.com/<YOUR_USERNAME>/<REPO_NAME>.git
   git branch -M main
   git push -u origin main
   ```
3. **Bật GitHub Pages:**
   * Vào Repo của bạn trên GitHub -> Chọn **Settings** -> Chọn **Pages**.
   * Phần *Source* chọn **Deploy from a branch**.
   * Chọn nhánh `main` và thư mục gốc `/ (root)`, sau đó bấm **Save**.
   * Đợi 1-3 phút, trang web của bạn sẽ được kích hoạt tại: `https://<YOUR_USERNAME>.github.io/<REPO_NAME>/`.
