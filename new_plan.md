# Project Plan: Lightweight Markdown Documentation Viewer (Multi-Category Version)

## 1. Project Objective
Tạo một ứng dụng web dạng Single Page Application (SPA) siêu nhẹ để hiển thị kho kiến thức Java Core dựa trên cấu trúc phân cấp thư mục thực tế (`memory-bank/`).
* **Tiêu chí cốt lõi:** Không cài đặt môi trường, không `npm`, không cần build. Hệ thống tự động phân loại bài viết theo danh mục (Categories) dựa trên cấu trúc cha - con và render động bằng Vanilla JavaScript thông qua CDN.

---

## 2. Technology Stack & Architecture

### Core Stack (Chạy trực tiếp qua Browser CDN)
* **Base Framework:** Thuần HTML5, CSS3 và Vanilla JavaScript (ES6+).
* **UI/Styling:** Tailwind CSS (Play CDN) + `@tailwindcss/typography` (class `prose`) giúp tự động format văn bản tài liệu và bảng biểu.
* **Markdown Parser:** `Marked.js` (Chuyển đổi cú pháp `.md` sang HTML).
* **Syntax Highlighting:** `Prism.js` + module `prism-java.min.js` (Tô màu mã nguồn Java).

### Data Flow & Routing
* **Phân cấp cấu trúc (Nested Registry):** Cấu hình `registry.json` sẽ được thiết kế theo dạng Nhóm (Category) -> Bài viết (Articles) để khớp với thư mục `Foundation knowledge` và `Interview Startegies`.
* **Fetch Dynamic:** Trình duyệt tự động mò vào từng thư mục con để `fetch()` nội dung dựa trên đường dẫn tương đối (ví dụ: `./memory-bank/Foundation knowledge/ClassAndObject.md`).

---

## 3. Development Phases

### Phase 1: Chuẩn hóa cấu trúc & Khởi tạo
* Giữ nguyên và tổ chức thư mục gốc như ảnh chụp thực tế:
    ```text
    📂 JAVA ECOSYSTEM CONSULTANT/
    ├── 📄 index.html             (File giao diện & Logic xử lý chính)
    ├── 📄 registry.json          (File cấu hình menu phân cấp)
    └── 📂 memory-bank/
        ├── 📂 Foundation knowledge/
        │   ├── 📄 ClassAndObject.md
        │   ├── 📄 Design Patterns.md
        │   └── ...
        └── 📂 Interview Startegies/
            ├── 📄 Algorhythm_Patterns.md
            └── ...
    ```

### Phase 2: Thiết kế cấu hình Phân cấp (`registry.json`)
* Xây dựng file cấu hình chứa đường dẫn chính xác của các file `.md` theo từng nhóm:
    ```json
    [
      {
        "category": "Foundation Knowledge",
        "folder": "Foundation knowledge",
        "items": [
          { "slug": "ClassAndObject", "title": "Class and Object" },
          { "slug": "Design Patterns", "title": "Design Patterns" },
          { "slug": "JavaCauTrucDuLieu", "title": "Java Cấu Trúc Dữ Liệu" },
          { "slug": "ThuakeDahinhTruutuong", "title": "Thừa kế - Đa hình - Trừu tượng" }
        ]
      },
      {
        "category": "Interview Strategies",
        "folder": "Interview Startegies",
        "items": [
          { "slug": "Algorhythm_Patterns", "title": "Algorithm Patterns" },
          { "slug": "Java_BackEnd_Interview", "title": "Java Backend Interview" },
          { "slug": "JavaCore_doccument", "title": "Java Core Document" }
        ]
      }
    ]
    ```

### Phase 3: Xây dựng Giao diện Accordion Menu (Tailwind CSS)
* **Multi-level Sidebar:** Thanh menu bên trái sẽ hiển thị tên Danh mục lớn (có thể thêm tính năng click để đóng/mở cụm bài viết). Bên trong danh mục là danh sách các bài viết con thụt lề vào trong.
* **Main Content Window:** Vùng hiển thị nội dung tài liệu chuẩn chỉ, responsive tốt trên các thiết bị.

### Phase 4: Xử lý Logic JavaScript (Core Engine nâng cấp)
* Hàm `initApp()` sẽ lặp qua các tầng của `registry.json` để dựng menu dạng tiêu đề nhóm + bài viết con.
* Hàm `loadMarkdownFile(folder, slug)` sẽ ghép đường dẫn động:
    ```javascript
    const url = `./memory-bank/${folder}/${slug}.md`;
    const response = await fetch(url);
    ```
* Convert nội dung bằng `marked.parse()` và kích hoạt `Prism.highlightAll()` để highlight code Java.

### Phase 5: Polish & Deployment
* Thêm thanh Filter lọc nhanh tên bài viết trên sidebar (hỗ trợ tìm kiếm không phân biệt hoa thường).
* Chạy ứng dụng qua VS Code `Live Server` ở local để tránh lỗi CORS, hoặc kéo thả toàn bộ thư mục lên GitHub Pages/Vercel khi cần chia sẻ link online.

### Phase 6: Hướng dẫn triển khai lên GitHub Pages
Để đưa ứng dụng lên GitHub Pages và tận dụng kiến trúc file `.md` riêng biệt (không cần bundle nội dung vào `index.html`), bạn thực hiện các bước sau:

1.  **Tạo Repository mới trên GitHub:**
    *   Truy cập GitHub và đăng nhập.
    *   Click vào dấu `+` ở góc trên bên phải, chọn `New repository`.
    *   Đặt tên cho repository (ví dụ: `java-knowledge-docs`). Đảm bảo là `Public`.
    *   **Không** tích chọn `Add a README file`, `Add .gitignore`, `Choose a license` (chúng ta sẽ đẩy file từ local lên).
    *   Click `Create repository`.

2.  **Khởi tạo Git Repository cục bộ và đẩy mã nguồn:**
    *   Mở Terminal hoặc Command Prompt trong thư mục gốc của dự án (`JAVA ECOSYSTEM CONSULTANT/`).
    *   Khởi tạo Git:
        ```bash
        git init
        ```
    *   Thêm tất cả các file vào staging area:
        ```bash
        git add .
        ```
    *   Commit các thay đổi:
        ```bash
        git commit -m "Initial commit: Lightweight Java Docs"
        ```
    *   Liên kết repository cục bộ với repository trên GitHub (thay `YOUR_USERNAME` và `YOUR_REPOSITORY_NAME` bằng thông tin của bạn):
        ```bash
        git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
        git branch -M main
        git push -u origin main
        ```

3.  **Cấu hình GitHub Pages:**
    *   Trên trang repository của bạn trên GitHub, click vào tab `Settings`.
    *   Trong menu bên trái, chọn `Pages`.
    *   Dưới mục "Build and deployment", trong phần "Source", chọn `Deploy from a branch`.
    *   Trong phần "Branch", chọn `main` (hoặc nhánh bạn đã đẩy code lên) và chọn thư mục `/ (root)`.
    *   Click `Save`.

4.  **Truy cập ứng dụng:**
    *   Sau vài phút (thường là 1-5 phút), GitHub Pages sẽ triển khai ứng dụng của bạn.
    *   Bạn sẽ thấy một URL hiển thị trên trang `Settings -> Pages` (ví dụ: `https://YOUR_USERNAME.github.io/YOUR_REPOSITORY_NAME/`).
    *   Truy cập URL này để xem ứng dụng của bạn trực tuyến. Từ giờ, bạn có thể chia sẻ link này cho mọi người.

---

## 4. Technical Constraints & Considerations
* **Đường dẫn file chính xác:** Tên thư mục vật lý (ví dụ: `Interview Startegies` đang viết sai chính tả chữ Str**a**tegies thành St**ar**tegies) cần phải ghi *chính xác từng ký tự* trong file cấu hình JSON để hàm `fetch()` không bị lỗi `404 Not Found`.

---

## 5. Success Criteria
* [ ] Sidebar hiển thị rõ ràng, phân biệt được bài viết nào thuộc nhóm "Foundation" và bài nào thuộc nhóm "Interview".
* [ ] Click vào bài viết bất kỳ ở bất kỳ nhóm nào, nội dung Markdown đều được fetch và hiển thị chính xác.
* [ ] Code Java bên trong các file `.md` được tô màu chuẩn (Prism Tomorrow Theme).
* [ ] Thêm bài mới bằng cách thả file vào đúng thư mục con và cập nhật file JSON mục lục trong 30 giây.