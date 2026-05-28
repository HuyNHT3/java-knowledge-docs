# Java: Lớp (Class) và Đối tượng (Object)

## Mục lục

1. Khái niệm Class và Object
2. Cấu trúc của một Class
3. Thuộc tính (Fields / Variables)
4. Phương thức (Methods)
5. Constructor (Hàm khởi tạo)
6. Từ khóa `this`
7. Access Modifiers (Phạm vi truy cập)
8. Encapsulation (Đóng gói)
9. Static Members
10. Static Block và Instance Block
11. Nested Classes (Lớp lồng)
12. Anonymous Class
13. Immutable Class
14. Vòng đời của Object
15. `equals()` và `hashCode()`
16. `toString()`
17. Best Practices khi thiết kế Class

---

# 1. Khái niệm Class và Object

## Class

**Class** là bản thiết kế (blueprint) để tạo ra các đối tượng.

```java
class Student {
    String name;
    int age;

    void study() {
        System.out.println("Studying...");
    }
}
```

### Sơ đồ

```
Class (Blueprint)
     │
     ▼
+----------------+
|   Student      |
|----------------|
| name           |
| age            |
|----------------|
| study()        |
+----------------+
```

---

## Object

Object là **instance của class**.

```java
Student s1 = new Student();
Student s2 = new Student();
```

### Sơ đồ

```
Class: Student

        │
        │ tạo object
        ▼

+------------+     +------------+
| Student s1 |     | Student s2 |
|------------|     |------------|
| name       |     | name       |
| age        |     | age        |
+------------+     +------------+
```

---

# 2. Cấu trúc của một Class

Một class Java thường gồm:

```
Class
 ├── Fields
 ├── Constructors
 ├── Methods
 ├── Blocks
 └── Nested Classes
```

Ví dụ:

```java
class Car {

    // field
    String brand;

    // constructor
    Car(String brand) {
        this.brand = brand;
    }

    // method
    void run() {
        System.out.println("Car running");
    }
}
```

---

# 3. Thuộc tính (Fields)

Field là **biến được khai báo trong class**.

```java
class Car {
    String brand;
    int speed;
}
```

### Các loại Field

| Loại              | Mô tả        |
| ----------------- | ------------ |
| Instance Variable | thuộc object |
| Static Variable   | thuộc class  |
| Final Variable    | hằng số      |

---

## Instance Variable

```
Object A
 ├── name
 └── age

Object B
 ├── name
 └── age
```

Mỗi object có bản sao riêng.

---

## Static Variable

```java
class User {
    static int count = 0;
}
```

Sơ đồ:

```
Class User
 ├── static count
 │
 ├── User object 1
 ├── User object 2
 └── User object 3
```

---

# 4. Methods (Phương thức)

Method định nghĩa **hành vi của object**.

```java
class Dog {

    void bark() {
        System.out.println("Woof");
    }

}
```

### Sơ đồ

```
Object: Dog

   bark()
     │
     ▼
  "Woof"
```

---

## Method có tham số

```java
void eat(String food) {
    System.out.println("Eating " + food);
}
```

---

## Method trả về giá trị

```java
int add(int a, int b) {
    return a + b;
}
```

---

# 5. Constructor (Hàm khởi tạo)

Constructor được gọi khi tạo object.

```java
class Person {

    String name;

    Person(String name) {
        this.name = name;
    }

}
```

### Sơ đồ

```
new Person("Huy")

      │
      ▼

+----------------+
| Person object  |
|----------------|
| name = "Huy"   |
+----------------+
```

---

## Constructor Overloading

```java
class Product {

    String name;
    double price;

    Product() {}

    Product(String name) {
        this.name = name;
    }

    Product(String name, double price) {
        this.name = name;
        this.price = price;
    }
}
```

---

# 6. Từ khóa `this`

`this` tham chiếu đến **object hiện tại**.

```java
class User {

    String name;

    User(String name) {
        this.name = name;
    }
}
```

### Sơ đồ

```
Object User

   this
    │
    ▼
 current object
```

---

# 7. Access Modifiers

| Modifier  | Phạm vi            |
| --------- | ------------------ |
| private   | chỉ trong class    |
| default   | cùng package       |
| protected | package + subclass |
| public    | mọi nơi            |

### Sơ đồ

```
public
 ├── package
 │   ├── protected
 │   │   └── subclass
 │   └── default
 └── private (class only)
```
| Modifier   | Cùng class | Cùng package | Subclass | Khác package |
|------------|------------|--------------|----------|--------------|
| public     | ✔          | ✔            | ✔        | ✔            |
| protected  | ✔          | ✔            | ✔        | ❌           |
| default    | ✔          | ✔            | ❌       | ❌           |
| private    | ✔          | ❌           | ❌       | ❌           |
---

# 8. Encapsulation (Đóng gói)

Nguyên tắc:

* field nên **private**
* truy cập qua **getter/setter**

```java
class Account {

    private double balance;

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }
}
```

### Sơ đồ

```
Outside World
      │
      ▼
+----------------+
|   Account      |
|----------------|
| private balance|
|----------------|
| getBalance()   |
| setBalance()   |
+----------------+
```

---

# 9. Static Members

`static` thuộc về class.

```java
class MathUtil {

    static int add(int a, int b) {
        return a + b;
    }

}
```

### Sơ đồ

```
MathUtil class

   add()

MathUtil.add(2,3)
```

---

# 10. Static Block và Instance Block

## Static Block

Chạy **khi class được load**.

```java
class Config {

    static {
        System.out.println("Class loaded");
    }

}
```

---

## Instance Block

Chạy mỗi lần tạo object.

```java
class Example {

    {
        System.out.println("Object created");
    }

}
```

---

# 11. Nested Classes

Class bên trong class.

### Static Nested Class

```java
class Outer {

    static class Inner {
        void show() {}
    }

}
```

Sơ đồ:

```
Outer
 └── Inner
```

---

### Inner Class

```java
class Outer {

    class Inner {
        void show() {}
    }

}
```

---

# 12. Anonymous Class

Class không tên.

```java
Runnable r = new Runnable() {
    public void run() {
        System.out.println("Running");
    }
};
```

---

# 13. Immutable Class

Class **không thể thay đổi sau khi tạo**.

```java
final class User {

    private final String name;

    public User(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

---

# 14. Vòng đời của Object

```
Class Loading
      │
      ▼
Object Creation (new)
      │
      ▼
Initialization
      │
      ▼
Object Usage
      │
      ▼
Garbage Collection
```

---

# 15. equals() và hashCode()

Dùng để so sánh object.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof User)) return false;
    User user = (User) o;
    return name.equals(user.name);
}
```

---

# 16. toString()

Dùng để debug object.

```java
@Override
public String toString() {
    return "User{name='" + name + "'}";
}
```

---

# 17. Best Practices khi thiết kế Class

✔ Fields nên **private**
✔ Sử dụng **constructor để khởi tạo object**
✔ Class nên **immutable khi có thể**
✔ Tránh **God Class**
✔ Override `equals()` và `hashCode()` khi cần
✔ Sử dụng **composition thay vì inheritance khi hợp lý**

---
