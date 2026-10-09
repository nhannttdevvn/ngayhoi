# Sơ đồ hệ thống đăng ký Ngày hội việc làm

## 1. Kiến trúc hệ thống

```mermaid
flowchart LR
    U[Người dùng]
    F[React Frontend<br/>localhost:5173]
    A[FastAPI Backend<br/>localhost:8000]
    P[Pydantic Validation]
    D[(SQLite<br/>ngayhoi.db)]

    U -->|Nhập mã sinh viên + mã phiên| F
    F -->|POST /api/dang-ky| A
    A --> P
    P -->|Dữ liệu hợp lệ| D

    D -->|Thêm mới thành công| S[201 Created]
    D -->|Trùng UNIQUE| C[409 Conflict]

    S --> F
    C --> F
    