from flask import Flask, url_for, request, abort
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
    selected_class = request.args.get("lop", "")
    classes = sorted({student["lop"] for student in STUDENTS.values()})

    body = "<h1>Danh sách sinh viên</h1>"
    body += f'<p><a href="{escape(url_for("student_list"))}">Tất cả</a>'

    for lop in classes:
        body += (
            f' | <a href="{escape(url_for("student_list", lop=lop))}">'
            f'{escape(lop)}</a>'
        )

    body += "</p>"

    rows = ""

    for mssv, student in STUDENTS.items():
        if selected_class and student["lop"].lower() != selected_class.lower():
            continue

        summary = student_summary(mssv)
        avg_text = "—" if summary["average"] is None else str(summary["average"])

        rows += f"""
        <tr>
            <td>
                <a href="{escape(url_for('student_detail', mssv=mssv))}">
                    {escape(mssv)}
                </a>
            </td>
            <td>{escape(summary['name'])}</td>
            <td>{escape(summary['lop'])}</td>
            <td>{escape(avg_text)}</td>
            <td>{escape(summary['rank'])}</td>
        </tr>
        """

    if rows:
        body += f"""
        <table border="1">
            <thead>
                <tr>
                    <th>MSSV</th>
                    <th>Họ tên</th>
                    <th>Lớp</th>
                    <th>Điểm TB</th>
                    <th>Xếp loại</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        """
    else:
        body += "<p>Không có sinh viên phù hợp.</p>"

    return layout("Sinh viên", body)

@app.route("/search")
def search():
    return layout("Tìm kiếm", "<h1>Tìm kiếm sinh viên</h1>")
@app.route("/api/students")
def api_student_list():
    return []
@app.route("/students/<mssv>")
def student_detail(mssv):
    if mssv not in STUDENTS:
        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    summary = student_summary(mssv)
    avg_text = "—" if summary["average"] is None else str(summary["average"])

    body = f"""
    <h1>{escape(summary['name'])}</h1>
    <p>MSSV: {escape(mssv)}</p>
    <p>
        Lớp:
        <a href="{escape(url_for('student_list', lop=summary['lop']))}">
            {escape(summary['lop'])}
        </a>
    </p>
    <p>Điểm TB: {escape(avg_text)}</p>
    <p>Xếp loại: {escape(summary['rank'])}</p>
    <h2>Bảng điểm</h2>
    """

    if summary["scores"]:
        body += """
        <table border="1">
            <tr>
                <th>Học phần</th>
                <th>Điểm</th>
            </tr>
        """

        for course, score in summary["scores"].items():
            body += f"""
            <tr>
                <td>{escape(course)}</td>
                <td>{escape(str(score))}</td>
            </tr>
            """

        body += "</table>"
    else:
        body += "<p>Chưa có điểm.</p>"

    return layout("Chi tiết sinh viên", body)