# Bài thực hành Buổi 4 · Giới hạn 30 chỗ có bằng chứng

Tiếp tục thư mục ngayhoi của Buổi 3.

| Tệp | Dùng ở bước | Ghi chú |
|---|---|---|
| spec_mau.md | 2 | Bảng 6 ví dụ để đối chiếu sau khi tự viết spec.md |
| test_khung.py | 3 | Phần đầu tệp test: DB_PATH, TestClient, fixture xóa bảng, hàm lap_day |
| ban_dong_thoi.py | 6–7 | Bắn 40 yêu cầu đồng thời vào máy chủ đang chạy |

## Kết quả mong đợi
| Lúc | Lệnh | In ra |
|---|---|---|
| Bước 4 | python -m pytest -q | 1 failed, 4 passed |
| Bước 5 | python -m pytest -q | 5 passed |
| Bước 6 (có sleep, chưa sửa) | python ban_dong_thoi.py P09 | 201 > 30 |
| Bước 7 (có sleep, đã sửa) | python ban_dong_thoi.py P10 | 201: 30 · 409: 10 |
