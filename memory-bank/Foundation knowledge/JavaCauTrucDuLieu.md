# Java Core -- Collections & Data Structures (Interview Notes)

## MENU

1. [HashMap Internals (hash, bucket, resize)](#1-hashmap-internals)
2. [Collision & Treeify (Java 8)](#2-collision-treeify)
3. [ArrayList vs LinkedList](#3-arraylist-vs-linkedlist)
4. [HashSet vs TreeSet](#4-hashset-vs-treeset)
5. [ConcurrentHashMap & Multithreading](#5-concurrenthashmap--threads)
6. [Big-O (Complexity cơ bản)](#6-big-o)
7. [equals() & hashCode() contract](#7-equals--hashcode)
8. [Java Stream API](#8-java-stream-api)

------------------------------------------------------------------------

## 1. HashMap Internals

**Cấu trúc bên trong:**
HashMap sử dụng một mảng (Array) làm xương sống, gọi là `Node<K,V>[] table`.
Mỗi phần tử trong mảng này được gọi là một **Bucket**.

### 1.1 Array & Bucket
- **Array:** Là nơi lưu trữ chính. Mặc định capacity là 16 (2^4). Capacity luôn là lũy thừa của 2.
- **Bucket:** Tại mỗi index của Array, không chỉ chứa 1 phần tử mà chứa **đầu mối (head)** của một cấu trúc dữ liệu (Linked List hoặc Red-Black Tree).
- **Index Calculation (Bitwise masking):**
  Java không dùng toán tử `%` (modulo) vì chậm. Thay vào đó dùng bitwise `&` để tìm vị trí bucket. Điều này chỉ đúng khi capacity `n` là lũy thừa của 2.

  ```java
  // Cách Java tính index (nhanh hơn %)
  // n là capacity (ví dụ 16)
  index = (n - 1) & hash;
  ```

### 1.2 Resize (Rehashing)
Là quá trình **mở rộng mảng chứa** khi số lượng phần tử vượt quá ngưỡng cho phép, nhằm giảm thiểu va chạm (collision).

- **Load Factor (Hệ số tải):** Mặc định **0.75**. Đây là điểm cân bằng (trade-off) giữa *Time* (tốc độ truy xuất) và *Space* (bộ nhớ).
  - Nếu quá nhỏ (ví dụ 0.5): Tốn bộ nhớ (nhiều bucket rỗng).
  - Nếu quá lớn (ví dụ 1.0): Tiết kiệm bộ nhớ nhưng dễ bị Collision -> bucket dài -> tìm kiếm chậm (O(n) hoặc O(log n)).

- **Threshold (Ngưỡng):** `capacity * load_factor`.
  - Ví dụ: Mặc định capacity = 16. Threshold = 16 * 0.75 = 12.
  - Khi thêm phần tử thứ 13 -> Kích hoạt Resize.

- **Quá trình Resize hoạt động ra sao?**
  1. Tạo mảng mới (new table) với kích thước **gấp đôi** (ví dụ 16 -> 32).
  2. **Rehashing:** Duyệt qua toàn bộ các bucket cũ, tính toán lại vị trí (index) cho **TỪNG** node để chuyển sang mảng mới.
  3. **Tối ưu của Java:** Vì size tăng gấp đôi (thêm 1 bit vào mask), một node tại index `i` cũ chỉ có 2 trường hợp:
     - Giữ nguyên vị trí `i`.
     - Chuyển sang vị trí `i + oldCap`.
     -> Không cần tính lại `hashCode` từ đầu, chỉ cần kiểm tra bit cao nhất.

> **Performance Note:** Resize là thao tác **O(n)** rất tốn kém.
> **Best Practice:** Nếu biết trước sẽ chứa 1000 phần tử, hãy khởi tạo `new HashMap<>(1334)` (1000/0.75 + 1) để tránh việc resize liên tục.

### 1.3 Khi nào nên dùng HashMap? (Real-world Use Cases)
HashMap là lựa chọn mặc định (Go-to choice) cho 90% các trường hợp cần lưu trữ Key-Value, cụ thể:

1.  **High-Performance Lookup (Tra cứu O(1)):**
    - Khi có Unique Identifier (ID) và cần lấy dữ liệu ngay lập tức.
    - *Ví dụ:* Caching `Map<UserId, UserDTO>` để tránh query DB liên tục.

2.  **Grouping & Indexing (Gom nhóm dữ liệu):**
    - Chuyển đổi List phẳng thành cấu trúc phân cấp.
    - *Ví dụ:* Gom sản phẩm theo danh mục -> `Map<CategoryId, List<Product>>`.

3.  **Frequency Counting (Đếm tần suất):**
    - *Ví dụ:* Đếm số lần xuất hiện của từ khóa trong log file -> `Map<String, Integer>`.

4.  **Lookup Tables (Bảng tra cứu):**
    - Thay thế cho các cấu trúc `switch-case` hoặc `if-else` dài ngoằng.
    - *Ví dụ:* `Map<String, Strategy> actionMap`.

**⚠️ Khi nào KHÔNG nên dùng HashMap?**
- **Cần đa luồng (Multi-thread):** Tuyệt đối không dùng. Phải dùng `ConcurrentHashMap`. (HashMap không thread-safe, có thể gây mất dữ liệu hoặc CPU spike 100% do infinite loop khi resize ở Java cũ).
- **Cần giữ thứ tự (Ordering):**
    - Thứ tự chèn (Insertion Order) -> Dùng `LinkedHashMap`.
    - Thứ tự sắp xếp Key (Sorted Key) -> Dùng `TreeMap` (Red-Black Tree, O(log n)).
- **Bộ nhớ hạn hẹp:** HashMap tốn bộ nhớ overhead cho đối tượng `Node` và mảng `bucket`. Nếu lưu lượng lớn primitive (ví dụ `Map<Integer, Integer>`), hãy cân nhắc các thư viện tối ưu primitive (như Eclipse Collections) để giảm boxing/unboxing.

### 1.4 Các thao tác cơ bản (Cheat Sheet)

```java
import java.util.*;

Map<String, Integer> map = new HashMap<>();

// 1. Thêm & Cập nhật
map.put("A", 1); 
map.putIfAbsent("B", 2);

// 2. Truy xuất
map.get("A");               // Trả về 1
map.getOrDefault("C", 0);   // Trả về 0 nếu không thấy

// 3. Kiểm tra & Xóa
map.containsKey("A");       // true
map.remove("A");            // Xóa key A

// 4. Duyệt Map
map.forEach((k, v) -> System.out.println(k + " -> " + v));

// 5. Tính toán (Java 8)
map.merge("B", 1, Integer::sum); // Tăng giá trị B thêm 1
```


------------------------------------------------------------------------

## 2. Collision & Treeify
### 2.1 Collision (Va chạm)
(xử lý cho hashmap tránh bị đụng độ)
Xảy ra khi `(n - 1) & hash` trả về cùng một index cho các Key khác nhau. 
**Hệ quả:** Các Node sẽ cùng nằm trong một Bucket.

### 2.2 Treeification (Cây hóa)
Để tránh hiện tượng "Hash DoS attack" (tạo ra hàng loạt key trùng hash để làm chậm hệ thống), Java 8 cải tiến:

- **Cấu trúc:** Chuyển từ `Linked List` (O(n)) sang `Red-Black Tree` (O(log n)).
- **Điều kiện kích hoạt:**
    1.  Số lượng phần tử trong 1 bucket đạt tới `TREEIFY_THRESHOLD = 8`.
    2.  Tổng capacity của HashMap phải đạt ít nhất `MIN_TREEIFY_CAPACITY = 64`.
    *Lưu ý:* Nếu bucket >= 8 nhưng capacity < 64, Java sẽ gọi `resize()` thay vì treeify.

### 2.3 Untreeify (Hủy cây hóa)
- Khi số lượng phần tử trong bucket giảm xuống `UNTREEIFY_THRESHOLD = 6` (do `remove` hoặc `resize`), cấu trúc cây sẽ chuyển ngược lại thành Linked List.
- **Tại sao là 6 và 8?** Khoảng cách giữa 6 và 8 giúp tránh việc cấu trúc dữ liệu bị chuyển đổi liên tục (flickering) nếu ta liên tục thêm/xóa 1 phần tử tại ngưỡng đó.

### 2.4 Tại sao Red-Black Tree?
- Giúp đảm bảo hiệu năng trong trường hợp xấu nhất.
- Red-Black Tree là cây nhị phân tìm kiếm tự cân bằng, đảm bảo chiều cao cây luôn ở mức `log(n)`.

**Phân tích độ phức tạp (Worst case):**
- **Chưa treeify:** O(n)
- **Đã treeify:** O(log n)

> **Phỏng vấn Tip:** Interviewer có thể hỏi "Tại sao không treeify ngay từ đầu?". Trả lời: Vì Tree Node tốn bộ nhớ hơn (có thêm tham chiếu left, right, parent, color) và với số lượng phần tử nhỏ (< 8), tốc độ của Linked List vẫn rất nhanh.

### 2.5 Ứng dụng thực tế khi coding

#### 1. Khởi tạo Capacity (Tránh Resize tốn kém)
Nếu bạn biết trước mình sẽ lưu khoảng 1000 phần tử, đừng khởi tạo `new HashMap<>()`.

```java
// SAI: Gây ra khoảng 6-7 lần resize và rehashing lại toàn bộ dữ liệu
Map<String, User> map = new HashMap<>(); 

// ĐÚNG: Tính toán dựa trên Load Factor 0.75 (1000 / 0.75 + 1 ≈ 1334)
Map<String, User> optimizedMap = new HashMap<>(1334);
```

#### 2. Viết hashCode() phân tán (Tránh Collision)
Hàm `hashCode()` tồi sẽ ép các phần tử vào cùng một bucket, khiến HashMap từ O(1) biến thành O(log n).

```java
class User {
    private int id;
    private String email;

    // SAI: Mọi user đều vào cùng 1 bucket nếu id đều là số chẵn
    @Override
    public int hashCode() {
        return id % 2; 
    }

    // ĐÚNG: Sử dụng Objects.hash()
    @Override
    public int hashCode() {
        return Objects.hash(id, email); 
    }
    /* 
       Tác dụng của Objects.hash():
       - Kết hợp mã hash của nhiều trường (id, email) thành 1 số duy nhất.
       - Null-safe: Tự động xử lý nếu id hoặc email bị null.
       - Sử dụng hệ số 31 để tối ưu phân tán và tốc độ tính toán (bit-shifting).
    */
}
```

#### 3. Ưu tiên Key Immutable (Tránh "Mất tích" Object)
Nếu bạn dùng một Object có thể thay đổi (mutable) làm Key, và bạn thay đổi thuộc tính của nó sau khi đã `put` vào Map, bạn sẽ không bao giờ tìm lại được nó nữa.

```java
class MutableKey {
    String name;
    MutableKey(String name) { this.name = name; }
    @Override
    public int hashCode() { return name.hashCode(); }
}

MutableKey key = new MutableKey("Huy");
map.put(key, "Developer");

key.name = "Hoàng"; // Thay đổi field dùng để tính hash

System.out.println(map.get(key)); // Kết quả: NULL (vì hash mới khác hash cũ)
```
*Lời khuyên: Luôn dùng `String`, `Integer` hoặc các class `final` với field `private final` làm Key.*

#### 4. Cảnh giác với Object lớn (Hiệu năng tính toán)
HashMap gọi hàm `hashCode()` mỗi khi bạn `get()` hoặc `put()`. Nếu Key là một Object chứa List cực lớn hoặc chuỗi siêu dài, việc tính hash sẽ rất chậm.

```java
class HeavyKey {
    List<String> largeData; // Chứa 1 triệu phần tử

    @Override
    public int hashCode() {
        // Việc duyệt qua 1 triệu phần tử để tính hash mỗi lần 'get' sẽ làm CPU spike
        return largeData.hashCode(); 
    }
}
```
*Giải pháp: Nếu bắt buộc dùng Key phức tạp, hãy tính `hashCode` một lần duy nhất khi khởi tạo và lưu vào một biến (Caching hash code) giống như cách lớp `String` trong Java đang làm.*

------------------------------------------------------------------------

## 3. ArrayList vs LinkedList (Deep Dive)

### 3.1 Cấu trúc dữ liệu và Đặc điểm

| Đặc điểm | ArrayList | LinkedList |
| :--- | :--- | :--- |
| **Cấu trúc bên trong** | Sử dụng một mảng động (Dynamic Array). | Sử dụng danh sách liên kết kép (Doubly Linked List). |
| **Thao tác truy xuất** | **Nhanh.** Truy cập trực tiếp qua index nhờ địa chỉ ô nhớ liên tiếp. | **Chậm.** Phải duyệt từ đầu (hoặc cuối) danh sách đến vị trí cần tìm. |
| **Thêm/Xóa (Insert/Delete)** | **Chậm.** Cần dịch chuyển (shifting) các phần tử phía sau. Nếu mảng đầy, cần resize. | **Nhanh.** Chỉ cần thay đổi con trỏ (pointer) của các node lân cận. |
| **Sử dụng bộ nhớ** | **Ít hơn.** Chỉ lưu trữ giá trị phần tử. | **Nhiều hơn.** Mỗi phần tử (Node) tốn thêm bộ nhớ để lưu con trỏ `next` và `prev`. |
| **Khả năng Cache** | **Tốt.** Do các phần tử nằm kề nhau nên tận dụng được CPU Cache. | **Kém.** Các Node nằm rải rác trong Heap, dễ gây Cache Miss. |

### 3.2 Bảng so sánh độ phức tạp (Big-O)

| Operation | ArrayList | LinkedList |
| :--- | :--- | :--- |
| **get(index)** | O(1) | O(n) |
| **add(element)** (vào cuối) | O(1) (Amortized) | O(1) |
| **add(index, element)** | O(n) (Do shifting) | O(n) (Do tìm vị trí) |
| **remove(index)** | O(n) (Do shifting) | O(n) (Do tìm vị trí) |
| **addFirst / removeFirst** | O(n) | O(1) |

### 3.3 Khi nào dùng cái nào? (Real-world Decision)

#### 1. Ưu tiên dùng `ArrayList` khi:
- Cần truy xuất phần tử theo index thường xuyên (`list.get(i)`).
- Ứng dụng ưu tiên việc đọc dữ liệu nhiều hơn là ghi/thêm mới.
- Số lượng phần tử lớn và bạn muốn tiết kiệm RAM (tránh overhead của Node pointer).
- Dữ liệu được thêm chủ yếu vào cuối danh sách.

#### 2. Ưu tiên dùng `LinkedList` khi:
- Cần thao tác thêm/xóa ở **hai đầu** danh sách thường xuyên (LinkedList triển khai interface `Deque`).
- Bạn sử dụng nó như một **Stack** hoặc **Queue**.
- Không biết trước số lượng phần tử và việc thêm/xóa xảy ra liên tục ở giữa danh sách (nhưng lưu ý bạn phải có sẵn tham chiếu đến Node đó qua `Iterator`).

### 3.4 Code Example: Performance Comparison

```java
import java.util.*;

public class ListComparison {
    public static void main(String[] args) {
        int iterations = 100000;
        List<Integer> arrayList = new ArrayList<>();
        List<Integer> linkedList = new LinkedList<>();

        // 1. Thêm vào đầu (Add at the beginning)
        long startTime = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            arrayList.add(0, i); // O(n) - Rất chậm cho ArrayList
        }
        System.out.println("ArrayList addFirst: " + (System.nanoTime() - startTime) / 1e6 + " ms");

        startTime = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            linkedList.add(0, i); // O(1) - Rất nhanh cho LinkedList
        }
        System.out.println("LinkedList addFirst: " + (System.nanoTime() - startTime) / 1e6 + " ms");

        // 2. Truy xuất ngẫu nhiên (Random Access)
        startTime = System.nanoTime();
        for (int i = 0; i < 1000; i++) {
            arrayList.get(iterations / 2); // O(1)
        }
        System.out.println("ArrayList get(middle): " + (System.nanoTime() - startTime) / 1e6 + " ms");

        startTime = System.nanoTime();
        for (int i = 0; i < 1000; i++) {
            linkedList.get(iterations / 2); // O(n) - Phải duyệt lại từ đầu
        }
        System.out.println("LinkedList get(middle): " + (System.nanoTime() - startTime) / 1e6 + " ms");
    }
}
```

### 3.5 Lưu ý quan trọng cho Senior Level

- **ArrayList Resizing:** Khi ArrayList đạt đến ngưỡng (default 10), nó sẽ tạo mảng mới có kích thước gấp khoảng **1.5 lần** mảng cũ và copy dữ liệu qua (dùng `Arrays.copyOf`). Thao tác này là O(n). Để tối ưu, hãy khởi tạo `new ArrayList<>(initialCapacity)` nếu biết trước số lượng.
- **LinkedList không hẳn là nhanh hơn khi chèn ở giữa:** Dù việc đổi pointer là O(1), nhưng để đến được vị trí `index` cần chèn, LinkedList phải tốn O(n) để duyệt. Trong nhiều trường hợp, việc dịch chuyển mảng của ArrayList còn nhanh hơn việc duyệt Node của LinkedList do cơ chế tối ưu bộ nhớ đệm (CPU Cache).
- **Fail-fast Iterator:** Cả hai đều ném ra `ConcurrentModificationException` nếu danh sách bị thay đổi cấu trúc (structural modification) trong khi đang duyệt bằng Iterator, trừ khi dùng chính method `remove()` của Iterator.
- **Thread-safety:** Cả hai đều **không thread-safe**. Nếu cần dùng trong môi trường đa luồng, hãy cân nhắc `CopyOnWriteArrayList` hoặc `Collections.synchronizedList()`.

### 3.6 Hướng dẫn sử dụng chi tiết

#### 3.6.1 ArrayList: Thao tác với mảng động
`ArrayList` là lựa chọn mặc định khi bạn cần một danh sách có thể thay đổi kích thước và truy cập phần tử nhanh chóng.

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ArrayListUsage {
    public static void main(String[] args) {
        // 1. Khởi tạo (Nên chỉ định Capacity nếu biết trước size)
        List<String> list = new ArrayList<>(20);

        // 2. Thêm phần tử
        list.add("Java");      // Thêm vào cuối - O(1)
        list.add(0, "Python"); // Thêm vào vị trí index - O(n)

        // 3. Truy xuất và Cập nhật
        String lang = list.get(1);     // Lấy phần tử theo index - O(1)
        list.set(1, "JavaScript");      // Thay thế phần tử - O(1)

        // 4. Xóa phần tử
        list.remove(0);           // Xóa theo index - O(n)
        list.remove("Java");      // Xóa theo object - O(n)

        // 5. Kiểm tra và Sắp xếp
        boolean hasJava = list.contains("Java"); // O(n)
        Collections.sort(list);                  // Sắp xếp danh sách

        // 6. Duyệt danh sách (Sử dụng Stream API cho Modern Java)
        list.forEach(System.out::println);
    }
}
```

#### 3.6.2 LinkedList: Thao tác với Danh sách liên kết & Deque
`LinkedList` đặc biệt mạnh khi bạn sử dụng nó như một **Queue** (Hàng đợi) hoặc **Deque** (Hàng đợi hai đầu) nhờ triển khai các phương thức hỗ trợ thao tác tại hai đầu.

```java
import java.util.LinkedList;
import java.util.Deque;

public class LinkedListUsage {
    public static void main(String[] args) {
        // 1. Khởi tạo (Thường dùng interface Deque để tận dụng các method đặc thù)
        LinkedList<String> linkedList = new LinkedList<>();
        Deque<String> stackOrQueue = new LinkedList<>();

        // 2. Thao tác đặc thù ở hai đầu (Rất nhanh - O(1))
        linkedList.addFirst("Header");
        linkedList.addLast("Footer");
        
        String first = linkedList.getFirst();
        String last = linkedList.getLast();

        // 3. Sử dụng như một Stack (LIFO - Last In First Out)
        stackOrQueue.push("Action 1");
        stackOrQueue.push("Action 2");
        String lastAction = stackOrQueue.pop(); // Lấy và xóa phần tử vừa thêm vào

        // 4. Sử dụng như một Queue (FIFO - First In First Out)
        stackOrQueue.offer("Customer 1");
        stackOrQueue.offer("Customer 2");
        String nextCustomer = stackOrQueue.poll(); // Lấy và xóa phần tử đầu hàng đợi

        // 5. Duyệt ngược danh sách (Chỉ LinkedList làm tốt điều này)
        var iterator = linkedList.descendingIterator();
        while(iterator.hasNext()) {
            System.out.println(iterator.next());
        }
    }
}
```

**💡 Tip:** Nếu bạn chỉ cần dùng các method của `List` (add, get, remove), hãy luôn chọn `ArrayList`. Chỉ chuyển sang `LinkedList` khi thực sự cần các tính năng của `Queue`, `Stack` hoặc phải chèn/xóa liên tục ở hai đầu danh sách.

------------------------------------------------------------------------

## 4. HashSet vs TreeSet (Deep Dive)

### 4.1 HashSet
**Bản chất:** Sử dụng một `HashMap` nội bộ để lưu trữ phần tử.

- **Cách hoạt động:** Khi bạn gọi `add(E e)` vào HashSet, nó thực chất thực hiện `map.put(e, PRESENT)`, trong đó `PRESENT` là một object giả (dummy object) dùng chung để làm giá trị cho mọi key.
- **Đặc điểm:**
    - Không cho phép phần tử trùng lặp (Uniqueness).
    - **Không bảo toàn thứ tự** chèn (Unordered). Thứ tự có thể thay đổi sau khi resize.
    - Cho phép chứa một phần tử `null`.
    - Hiệu năng: Truy xuất, thêm, xóa đều là **O(1)** trong điều kiện lý tưởng (ít va chạm hash).

### 4.2 TreeSet
**Bản chất:** Sử dụng một `TreeMap` nội bộ, dựa trên cấu trúc cây nhị phân tự cân bằng (Red-Black Tree).

- **Đặc điểm:**
    - Không cho phép phần tử trùng lặp.
    - **Luôn tự động sắp xếp** các phần tử theo thứ tự tự nhiên (Natural Ordering) hoặc theo một `Comparator` tùy chỉnh.
    - **Không cho phép null:** Vì cần thực hiện so sánh (`compareTo` hoặc `compare`) giữa các phần tử để sắp xếp, nên thêm `null` sẽ gây ra `NullPointerException`.
    - Hiệu năng: Các thao tác cơ bản là **O(log n)**.
    - Triển khai `NavigableSet`, cung cấp các phương thức tìm kiếm khoảng như `higher()`, `lower()`, `ceiling()`, `floor()`.

### 4.2.1 Khai báo TreeSet với thứ tự giảm dần (Descending Order)
Mặc định, `TreeSet` sử dụng "Natural Ordering" (tăng dần). Để sắp xếp từ cao xuống thấp, ta cần truyền vào một `Comparator`.

**Cách 1: Sử dụng `Collections.reverseOrder()`**
Đây là cách chuyên nghiệp và dễ đọc nhất.
```java
Set<Integer> descendingSet = new TreeSet<>(Collections.reverseOrder());
```

**Cách 2: Sử dụng Lambda Expression**
Phù hợp khi bạn muốn tùy biến sâu hơn logic so sánh.
```java
Set<Integer> descendingSet = new TreeSet<>((a, b) -> b.compareTo(a));
```

> **Lưu ý:** Nếu sắp xếp Object tùy chỉnh, hãy đảm bảo thuộc tính dùng để so sánh không bị `null` để tránh `NullPointerException`.

### 4.3 Bảng so sánh chi tiết

| Đặc điểm | HashSet | TreeSet |
| :--- | :--- | :--- |
| **Cấu trúc dữ liệu** | Hash Table | Red-Black Tree |
| **Thứ tự (Ordering)** | Không xác định | Có thứ tự (Sorted) |
| **Hiệu năng (Time)** | Nhanh hơn (O(1)) | Chậm hơn (O(log n)) |
| **Phần tử Null** | Cho phép | Không cho phép |
| **Cơ chế so sánh** | `hashCode()` và `equals()` | `compareTo()` hoặc `compare()` |
| **Sử dụng khi nào?** | Chỉ cần lọc trùng dữ liệu | Cần tập hợp luôn được sắp xếp |

### 4.4 Code Example: So sánh thực tế

```java
import java.util.*;

public class SetDemo {
    public static void main(String[] args) {
        // 1. HashSet: Tốc độ tối đa, không quan tâm thứ tự
        Set<String> hashSet = new HashSet<>();
        hashSet.add("Zebra");
        hashSet.add("Apple");
        hashSet.add("Mango");
        hashSet.add("Apple"); // Sẽ bị bỏ qua
        System.out.println("HashSet: " + hashSet); 
        // Output (thứ tự ngẫu nhiên): [Apple, Zebra, Mango]

        // 2. TreeSet: Tự động sắp xếp A-Z
        Set<String> treeSet = new TreeSet<>();
        treeSet.add("Zebra");
        treeSet.add("Apple");
        treeSet.add("Mango");
        System.out.println("TreeSet: " + treeSet);
        // Output (luôn cố định): [Apple, Mango, Zebra]

        // 3. NavigableSet features (Chỉ có ở TreeSet)
        TreeSet<Integer> scores = new TreeSet<>(Arrays.asList(50, 85, 40, 90, 70));
        System.out.println("Điểm thấp nhất >= 60: " + scores.ceiling(60)); // 70
        System.out.println("Điểm cao nhất < 85: " + scores.lower(85));    // 70
    }
}
```

### 4.5 Những lưu ý quan trọng khi đi phỏng vấn

1.  **Contract giữa equals/hashCode:** Đối với `HashSet`, nếu bạn thêm một Object tùy chỉnh (ví dụ `User`), bạn **phải** override cả `equals()` và `hashCode()`. Nếu không, Set sẽ không thể nhận diện được hai object có cùng nội dung là "trùng nhau".
2.  **Contract của TreeSet:** Đối với `TreeSet`, các phần tử phải triển khai interface `Comparable` hoặc bạn phải truyền vào một `Comparator`. Nếu không, chương trình sẽ ném ra `ClassCastException`.
3.  **LinkedHashSet:** Nếu interviewer hỏi: *"Làm sao để vừa lọc trùng (Set) vừa giữ đúng thứ tự lúc thêm vào (Insertion Order)?"* -> Câu trả lời là **LinkedHashSet**. Nó là sự kết hợp giữa HashSet và LinkedList, tốn bộ nhớ hơn một chút nhưng bảo toàn được thứ tự chèn.

**Tóm tắt lựa chọn:**
- **HashSet:** Lựa chọn mặc định cho hiệu năng tốt nhất.
- **LinkedHashSet:** Dùng khi cần giữ thứ tự chèn (ví dụ: danh sách lịch sử truy cập gần đây).
- **TreeSet:** Dùng khi cần dữ liệu luôn được sắp xếp theo thứ tự (ví dụ: danh sách điểm số từ cao đến thấp).

### 4.6 Trick: Chuyển đổi nhanh từ List sang TreeSet
Một câu hỏi phỏng vấn phổ biến: *"Nếu có một ArrayList vừa lộn xộn vừa trùng lặp, làm sao để có một danh sách vừa sạch (không trùng) vừa thứ tự nhanh nhất?"*

**Giải pháp:** Pass trực tiếp List vào constructor của TreeSet.

```java
List<String> dirtyList = Arrays.asList("Z", "A", "B", "A", "Z");
Set<String> cleanSet = new TreeSet<>(dirtyList);
// cleanSet lúc này là: [A, B, Z]
```

**Phân tích kỹ thuật cho Senior:**
- **Độ phức tạp:** Thao tác này tốn **O(N log N)**. Trong đó `N` là số phần tử của List, và mỗi lần chèn vào TreeSet (cây đỏ đen) tốn `log N`.
- **Điều kiện:** Các phần tử trong List **phải** cùng kiểu dữ liệu và implement interface `Comparable` (hoặc bạn phải cung cấp một `Comparator` riêng). Nếu List chứa các Object không thể so sánh, nó sẽ ném ra `ClassCastException`.
- **Lưu ý về Null:** Nếu trong `ArrayList` của bạn có chứa phần tử `null`, thao tác parse này sẽ văng `NullPointerException` ngay lập tức vì `TreeSet` không chấp nhận `null`.

------------------------------------------------------------------------

## 5. ConcurrentHashMap & Threads (Deep Dive)

`ConcurrentHashMap` là phiên bản thread-safe của `HashMap`, được thiết kế để tối ưu cho môi trường đa luồng (multi-threaded).

### 5.1 Cơ chế hoạt động (Java 8+)
Thay vì khóa toàn bộ bảng như `Hashtable`, `ConcurrentHashMap` sử dụng:

- **CAS (Compare-And-Swap):** Sử dụng các thao tác nguyên tử (atomic operations) của CPU để thêm một Node mới vào bucket rỗng mà không cần dùng lock.
- **Synchronized trên từng Node đầu (Bucket-level lock):** Chỉ khi có sự va chạm (collision) trong một bucket, Java mới dùng `synchronized` trên chính Node đầu tiên của bucket đó.

### 5.2 Tại sao không cho phép NULL?
Khác với `HashMap`, `ConcurrentHashMap` **không cho phép** Key hoặc Value là `null`.
**Lý do:** Để tránh sự mập mờ. Nếu `get(key)` trả về `null`, ta không biết là "Key không tồn tại" hay "Value là null". Trong đa luồng, việc check `containsKey()` rồi mới `get()` không đảm bảo tính nguyên tử (atomic).

### 5.3 Thread & Multithreading (Java Core)

#### 5.3.1 Cách tạo Thread

```java
// Cách 1: Implements Runnable (Khuyên dùng vì Java chỉ hỗ trợ đơn kế thừa)
Runnable task = () -> System.out.println("Running task...");
new Thread(task).start();

// Cách 2: Kế thừa lớp Thread
class MyThread extends Thread {
    public void run() { System.out.println("Running thread..."); }
}
new MyThread().start();
```

#### 5.3.2 Race Condition & Cách xử lý
**Race Condition** xảy ra khi nhiều luồng cùng sửa đổi một biến dùng chung dẫn đến kết quả sai lệch.

**Giải pháp 1: Synchronized (Lock)**
```java
synchronized (this) {
    count++;
}
```

**Giải pháp 2: Atomic Variables (Non-blocking)**
```java
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();
```

#### 5.3.3 Thread Pool (ExecutorService)
Nên dùng Thread Pool thay vì tạo `new Thread()` thủ công để tối ưu tài nguyên.

```java
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> System.out.println("Task in pool"));
executor.shutdown();
```

### 5.4 So sánh Map trong Đa luồng

| Tiêu chí | Hashtable | HashMap | ConcurrentHashMap |
| :--- | :--- | :--- | :--- |
| **Thread-safe** | ✅ Có | ❌ Không | ✅ Có |
| **Cơ chế** | Lock toàn bộ Map | Không có | Lock từng Bucket (CAS) |
| **Hiệu năng** | Thấp | Cao (Đơn luồng) | Cao (Đa luồng) |
| **Null Key/Value** | ❌ Không | ✅ Có | ❌ Không |


------------------------------------------------------------------------

## 6. Big-O

| Cấu trúc dữ liệu | Get | Insert | Delete |
| :--- | :--- | :--- | :--- |
| **ArrayList** | O(1) | O(n) | O(n) |
| **LinkedList** | O(n) | O(1) | O(1) |
| **HashMap** | O(1) | O(1) | O(1) |
| **TreeMap** | O(log n) | O(log n) | O(log n) |

------------------------------------------------------------------------

## 7. equals & hashCode

**Quy tắc vàng:** Nếu `a.equals(b) == true` thì `a.hashCode() == b.hashCode()` bắt buộc phải đúng.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    User user = (User) o;
    return id == user.id && Objects.equals(name, user.name);
}

@Override
public int hashCode() {
    return Objects.hash(id, name);
}
```

## 8. Java Stream
Java Stream API (Java 8+) mang đến phong cách lập trình hàm (functional programming), giúp xử lý các collection dữ liệu một cách khai báo (declarative) thay vì mệnh lệnh (imperative).

### 8.1 Functional Programming Basics in Java
Stream dựa trên các **Functional Interface**:
- `Predicate<T>`: Nhận T, trả về `boolean` (Dùng trong `filter`).
- `Function<T, R>`: Nhận T, trả về R (Dùng trong `map`).
- `Consumer<T>`: Nhận T, trả về `void` (Dùng trong `forEach`).
- `Supplier<T>`: Không nhận gì, trả về T.

### 8.2 Method Reference
Cú pháp viết tắt cho Lambda: `ClassName::methodName`. Giúp code ngắn gọn, dễ đọc và tập trung vào ý định thực hiện.

**4 loại Method Reference phổ biến:**

1.  **Static Method Reference**: `ContainingClass::staticMethodName`
    - `Integer::parseInt` tương đương `str -> Integer.parseInt(str)`
    - `Objects::nonNull` tương đương `obj -> Objects.nonNull(obj)`
    - `Math::max` tương đương `(a, b) -> Math.max(a, b)`

2.  **Instance Method of a Particular Object**: `containingObject::instanceMethodName`
    - `System.out::println` tương đương `x -> System.out.println(x)`
    - `this::myMethod` tương đương `x -> this.myMethod(x)`

3.  **Instance Method of an Arbitrary Object of a Particular Type**: `ContainingType::methodName`
    - `String::toLowerCase` tương đương `str -> str.toLowerCase()`
    - `String::isEmpty` tương đương `str -> str.isEmpty()`
    - `Employee::getSalary` tương đương `emp -> emp.getSalary()`

4.  **Constructor Reference**: `ClassName::new`
    - `ArrayList::new` tương đương `() -> new ArrayList<>()`
    - `User::new` (nếu có constructor `User(String name)`) tương đương `name -> new User(name)`

**Ví dụ thực tế:**
```java
list.stream().filter(Objects::nonNull).map(String::trim).forEach(System.out::println);
```

### 8.3 Stream API Fundamentals
Một Stream Pipeline gồm 3 phần:
1. **Source**: (List, Set, Array, File...)
2. **Intermediate Operations**: Xử lý logic, luôn trả về một Stream mới (**Lazy Evaluation** - chỉ chạy khi có terminal operation).
3. **Terminal Operation**: Kết thúc stream và trả về kết quả (List, Single Value, void).

### 8.4 Intermediate Operations (Lazy)
- `filter(Predicate)`: Lọc phần tử.
- `map(Function)`: Chuyển đổi kiểu dữ liệu.
- `flatMap(Function)`: "Phẳng hóa" các stream con (thường dùng xử lý `List<List<T>>`).
- `distinct()`: Loại bỏ trùng lặp (dựa trên `equals`).
- `sorted()`: Sắp xếp.
- `peek(Consumer)`: Debug giữa các bước mà không làm thay đổi dữ liệu.

### 8.5 Terminal Operations (Eager)
- `collect(Collector)`: Gom kết quả về List, Set, Map.
- `forEach(Consumer)`: Duyệt qua từng phần tử.
- `reduce(BinaryOperator)`: Kết hợp các phần tử thành 1 giá trị duy nhất (tổng, max...).
- `anyMatch`, `allMatch`, `noneMatch`: Kiểm tra điều kiện.
- `count()`: Đếm số phần tử.

### 8.6 Collectors Framework
`java.util.stream.Collectors` cung cấp các tiện ích mạnh mẽ:
```java
List<String> names = users.stream()
    .map(User::getName)
    .collect(Collectors.toList());

// Gom nhóm (Grouping)
Map<Department, List<User>> byDept = users.stream()
    .collect(Collectors.groupingBy(User::getDepartment));

// Tính toán
Double avgAge = users.stream()
    .collect(Collectors.averagingInt(User::getAge));
```

### 8.7 Advanced Stream Operations
- `Stream.iterate()` và `Stream.generate()`: Tạo stream vô hạn.
- `takeWhile(Predicate)` và `dropWhile(Predicate)` (Java 9+): Lấy/bỏ phần tử cho đến khi gặp điều kiện dừng.

### 8.8 Optional & Stream Integration
Optional có thể coi như một Stream có tối đa 1 phần tử:
```java
Optional<User> userOpt = findUserById(id);
List<String> names = userOpt.stream() // Java 9+
    .map(User::getName)
    .collect(Collectors.toList());
```

### 8.9 Parallel Stream & Performance
- Sử dụng `parallelStream()` để tận dụng đa nhân CPU (qua Common ForkJoinPool).
- **Khi nào dùng?** Dữ liệu cực lớn, thao tác xử lý mỗi phần tử tốn thời gian, và các thao tác phải **không phụ thuộc thứ tự (stateless)**.
- **Cảnh báo:** Tránh dùng với các tác vụ I/O hoặc khi chia nhỏ dữ liệu tốn kém hơn xử lý tuần tự.

### 8.10 Custom Collector
Bạn có thể tự tạo Collector qua `Collector.of(...)` nếu các phương thức sẵn có của `Collectors` không đáp ứng được logic phức tạp.

### 8.11 Stream Debugging & Best Practices
- **Không tái sử dụng Stream**: Stream đã gọi terminal operation sẽ bị đóng.
- **Hạn chế Side Effects**: Tránh thay đổi biến bên ngoài bên trong lambda.
- **Sử dụng `peek()` để debug**: Xem dữ liệu trôi qua pipeline mà không dừng stream.
- **Ưu tiên Primitive Streams**: Dùng `IntStream`, `LongStream`, `DoubleStream` để tránh Autoboxing tốn hiệu năng.

### 8.12 Real-world Use Cases
1. **Dịch dữ liệu (DTO Mapping)**: Chuyển đổi Entity sang DTO.
2. **Lọc dữ liệu**: Tìm các đơn hàng đã thanh toán trong tháng.
3. **Tính toán báo cáo**: Group doanh thu theo danh mục sản phẩm.

### 8.13 Interview & Coding Patterns
- **Câu hỏi kinh điển**: "Phân biệt `map` và `flatMap`?", "Tại sao Stream là lazy?".
- **Pattern phổ biến**:
```java
// Tìm User lớn tuổi nhất của mỗi phòng ban
Map<Department, Optional<User>> topUserByDept = users.stream()
    .collect(Collectors.groupingBy(
        User::getDepartment,
        Collectors.maxBy(Comparator.comparingInt(User::getAge))
    ));
```
Level tiếp theo:
flatMap nâng cao
groupingBy + mapping
comparator chaining
optional chuẩn

Level thực chiến:
Stream vs Database
performance
debug stream
exception handling