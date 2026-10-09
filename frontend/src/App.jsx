import { useState } from "react";
import "./App.css";

const STATUS_MESSAGES = {
  idle: "Vui lòng nhập Mã sinh viên và Mã phiên để đăng ký.",
  success: "Đăng ký thành công",
  duplicate: "Bạn đã đăng ký phiên này",
  error: "Dữ liệu không hợp lệ",
};

function App() {
  const [studentId, setStudentId] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [status, setStatus] = useState("idle");

  const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/dang-ky",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ma_sv: studentId,
          ma_phien: sessionId,
        }),
      }
    );

    if (response.status === 201) {
      setStatus("success");
    } else if (response.status === 409) {
      setStatus("duplicate");
    } else if (response.status === 422) {
      setStatus("error");
    } else {
      setStatus("error");
    }
  } catch (error) {
    console.error("Không kết nối được backend:", error);
    setStatus("error");
  }
};

  return (
    <main className="page">
      <section className="card">
        <header className="card-header">
          <span className="badge">Job Fair 2026</span>
          <h1>Đăng ký Ngày hội việc làm</h1>
          <p className="subtitle">
            Nhập thông tin để giữ chỗ tại phiên bạn quan tâm.
          </p>
        </header>

        <form className="form" onSubmit={handleSubmit} noValidate>
          <div className="field">
            <label htmlFor="studentId">Mã sinh viên</label>
            <input
              id="studentId"
              name="studentId"
              type="text"
              placeholder="VD: SV12345"
              autoComplete="off"
              value={studentId}
              onChange={(e) => setStudentId(e.target.value)}
              data-testid="student-id"
            />
          </div>

          <div className="field">
            <label htmlFor="sessionId">Mã phiên</label>
            <input
              id="sessionId"
              name="sessionId"
              type="text"
              placeholder="VD: P01"
              autoComplete="off"
              value={sessionId}
              onChange={(e) => setSessionId(e.target.value)}
              data-testid="session-id"
            />
          </div>

          <button type="submit" className="btn btn-primary" data-testid="submit">
            Đăng ký
          </button>
        </form>

        <div
          className={`status status-${status}`}
          role="status"
          aria-live="polite"
          data-testid="status"
        >
          {STATUS_MESSAGES[status]}
        </div>
      </section>
    </main>
  );
}

export default App;