# Sổ điểm lớp học – Bài tập tổng hợp chương 3

## 1. Chạy ứng dụng

Chạy tại thư mục `chuong_03/tong_hop` trên Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app sodiem run --debug --port 8000
```

Mở http://127.0.0.1:8000. Giữ server chạy và dùng terminal thứ hai để kiểm thử.

## 2. Danh sách route

Lệnh đã chạy:

```powershell
.\.venv\Scripts\python.exe -m flask --app sodiem routes
```

Kết quả có 10 route, tính cả static:

```text
Endpoint            Methods           Rule
------------------  ----------------  ------------------------------------
api_student_detail  GET               /api/students/<mssv>
api_student_list    GET               /api/students
api_student_score   DELETE, GET, PUT  /api/students/<mssv>/scores/<course>
home                GET               /
search              GET               /search
static              GET               /static/<path:filename>
student_detail      GET               /students/<mssv>
student_export      GET               /students/<mssv>/export
student_list        GET               /students
student_short       GET               /sv/<mssv>
```

## 3. Kết quả kiểm thử curl

Các kết quả dưới đây được ghi từ các lần chạy thực tế. Lệnh PUT dùng tham số query `score`. Kiểm tra DELETE và GET sau xóa đã chạy với học phần TEST; kiểm tra POST đã chạy với TEST và PMMNM.

### Link rút gọn

```powershell
curl.exe -i http://127.0.0.1:8000/sv/23T1020001
```

```text
HTTP/1.1 301 MOVED PERMANENTLY
Location: /students/23T1020001
```

### Tải CSV

```powershell
curl.exe -i http://127.0.0.1:8000/students/23T1020001/export
```

```text
HTTP/1.1 200 OK
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename=diem_23T1020001.csv

hoc_phan,diem
PMMNM,8.5
CSDL,7.0
MMT,9.0
```

### Lọc đồng thời lớp và điểm trung bình

```powershell
curl.exe -i "http://127.0.0.1:8000/api/students?lop=k47a&min_avg=7"
```

Trả `HTTP/1.1 200 OK`, `Content-Type: application/json`:

```json
[
  {
    "average": 8.17,
    "lop": "K47A",
    "mssv": "23T1020001",
    "name": "Nguyễn Văn An",
    "rank": "Khá",
    "scores": {"CSDL": 7.0, "MMT": 9.0, "PMMNM": 8.5}
  }
]
```

### Tham số min_avg sai

```powershell
curl.exe -i "http://127.0.0.1:8000/api/students?min_avg=abc"
```

Trả `HTTP/1.1 400 BAD REQUEST`, `Content-Type: application/json`:

```json
{"detail": "min_avg phải là số.", "error": "Dữ liệu không hợp lệ"}
```

### Sinh viên không tồn tại

```powershell
curl.exe -i http://127.0.0.1:8000/api/students/999
```

Trả `HTTP/1.1 404 NOT FOUND`, `Content-Type: application/json`:

```json
{"detail": "Không tìm thấy sinh viên.", "error": "Không tìm thấy"}
```

### Thêm điểm WEB cho Hoàng Thu Hà

```powershell
curl.exe -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/web?score=9"
```

```text
HTTP/1.1 201 CREATED
Content-Type: application/json
Location: /api/students/23T1020005/scores/WEB
```

```json
{"course": "WEB", "mssv": "23T1020005", "score": 9.0}
```

### Sửa điểm WEB

```powershell
curl.exe -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB?score=7.5"
```

Trả `HTTP/1.1 200 OK`, `Content-Type: application/json`:

```json
{"course": "WEB", "mssv": "23T1020005", "score": 7.5}
```

### Điểm ngoài khoảng 0–10

```powershell
curl.exe -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB?score=11"
```

Trả `HTTP/1.1 400 BAD REQUEST`, `Content-Type: application/json`:

```json
{"detail": "Điểm phải là số từ 0 đến 10.", "error": "Dữ liệu không hợp lệ"}
```

### Xóa điểm và xem lại điểm đã xóa

Trước đó học phần TEST của sinh viên 23T1020001 đã được thêm để kiểm thử.

```powershell
curl.exe -i -X DELETE http://127.0.0.1:8000/api/students/23T1020001/scores/test
curl.exe -i http://127.0.0.1:8000/api/students/23T1020001/scores/test
```

DELETE trả `HTTP/1.1 204 NO CONTENT`, body rỗng.
GET sau xóa trả `HTTP/1.1 404 NOT FOUND`, mô tả “Chưa có điểm học phần này.”.
Lần chạy này thực hiện trước khi thêm hàm xử lý lỗi chung nên body 404 khi đó là HTML mặc định.

### POST tới API

```powershell
curl.exe -i -X POST http://127.0.0.1:8000/api/students/23T1020001/scores/PMMNM
```

```text
HTTP/1.1 405 METHOD NOT ALLOWED
Content-Type: application/json
Allow: DELETE, HEAD, PUT, GET, OPTIONS
```

```json
{
  "detail": "The method is not allowed for the requested URL.",
  "error": "Phương thức không được hỗ trợ"
}
```

### POST tới trang HTML

```powershell
curl.exe -i -X POST http://127.0.0.1:8000/students
```

```text
HTTP/1.1 405 METHOD NOT ALLOWED
Content-Type: text/html; charset=utf-8
Allow: GET, HEAD, OPTIONS
```

Body dùng layout chung, có thanh điều hướng, tiêu đề “405 - Phương thức không được hỗ trợ” và mô tả “The method is not allowed for the requested URL.”.

## 4. Giải thích mã HTTP

Route link rút gọn dùng 301 vì URL rút gọn chuyển hướng vĩnh viễn tới URL chi tiết sinh viên. Header Location cho biết địa chỉ đích.

PUT thêm học phần chưa có dùng 201 vì tạo mới tài nguyên điểm. Header Location trỏ tới URL của tài nguyên vừa tạo. PUT sửa điểm đã tồn tại trả 200.

DELETE thành công trả 204 vì đã xóa và không trả nội dung.

## 5. Dữ liệu sau khi khởi động lại

Đã thêm WEB cho sinh viên 23T1020005, sửa thành 7.5, sau đó dừng và chạy lại server.

```powershell
curl.exe -i http://127.0.0.1:8000/api/students/23T1020005/scores/WEB
```

Trả `HTTP/1.1 404 NOT FOUND`, `Content-Type: application/json`:

```json
{"detail": "Chưa có điểm học phần này.", "error": "Không tìm thấy"}
```

Điểm WEB không còn vì STUDENTS chỉ nằm trong bộ nhớ của tiến trình. Khi server khởi động lại, chương trình nạp dữ liệu ban đầu; thay đổi chưa được lưu vào file hoặc cơ sở dữ liệu.

## 6. Request trong hàm xử lý lỗi

Hàm xử lý lỗi được Flask gọi trong lúc xử lý yêu cầu. Ngữ cảnh yêu cầu vẫn còn, nên hàm đọc được request.path để chọn JSON cho /api/ và HTML cho các đường dẫn khác.

## 7. Git và các file nộp

Lệnh kiểm tra:

```powershell
git log --oneline
git ls-files
```

Trước khi thêm README đã có ít nhất 11 commit hiển thị. git ls-files chỉ gồm .gitignore, requirements.txt và sodiem.py; không theo dõi .venv/.

Các file nộp sau khi thêm README: sodiem.py, requirements.txt, .gitignore, README.md. Giữ lịch sử Git để đối chiếu các commit.

