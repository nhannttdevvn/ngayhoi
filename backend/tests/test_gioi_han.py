import os

# Đặt DB_PATH=":memory:" trước khi import main để dùng CSDL tạm, không ảnh hưởng dữ liệu thật
os.environ["DB_PATH"] = ":memory:"

import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


# Fixture tự động chạy trước mỗi hàm test để xóa sạch bảng dang_ky
@pytest.fixture(autouse=True)
def xoa_bang_truoc_moi_test():
    main.db.execute("DELETE FROM dang_ky")
    main.db.commit()


# Hàm phụ trợ đăng ký hàng loạt n sinh viên vào một phiên
def lap_day(ma_phien: str, n: int):
    for i in range(n):
        client.post(
            "/api/dang-ky",
            json={"ma_sv": f"SV{i:03}", "ma_phien": ma_phien},
        )


# --- 5 hàm test tương ứng chính xác các dòng 1–5 trong spec.md ---

# Dòng 1: P01 trống | SV001 đăng ký P01 | 201
def test_dong_1_phien_trong_dang_ky_thanh_cong():
    res = client.post("/api/dang-ky", json={"ma_sv": "SV001", "ma_phien": "P01"})
    assert res.status_code == 201
    assert res.json()["ok"] is True


# Dòng 2: P01 có 29 | SV mới đăng ký P01 | 201
def test_dong_2_phien_co_29_dang_ky_thanh_cong():
    lap_day("P01", 29)
    res = client.post("/api/dang-ky", json={"ma_sv": "SV030", "ma_phien": "P01"})
    assert res.status_code == 201
    assert res.json()["ok"] is True


# Dòng 3: P01 có 30 | SV mới đăng ký P01 | 409 HET_CHO
def test_dong_3_phien_co_30_tu_choi_het_cho():
    lap_day("P01", 30)
    res = client.post("/api/dang-ky", json={"ma_sv": "SV031", "ma_phien": "P01"})
    assert res.status_code == 409
    assert res.json()["detail"] == "HET_CHO"


# Dòng 4: P01 có 30, gồm SV000 | SV000 đăng ký lại P01 | 409 DA_DANG_KY
def test_dong_4_phien_co_30_trung_sv_tu_choi_da_dang_ky():
    lap_day("P01", 30)  # lap_day đã sinh các mã từ SV000 đến SV029
    res = client.post("/api/dang-ky", json={"ma_sv": "SV000", "ma_phien": "P01"})
    assert res.status_code == 409
    assert res.json()["detail"] == "DA_DANG_KY"


# Dòng 5: P01 có 30 | SV031 đăng ký P02 | 201
def test_dong_5_phien_p01_da_day_dang_ky_p02_thanh_cong():
    lap_day("P01", 30)
    res = client.post("/api/dang-ky", json={"ma_sv": "SV031", "ma_phien": "P02"})
    assert res.status_code == 201
    assert res.json()["ok"] is True

