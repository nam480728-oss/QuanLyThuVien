# LibraHub — Website quản lý thư viện Flask + MySQL

Ứng dụng quản lý thư viện theo kiến trúc module: HTML/CSS → Flask/Python → MySQL. Mọi sách, người dùng và giao dịch mượn trả đều được đọc/ghi trực tiếp trong database; không dùng JSON/CSV làm nguồn dữ liệu.

## Chức năng

- Trang công khai: trang chủ, tìm kiếm theo tên/tác giả/ISBN, lọc thể loại và tình trạng, chi tiết sách.
- Độc giả: đăng ký, đăng nhập, hồ sơ, gửi yêu cầu mượn, xem lịch sử, gia hạn và theo dõi quá hạn/tiền phạt.
- Thủ thư: dashboard vận hành, CRUD sách, quản lý tồn kho, duyệt/từ chối yêu cầu, nhận trả và thu tiền phạt.
- Quản trị: dashboard, tạo/sửa/khóa tài khoản, phân quyền, quản lý thể loại.
- Nghiệp vụ: khóa dòng MySQL khi duyệt/nhận trả, tự cập nhật quá hạn, tính phạt theo ngày, giới hạn gia hạn, bảo vệ CSRF và mã hóa mật khẩu.

## Cài đặt local

Hướng dẫn thao tác từng bước trong Navicat nằm tại [HUONGDANNAVICAT.md](HUONGDANNAVICAT.md). Tài liệu cấu hình MySQL tổng quát nằm tại [DATABASE_SETUP.md](DATABASE_SETUP.md). Dự án cũng cung cấp file [database/library_management.sql](database/library_management.sql) để import trực tiếp bằng Navicat.

### Chạy ngay trên máy đã được thiết lập

MySQL 8.4 của dự án chạy trực tiếp trên Windows host tại cổng mặc định `3306`. Lệnh dưới đây tự khởi động MySQL nền, áp dụng migration và mở website:

```powershell
python run.py
```

Mở http://127.0.0.1:5050.

### Thiết lập trên máy khác

Yêu cầu Python 3.10+ và MySQL 8.x.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Tạo database trong MySQL:

```sql
CREATE DATABASE library_management
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Sửa `DATABASE_URL` và `SECRET_KEY` trong `.env`, sau đó áp dụng migration có sẵn:

```powershell
python -m flask --app run.py db upgrade
python seed.py
python run.py
```
Mở http://127.0.0.1:5050.

Tài khoản mẫu sau khi chạy seed:

| Vai trò | Email | Mật khẩu |
|---|---|---|
| Quản trị | `admin@librahub.vn` | `Admin@123` |
| Thủ thư | `thuthu@librahub.vn` | `Thuthu@123` |
| Độc giả | `docgia@librahub.vn` | `Docgia@123` |

Hãy đổi mật khẩu mẫu trước khi dùng ngoài môi trường phát triển.

## Kiểm thử

```powershell
pytest -q
```

Test dùng database SQLite trong bộ nhớ để cô lập và chạy nhanh. Ứng dụng thật vẫn bắt buộc đọc kết nối MySQL từ `DATABASE_URL`.

## Cấu trúc

```text
app/
├── models/        # User, Book, Author, Category, Loan
├── routes/        # public, auth, reader, librarian, admin
├── services/      # nghiệp vụ danh mục và mượn trả
├── templates/     # Jinja2 theo từng vai trò
└── static/css/    # giao diện responsive thuần CSS
config.py          # cấu hình từ .env
run.py             # điểm chạy ứng dụng
seed.py            # dữ liệu khởi tạo MySQL
tests/             # kiểm thử xác thực và vòng đời mượn trả
```

## Prototype giao diện

Các bản thiết kế HTML ban đầu của repository được giữ nguyên trong `src/components/` để tham khảo. Ứng dụng Flask đang chạy sử dụng giao diện Jinja2 trong `app/templates/`.
