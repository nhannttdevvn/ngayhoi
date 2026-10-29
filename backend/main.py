import os
import sqlite3
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Cổng đăng ký Ngày hội việc làm")


# Chỉ cho phép frontend Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_PATH = os.getenv("DB_PATH", "ngayhoi.db")
db = sqlite3.connect(DB_PATH, check_same_thread=False)


class DangKy(BaseModel):
    ma_sv: str
    ma_phien: str


def init_db():
    cursor = db.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dang_ky (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ma_sv TEXT NOT NULL,
            ma_phien TEXT NOT NULL,
            UNIQUE(ma_sv, ma_phien)
        )
        """
    )

    db.commit()


init_db()


@app.get("/")
def root():
    return {"message": "Cổng đăng ký Ngày hội việc làm đang chạy"}


@app.post("/api/dang-ky", status_code=status.HTTP_201_CREATED)
def dang_ky(data: DangKy):
    conn = db if DB_PATH == ":memory:" else sqlite3.connect(DB_PATH, timeout=30.0)
    should_close = (DB_PATH != ":memory:")

    try:
        cursor = conn.cursor()

        # Kiểm tra người dùng đã đăng ký phiên này chưa
        cursor.execute(
            "SELECT 1 FROM dang_ky WHERE ma_sv = ? AND ma_phien = ?",
            (data.ma_sv, data.ma_phien),
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="DA_DANG_KY",
            )

        # Chèn nguyên tử: chỉ INSERT khi số lượng sinh viên trong phiên < 30
        cursor.execute(
            """
            INSERT INTO dang_ky (ma_sv, ma_phien)
            SELECT ?, ?
            WHERE (SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?) < 30
            """,
            (data.ma_sv, data.ma_phien, data.ma_phien),
        )

        conn.commit()

        # Nếu không có dòng nào được chèn, tức là phiên đã đủ 30 chỗ
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=409,
                detail="HET_CHO",
            )

        return {
            "ok": True,
            "ma_sv": data.ma_sv,
            "ma_phien": data.ma_phien,
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="DA_DANG_KY",
        )

    finally:
        if should_close:
            conn.close()


SUC_CHUA = 30


@app.get("/api/con-cho")
def con_cho(ma_phien: str):
    conn = db if DB_PATH == ":memory:" else sqlite3.connect(DB_PATH, timeout=30.0)
    try:
        da_dang_ky = conn.execute(
            "SELECT COUNT(*) FROM dang_ky WHERE ma_phien = ?",
            (ma_phien,),
        ).fetchone()[0]
        return {"con_cho": max(0, SUC_CHUA - da_dang_ky)}
    finally:
        if DB_PATH != ":memory:":
            conn.close()
