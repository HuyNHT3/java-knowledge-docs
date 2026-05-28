Merge Sort

void mergeProcess(int[] A, int[] B) {
    int m = A.length, n = B.length;
    int i = 0, j = 0;

    while (i < m && j < n) {
        if (A[i] <= B[j]) {
            process(A[i]); // xử lý phần tử A[i]
            i++;
        } else {
            process(B[j]); // xử lý phần tử B[j]
            j++;
        }
    }

    // phần còn lại
    while (i < m) {
        process(A[i]);
        i++;
    }

    while (j < n) {
        process(B[j]);
        j++;
    }
}

Sliding window

int left = 0;

for (int right = 0; right < n; right++) {

    // 1. mở rộng window
    add(s.charAt(right));

    // 2. thu hẹp nếu vi phạm điều kiện
    while (vi phạm điều kiện) {
        remove(s.charAt(left));
        left++;
    }

    // 3. cập nhật kết quả
    updateResult(left, right);
}

Binary search

int left = 0, right = n - 1;

while (left <= right) {
    int mid = left + (right - left) / 2;

    if (condition(mid)) {
        // giữ lại bên trái
        right = mid - 1;
    } else {
        // giữ lại bên phải
        left = mid + 1;
    }
}