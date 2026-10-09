# Khung đầu tệp backend/tests/test_gioi_han.py — giữ nguyên thứ tự dòng
import os
os.environ["DB_PATH"] = ":memory:"   # phải đặt TRƯỚC khi import main
import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def so_trong():
    main.db.execute("DELETE FROM dang_ky"); main.db.commit()

def lap_day(ma_phien, n):
    for i in range(n):
        client.post("/api/dang-ky", json={"ma_sv": f"SV{i:03}", "ma_phien": ma_phien})

# Viết 5 test, mỗi test ứng một dòng 1–5 của spec.md
