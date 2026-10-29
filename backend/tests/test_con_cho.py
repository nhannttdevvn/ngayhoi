import os

os.environ["DB_PATH"] = ":memory:"

import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def xoa_bang_truoc_moi_test():
    main.db.execute("DELETE FROM dang_ky")
    main.db.commit()


def test_con_cho_phien_trong_tra_30():
    res = client.get("/api/con-cho", params={"ma_phien": "P01"})
    assert res.status_code == 200
    assert res.json() == {"con_cho": 30}


def test_con_cho_giam_theo_tung_phien():
    client.post("/api/dang-ky", json={"ma_sv": "SV001", "ma_phien": "P01"})
    client.post("/api/dang-ky", json={"ma_sv": "SV002", "ma_phien": "P01"})
    client.post("/api/dang-ky", json={"ma_sv": "SV003", "ma_phien": "P02"})
    res = client.get("/api/con-cho", params={"ma_phien": "P01"})
    assert res.status_code == 200
    assert res.json() == {"con_cho": 28}


def test_con_cho_phien_day_tra_0():
    for i in range(30):
        client.post("/api/dang-ky", json={"ma_sv": f"SV{i:03}", "ma_phien": "P01"})
    res = client.get("/api/con-cho", params={"ma_phien": "P01"})
    assert res.status_code == 200
    assert res.json() == {"con_cho": 0}
