# Singleton Pattern

## 1. Khái niệm

Singleton Pattern là một mẫu thiết kế đảm bảo rằng một class chỉ có
**một instance duy nhất** và cung cấp một điểm truy cập toàn cục đến
instance đó.

------------------------------------------------------------------------

## 2. Ý tưởng chính

-   Chỉ tạo 1 object duy nhất
-   Dùng lại object đó trong toàn bộ chương trình

------------------------------------------------------------------------

## 3. Ví dụ KHÔNG dùng Singleton

``` java
public class DatabaseConnection {

    public DatabaseConnection() {
        System.out.println("Tạo kết nối mới tới database");
    }

    public void connect() {
        System.out.println("Đang kết nối database...");
    }
}

public class Main {
    public static void main(String[] args) {
        DatabaseConnection db1 = new DatabaseConnection();
        DatabaseConnection db2 = new DatabaseConnection();

        System.out.println(db1 == db2); // false
    }
}
```

------------------------------------------------------------------------

## 4. Ví dụ dùng Singleton

``` java
public class DatabaseConnection {

    private static DatabaseConnection instance;

    private DatabaseConnection() {
        System.out.println("Tạo DUY NHẤT 1 kết nối database");
    }

    public static DatabaseConnection getInstance() {
        if (instance == null) {
            instance = new DatabaseConnection();
        }
        return instance;
    }

    public void connect() {
        System.out.println("Đang kết nối database...");
    }
}

public class Main {
    public static void main(String[] args) {
        DatabaseConnection db1 = DatabaseConnection.getInstance();
        DatabaseConnection db2 = DatabaseConnection.getInstance();

        System.out.println(db1 == db2); // true
    }
}
```

------------------------------------------------------------------------

## 5. Ưu điểm

-   Tiết kiệm tài nguyên
-   Dễ quản lý resource dùng chung

------------------------------------------------------------------------

## 6. Nhược điểm

-   Khó test
-   Có thể gây phụ thuộc chặt (tight coupling)

------------------------------------------------------------------------

## 7. Khi nào dùng

-   Database connection
-   Logger
-   Config system
# Builder Pattern

## 1. Khái niệm

Builder Pattern là một mẫu thiết kế thuộc nhóm Creational, dùng để xây
dựng object phức tạp từng bước thay vì sử dụng constructor dài.

------------------------------------------------------------------------

## 2. Vấn đề khi không dùng Builder

``` java
public class User {
    private String name;
    private int age;
    private String email;
    private String address;

    public User(String name, int age, String email, String address) {
        this.name = name;
        this.age = age;
        this.email = email;
        this.address = address;
    }
}

// Sử dụng
User user = new User("Huy", 20, "huy@gmail.com", "Can Tho");
```

------------------------------------------------------------------------

## 3. Builder Pattern (Best Practice trong Java)

``` java
public class User {

    private String name;
    private int age;
    private String email;
    private String address;

    private User(Builder builder) {
        this.name = builder.name;
        this.age = builder.age;
        this.email = builder.email;
        this.address = builder.address;
    }

    public static class Builder {

        private String name;
        private int age;
        private String email;
        private String address;

        public Builder setName(String name) {
            this.name = name;
            return this;
        }

        public Builder setAge(int age) {
            this.age = age;
            return this;
        }

        public Builder setEmail(String email) {
            this.email = email;
            return this;
        }

        public Builder setAddress(String address) {
            this.address = address;
            return this;
        }

        public User build() {
            return new User(this);
        }
    }
}
```

------------------------------------------------------------------------

## 4. Cách sử dụng

``` java
User user = new User.Builder()
        .setName("Huy")
        .setAge(20)
        .setEmail("huy@gmail.com")
        .setAddress("Can Tho")
        .build();
```

------------------------------------------------------------------------

## 5. Ưu điểm

-   Dễ đọc, dễ hiểu
-   Không cần nhớ thứ tự tham số
-   Hỗ trợ optional field
-   Code clean hơn

------------------------------------------------------------------------

## 6. Nhược điểm

-   Code dài hơn
-   Phải viết thêm Builder class

------------------------------------------------------------------------

## 7. Builder có phải Nested Class không?

-   Không bắt buộc
-   Nhưng trong Java thường dùng static nested class

------------------------------------------------------------------------

## 8. Kết luận

Builder Pattern giúp tạo object phức tạp một cách rõ ràng, dễ đọc và dễ
bảo trì.
# Factory Pattern

## 1. Khái niệm

Factory Pattern là một mẫu thiết kế thuộc nhóm Creational, dùng để tạo
object mà không cần chỉ rõ class cụ thể.

------------------------------------------------------------------------

## 2. Vấn đề khi không dùng Factory

``` java
public class Main {
    public static void main(String[] args) {
        Car car = new Car();
        Bike bike = new Bike();
    }
}
```

### Nhược điểm:

-   Hard-code class cụ thể
-   Khó mở rộng
-   Vi phạm Open/Closed Principle

------------------------------------------------------------------------

## 3. Factory Pattern

### Interface chung

``` java
public interface Vehicle {
    void drive();
}
```

### Các class cụ thể

``` java
public class Car implements Vehicle {
    public void drive() {
        System.out.println("Driving a car");
    }
}

public class Bike implements Vehicle {
    public void drive() {
        System.out.println("Driving a bike");
    }
}
```

### Factory class

``` java
public class VehicleFactory {

    public static Vehicle getVehicle(String type) {
        if (type.equalsIgnoreCase("car")) {
            return new Car();
        } else if (type.equalsIgnoreCase("bike")) {
            return new Bike();
        }
        throw new IllegalArgumentException("Unknown type");
    }
}
```

------------------------------------------------------------------------

## 4. Cách sử dụng

``` java
public class Main {
    public static void main(String[] args) {
        Vehicle v1 = VehicleFactory.getVehicle("car");
        Vehicle v2 = VehicleFactory.getVehicle("bike");

        v1.drive();
        v2.drive();
    }
}
```

------------------------------------------------------------------------

## 5. Ưu điểm

-   Không cần biết class cụ thể
-   Dễ mở rộng
-   Code sạch hơn

------------------------------------------------------------------------

## 6. Nhược điểm

-   Có thể phức tạp nếu nhiều loại object

------------------------------------------------------------------------

## 7. Các biến thể

### Simple Factory

-   Dùng if/else hoặc switch

### Factory Method

-   Mỗi class có factory riêng

### Abstract Factory

-   Tạo nhóm object liên quan

------------------------------------------------------------------------

## 8. Kết luận

Factory Pattern giúp tách logic tạo object ra khỏi code chính, giúp hệ
thống dễ mở rộng và bảo trì.

# Software Development Life Cycle (SDLC)

Software Development Life Cycle (SDLC) là quy trình phát triển phần mềm từ khi nhận yêu cầu khách hàng cho đến khi triển khai và bảo trì hệ thống. Quy trình chuẩn bao gồm các bước: Requirement → Analysis → Design → Implementation → Testing → Deployment → Maintenance.

Ở bước Requirement (thu thập yêu cầu), nhóm phát triển làm việc với khách hàng để hiểu rõ nhu cầu, mục tiêu hệ thống, đối tượng sử dụng và các chức năng cần có. Kết quả của bước này thường là tài liệu BRD (Business Requirement Document).

Tiếp theo là bước Analysis (phân tích), nơi các yêu cầu nghiệp vụ được chuyển thành yêu cầu kỹ thuật cụ thể, ví dụ như các chức năng CRUD, validation, phân quyền. Output của bước này là tài liệu SRS (Software Requirement Specification).

Bước Design (thiết kế) bao gồm thiết kế tổng thể (high-level) và chi tiết (low-level). High-level design quyết định kiến trúc hệ thống (monolith hoặc microservices) và công nghệ sử dụng (ví dụ: Spring Boot, MySQL). Low-level design bao gồm thiết kế database (ERD), API, class diagram và luồng xử lý.

Sau đó là Implementation (lập trình), nơi developer bắt đầu code dựa trên thiết kế. Trong bước này cần tuân thủ clean code, sử dụng design patterns phù hợp và đảm bảo code dễ maintain.

Bước Testing đảm bảo hệ thống hoạt động đúng yêu cầu. Bao gồm unit test, integration test và manual test để kiểm tra các luồng nghiệp vụ chính và các trường hợp lỗi.

Tiếp theo là Deployment (triển khai), đưa hệ thống lên môi trường thực tế như server hoặc cloud. Thường sử dụng Docker, CI/CD pipeline (ví dụ GitHub Actions) để tự động hóa quá trình build và deploy.

Cuối cùng là Maintenance (bảo trì), bao gồm sửa lỗi (bug fixing), nâng cấp tính năng và tối ưu hiệu năng sau khi hệ thống đã được sử dụng.

Trong thực tế, quy trình này thường được áp dụng theo mô hình Agile/Scrum, nghĩa là không thực hiện một lần toàn bộ mà chia thành các vòng lặp nhỏ (sprint), mỗi sprint bao gồm các bước: backlog → sprint planning → development → daily meeting → demo → retrospective.

Ví dụ thực tế: xây dựng API login. Requirement là cho phép user đăng nhập bằng email/password. Analysis xác định cần validate input, kiểm tra dữ liệu trong database và trả về JWT. Design định nghĩa API POST /login và cấu trúc bảng User. Implementation viết controller, service và repository. Testing kiểm tra các trường hợp đăng nhập đúng/sai. Deployment đưa API lên server.

Một số sai lầm phổ biến cần tránh là: bắt đầu code khi chưa hiểu rõ yêu cầu, không thiết kế trước database và API, không viết test và hard-code logic làm giảm khả năng mở rộng.

Tóm lại, SDLC là quy trình: Hiểu yêu cầu → Phân tích → Thiết kế → Code → Test → Deploy → Bảo trì, giúp đảm bảo phần mềm được phát triển có hệ thống, dễ mở rộng và dễ bảo trì.

# Bài tập (Mini-Project)

Phần mềm nghe nhạc được xây dựng nhằm mang đến trải nghiệm quản lý và thưởng thức âm nhạc một cách tiện lợi và hiệu quả. Ứng dụng cho phép người dùng lưu trữ và quản lý danh sách bài hát cá nhân với đầy đủ thông tin như tên bài hát, ca sĩ, thể loại và thời lượng.

Người dùng có thể dễ dàng phân loại các bài hát theo từng thể loại nhạc, giúp việc tìm kiếm và tổ chức thư viện âm nhạc trở nên trực quan hơn. Bên cạnh đó, hệ thống còn hỗ trợ tạo danh mục các bài hát yêu thích, cho phép người dùng nhanh chóng truy cập và thưởng thức những ca khúc mà họ quan tâm nhất.

Với giao diện thân thiện và các chức năng quản lý linh hoạt, ứng dụng không chỉ giúp người dùng kiểm soát tốt thư viện âm nhạc của mình mà còn nâng cao trải nghiệm nghe nhạc hằng ngày.