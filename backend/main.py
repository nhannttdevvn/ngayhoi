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
    try:
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO dang_ky (ma_sv, ma_phien)
            VALUES (?, ?)
            """,
            (data.ma_sv, data.ma_phien),
        )

        db.commit()

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