from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False
STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0},
    },
    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0},
    },
    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {"PMMNM": 9.5, "CSDL": 9.0},
    },
    "23T1020004": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0},
    },
    "23T1020005": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {},
    },
    "23T1020006": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {"PMMNM": 7.5, "MMT": 8.0},
    },
}
def average(scores):
    if not scores:
        return None

    total = sum(scores.values())
    count = len(scores)
    return round(total / count, 2)
def rank(avg):
    if avg is None:
        return "Chưa có điểm"
    elif avg >= 8.5:
        return "Giỏi"
    elif avg >= 7.0:
        return "Khá"
    elif avg >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"
def student_summary(mssv):
    student = STUDENTS[mssv]
    avg = average(student["scores"])

    return {
        "mssv": mssv,
        "name": student["name"],
        "lop": student["lop"],
        "scores": student["scores"],
        "average": avg,
        "rank": rank(avg),
    }
def layout(title, body):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <title>{escape(title)} - Sổ điểm</title>
</head>
<body>
    <nav>
        <a href="{escape(url_for('home'))}">Trang chủ</a> ·
        <a href="{escape(url_for('student_list'))}">Sinh viên</a> ·
        <a href="{escape(url_for('search'))}">Tìm kiếm</a>
    </nav>
    <hr>
    {body}
</body>
</html>"""
@app.route("/")
def home():
    total_students = len(STUDENTS)
    classes = set()

    for student in STUDENTS.values():
        classes.add(student["lop"])

    total_classes = len(classes)

    body = f"""
    <h1>Sổ điểm lớp học</h1>
    <p>Tổng số sinh viên: {escape(str(total_students))}</p>
    <p>Số lớp: {escape(str(total_classes))}</p>
    <p>
        <a href="{escape(url_for('student_list'))}">
            Xem danh sách sinh viên
        </a>
    </p>
    <p>
        <a href="{escape(url_for('api_student_list'))}">
            Xem API sinh viên
        </a>
    </p>
    """

    return layout("Trang chủ", body)

@app.route("/students")
def student_list():
    return layout("Sinh viên", "<h1>Danh sách sinh viên</h1>")


@app.route("/search")
def search():
    return layout("Tìm kiếm", "<h1>Tìm kiếm sinh viên</h1>")
@app.route("/api/students")
def api_student_list():
    return []