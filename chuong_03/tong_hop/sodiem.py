from flask import Flask, url_for, request, abort, redirect, make_response, jsonify
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
    keyword = request.args.get("q", "")
    results = []

    for mssv, student in STUDENTS.items():
        if (
            keyword.lower() in student["name"].lower()
            or keyword.lower() in mssv.lower()
        ):
            results.append((mssv, student))

    body = f"""
    <h1>Tìm kiếm sinh viên</h1>
    <form method="get" action="{escape(url_for('search'))}">
        <input type="text" name="q" value="{escape(keyword)}">
        <button type="submit">Tìm kiếm</button>
    </form>
    <p>
        Tìm thấy {escape(str(len(results)))} kết quả
        cho “{escape(keyword)}”
    </p>
    <ul>
    """

    for mssv, student in results:
        body += f"""
        <li>
            <a href="{escape(url_for('student_detail', mssv=mssv))}">
                {escape(mssv)} - {escape(student['name'])}
            </a>
        </li>
        """

    body += "</ul>"

    return layout("Tìm kiếm", body)
@app.route("/api/students")
def api_student_list():
    selected_class = request.args.get("lop", "")
    min_avg_text = request.args.get("min_avg")
    min_avg = None

    if min_avg_text is not None:
        try:
            min_avg = float(min_avg_text)
        except ValueError:
            abort(400, description="min_avg phải là số.")

    results = []

    for mssv, student in STUDENTS.items():
        if (
            selected_class
            and student["lop"].lower() != selected_class.lower()
        ):
            continue

        summary = student_summary(mssv)

        if min_avg is not None:
            if (
                summary["average"] is None
                or summary["average"] < min_avg
            ):
                continue

        results.append({
            "mssv": mssv,
            "name": summary["name"],
            "lop": summary["lop"],
            "average": summary["average"],
            "rank": summary["rank"],
            "scores": summary["scores"]
        })

    return jsonify(results)
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

    short_url = url_for("student_short", mssv=mssv)
    body += f"""
    <p>
        Link rút gọn:
        <a href="{escape(short_url)}">{escape(short_url)}</a>
    </p>
    <p>
        <a href="{escape(url_for('student_export', mssv=mssv))}">
            Tải bảng điểm (CSV)
        </a>
    </p>
    """

    return layout("Chi tiết sinh viên", body)
@app.route("/sv/<mssv>")
def student_short(mssv):
    return redirect(url_for("student_detail", mssv=mssv), code=301)
@app.route("/students/<mssv>/export")
def student_export(mssv):
    if mssv not in STUDENTS:
        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    content = "hoc_phan,diem\n"

    for course, score in STUDENTS[mssv]["scores"].items():
        content += f"{course},{score}\n"

    response = make_response(content)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        f"attachment; filename=diem_{mssv}.csv"
    )

    return response
@app.route(
    "/api/students/<mssv>/scores/<course>",
    methods=["GET", "PUT", "DELETE"]
)
def api_student_score(mssv, course):
    if mssv not in STUDENTS:
        abort(404, description="Không tìm thấy sinh viên.")

    course = course.upper()
    scores = STUDENTS[mssv]["scores"]

    if request.method == "GET":
        if course not in scores:
            abort(404, description="Chưa có điểm học phần này.")

        return jsonify({
            "mssv": mssv,
            "course": course,
            "score": scores[course]
        })

    if request.method == "PUT":
        try:
            score = float(request.args.get("score", ""))
        except ValueError:
            abort(400, description="Điểm phải là số từ 0 đến 10.")

        if not 0 <= score <= 10:
            abort(400, description="Điểm phải là số từ 0 đến 10.")
        is_new = course not in scores
        scores[course] = score

        response = jsonify({
            "mssv": mssv,
            "course": course,
            "score": score
        })

        if is_new:
            response.status_code = 201
            response.headers["Location"] = url_for(
                "api_student_score",
                mssv=mssv,
                course=course
            )

        return response

    if course not in scores:
        abort(404, description="Chưa có điểm học phần này.")

    del scores[course]
    return "", 204
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def handle_error(error):
    titles = {
        400: "Dữ liệu không hợp lệ",
        404: "Không tìm thấy",
        405: "Phương thức không được hỗ trợ"
    }

    title = titles[error.code]
    response = error.get_response()

    if request.path.startswith("/api/"):
        response.set_data(
            jsonify({
                "error": title,
                "detail": error.description
            }).get_data()
        )
        response.headers["Content-Type"] = "application/json"
    else:
        body = f"""
        <h1>{error.code} - {escape(title)}</h1>
        <p>{escape(error.description)}</p>
        """
        response.set_data(layout(title, body))
        response.headers["Content-Type"] = "text/html; charset=utf-8"

    return response
@app.route("/api/students/<mssv>")
def api_student_detail(mssv):
    if mssv not in STUDENTS:
        abort(404, description="Không tìm thấy sinh viên.")

    summary = student_summary(mssv)

    return jsonify({
        "mssv": mssv,
        "name": summary["name"],
        "lop": summary["lop"],
        "average": summary["average"],
        "rank": summary["rank"],
        "scores": summary["scores"]
    })