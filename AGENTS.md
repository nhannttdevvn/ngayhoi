# Cổng đăng ký Ngày hội việc làm
## Cấu trúc
- backend/: FastAPI + SQLite (main.py)
- frontend/: React + Vite — không sửa khi làm việc ở backend
## Chạy test
cd backend && python -m pytest -q
## Không được sửa
- backend/tests/test_gioi_han.py và buoi-04/spec_mau.md (chỉ người sửa)
- .github/ (cổng CI)
## Xong việc nghĩa là
- pytest xanh, PR dưới 200 dòng, mô tả theo mẫu 5 mục
