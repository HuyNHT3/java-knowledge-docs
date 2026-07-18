# Database Advanced SQL & Objects (MySQL)

> Tài liệu này cung cấp kiến thức chi tiết về các đối tượng nâng cao và cơ chế giao dịch trong MySQL, bao gồm **Stored Procedure (Thủ tục lưu trữ)**, **Transaction (Giao dịch)**, và **View (Bảng ảo)**. Đây là những khái niệm quan trọng để lập trình viên Backend tối ưu hiệu năng ứng dụng và bảo đảm tính toàn vẹn của dữ liệu.

---

# 1. Stored Procedure (Thủ tục lưu trữ)

## Khái niệm
**Stored Procedure** là một tập hợp các câu lệnh SQL được biên dịch sẵn (precompiled) và lưu trữ trực tiếp trong cơ sở dữ liệu. Ứng dụng client thay vì gửi các chuỗi lệnh SQL dài qua mạng thì chỉ cần thực hiện gọi thủ tục bằng câu lệnh `CALL`.

### Lợi ích:
- **Tăng hiệu năng:** Do câu lệnh đã được biên dịch sẵn trên database server, giảm thiểu thời gian phân tích cú pháp (parsing) của database.
- **Tiết kiệm băng thông:** Giảm tải lưu lượng mạng vì client chỉ truyền tên thủ tục và các tham số.
- **Tăng cường bảo mật:** Có thể phân quyền cho một tài khoản chỉ được phép thực thi (`EXECUTE`) thủ tục mà không cần cấp quyền truy cập trực tiếp trên các bảng dữ liệu gốc.
- **Tập trung logic nghiệp vụ:** Giúp bảo trì logic xử lý dữ liệu tập trung tại một nơi thay vì rải rác ở nhiều dịch vụ Backend khác nhau.

---

## Cú pháp cơ bản
Trong MySQL, ta cần thay đổi ký tự kết thúc câu lệnh mặc định (dấu `;`) thành một ký tự khác (ví dụ: `//`) bằng từ khóa `DELIMITER`. Điều này giúp MySQL hiểu rằng toàn bộ khối lệnh trong thủ tục là một thực thể duy nhất chứ không bị ngắt quãng bởi các dấu `;` nội bộ.

```sql
DELIMITER //

CREATE PROCEDURE name_procedure (
    [IN | OUT | INOUT] param_name data_type,
    ...
)
BEGIN
    -- Khối lệnh SQL xử lý
END //

DELIMITER ;
```

### Các chế độ tham số (Parameter Modes):
1. **IN** (Mặc định): Tham số đầu vào truyền dữ liệu từ bên ngoài vào thủ tục. Giá trị của nó không thể bị thay đổi ra bên ngoài sau khi kết thúc thủ tục.
2. **OUT**: Tham số đầu ra dùng để trả kết quả từ thủ tục về cho bên gọi.
3. **INOUT**: Kết hợp cả đầu vào và đầu ra; nhận giá trị ban đầu từ bên ngoài, có thể bị thay đổi giá trị trong thủ tục và trả lại giá trị mới đó ra ngoài.

---

## Ví dụ thực tế

### Ví dụ 1: Thủ tục không có tham số (Xem danh sách sản phẩm)
```sql
DELIMITER //

CREATE PROCEDURE GetAllProducts()
BEGIN
    SELECT id, name, price, stock 
    FROM products;
END //

DELIMITER ;

-- Gọi thủ tục thực thi
CALL GetAllProducts();
```

### Ví dụ 2: Thủ tục có tham số IN và OUT (Tính tổng số tiền tiêu dùng của khách hàng)
Giả sử ta cần tính tổng tiền của tất cả các đơn hàng thuộc về một khách hàng cụ thể (`p_customer_id`) và lưu kết quả vào tham số đầu ra (`p_total_spending`).

```sql
DELIMITER //

CREATE PROCEDURE GetCustomerTotalSpending(
    IN p_customer_id INT,
    OUT p_total_spending DECIMAL(10, 2)
)
BEGIN
    SELECT COALESCE(SUM(total), 0)
    INTO p_total_spending
    FROM orders
    WHERE customer_id = p_customer_id;
END //

DELIMITER ;

-- Sử dụng biến session @spending để nhận giá trị trả về từ thủ tục
CALL GetCustomerTotalSpending(1, @spending);

-- Xem kết quả
SELECT @spending AS total_spent;
```

---

# 2. Transaction (Giao dịch)

## Khái niệm
**Transaction** là một nhóm các câu lệnh SQL được thực thi như một đơn vị công việc logic duy nhất. Transaction đảm bảo tính toàn vẹn dữ liệu bằng cách tuân thủ nguyên tắc: **tất cả các câu lệnh đều thành công (COMMIT)** hoặc **không câu lệnh nào được áp dụng vào database (ROLLBACK)** khi xuất hiện bất kỳ lỗi nào.
Đây là nền tảng để thực thi tính chất **ACID** (Atomicity, Consistency, Isolation, Durability) trong cơ sở dữ liệu quan hệ.

---

## Cú pháp thực thi
Trong MySQL (sử dụng Storage Engine InnoDB để hỗ trợ transaction):
- `START TRANSACTION` hoặc `BEGIN`: Đánh dấu điểm khởi đầu của giao dịch.
- `COMMIT`: Áp dụng vĩnh viễn tất cả các thay đổi thực hiện trong giao dịch hiện tại vào ổ đĩa.
- `ROLLBACK`: Hủy bỏ toàn bộ thay đổi của giao dịch hiện tại, đưa cơ sở dữ liệu trở lại trạng thái trước khi bắt đầu giao dịch.
- `SAVEPOINT name_point`: Tạo một điểm mốc trung gian trong giao dịch.
- `ROLLBACK TO name_point`: Khôi phục dữ liệu quay về điểm mốc đã lưu mà không hủy bỏ toàn bộ giao dịch.

---

## Ví dụ thực tế: Giao dịch chuyển tiền ngân hàng
Quy trình chuyển $100 từ tài khoản A (`id = 1`) sang tài khoản B (`id = 2`) yêu cầu cả hai thao tác cập nhật số dư phải thành công đồng thời:

```sql
-- Khởi động giao dịch
START TRANSACTION;

-- 1. Trừ tiền tài khoản A
UPDATE accounts 
SET balance = balance - 100 
WHERE id = 1 AND balance >= 100;

-- Kiểm tra: Nếu số dư của A không đủ (không dòng nào bị ảnh hưởng), ta tạo điểm kiểm tra
-- Ở đây ta tiếp tục mô phỏng bước kế tiếp
SAVEPOINT step1_done;

-- 2. Cộng tiền tài khoản B
UPDATE accounts 
SET balance = balance + 100 
WHERE id = 2;

-- Nếu không có lỗi gì xảy ra, lưu vĩnh viễn thay đổi vào database
COMMIT;

-- Nếu có bất kỳ lỗi nào xảy ra trong quá trình thực hiện:
-- ROLLBACK;
```

---

# 3. View (Bảng ảo)

## Khái niệm
**View** là một bảng ảo được định nghĩa bởi một câu lệnh truy vấn dữ liệu (`SELECT`). Nó không trực tiếp lưu trữ dữ liệu vật lý trên ổ đĩa. Khi bạn thực hiện truy vấn từ một View, database engine sẽ chạy câu lệnh `SELECT` làm nền tảng của nó để lấy dữ liệu thời gian thực từ các bảng gốc.

### Lợi ích:
- **Đơn giản hóa truy vấn:** Thay vì bắt lập trình viên phải viết các câu lệnh `JOIN` phức tạp qua nhiều bảng, ta có thể gói gọn nó vào một View để truy vấn đơn giản như trên một bảng thông thường.
- **Tăng tính bảo mật:** Cho phép ẩn đi các cột dữ liệu nhạy cảm (như mật khẩu, lương nhân viên) khỏi bảng gốc và chỉ trưng bày các cột an toàn qua View.
- **Bảo trì dễ dàng:** Nếu cấu trúc các bảng gốc thay đổi, ta chỉ cần cập nhật định nghĩa câu lệnh `SELECT` của View mà không cần thay đổi code của ứng dụng.

---

## Cú pháp cơ bản
```sql
-- Tạo View mới
CREATE VIEW name_view AS
SELECT column1, column2, ...
FROM table_name
WHERE condition;

-- Truy vấn dữ liệu từ View giống như bảng vật lý
SELECT * FROM name_view;

-- Xóa View khi không còn sử dụng
DROP VIEW name_view;
```

---

## Ví dụ thực tế
Giả sử hệ thống cần xuất báo cáo doanh số mua hàng của khách hàng thường xuyên. Thay vì lặp lại truy vấn `JOIN` phức tạp giữa bảng `customers` và `orders`:

```sql
-- Tạo View tổng hợp thông tin mua sắm của khách hàng
CREATE VIEW customer_spending_report AS
SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    COUNT(o.id) AS total_orders,
    SUM(o.total) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;

-- Truy vấn báo cáo cực kỳ nhanh gọn từ View
SELECT * FROM customer_spending_report
WHERE total_spent > 500
ORDER BY total_spent DESC;
```

---

# Tổng kết

| Đối tượng | Vai trò chính | Trường hợp sử dụng |
| :--- | :--- | :--- |
| **Stored Procedure** | Đóng gói logic nghiệp vụ phức tạp ngay trên DB | Xử lý dữ liệu lớn tuần tự, giảm thiểu round-trip mạng |
| **Transaction** | Đảm bảo tính toàn vẹn của chuỗi câu lệnh liên đới | Các giao dịch tài chính, đặt hàng thanh toán (ACID) |
| **View** | Đơn giản hóa cấu trúc dữ liệu hiển thị và bảo mật | Viết báo cáo phức tạp, phân quyền bảo mật cột |
