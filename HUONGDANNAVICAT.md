# HƯỚNG DẪN CÀI DATABASE THƯ VIỆN VÀO NAVICAT

Tài liệu này hướng dẫn từng bước kết nối MySQL và import database `library_management` bằng Navicat trên Windows.

## 1. Thông tin kết nối

Sử dụng đúng các thông số sau:

| Thuộc tính | Giá trị |
|---|---|
| Connection Name | `LibraHub MySQL` |
| Host | `127.0.0.1` |
| Port | `3306` |
| User Name | `root` |
| Password | `123456` |
| Database | `library_management` |

MySQL của dự án sử dụng cổng mặc định `3306`. MySQL của XAMPP đã được dừng để tránh xung đột cổng.

## 2. Khởi động MySQL của dự án

Trước khi mở Navicat, mở PowerShell hoặc Terminal tại thư mục dự án:

```powershell
cd D:\DangNam
python run.py
```

Khi terminal hiển thị địa chỉ sau thì MySQL và website đã sẵn sàng:

```text
http://127.0.0.1:5050
```

Giữ terminal này đang chạy trong lúc kiểm tra website. Sau khi MySQL đã được khởi động, Navicat có thể kết nối tại cổng `3306`.

## 3. Cài đặt Navicat

1. Tải **Navicat for MySQL** hoặc **Navicat Premium** từ trang chính thức của Navicat.
2. Mở file cài đặt.
3. Chọn **Next**.
4. Đồng ý điều khoản sử dụng.
5. Chọn thư mục cài đặt.
6. Chọn **Install**.
7. Sau khi cài xong, chọn **Finish** và mở Navicat.
8. Kích hoạt bằng giấy phép hợp lệ hoặc sử dụng thời gian dùng thử.

Navicat là công cụ quản lý. MySQL Server mới là nơi lưu dữ liệu thật của website.

## 4. Tạo kết nối MySQL trong Navicat

1. Mở Navicat.
2. Trên thanh công cụ, chọn **Connection**.
3. Chọn **MySQL**.
4. Tại tab **General**, nhập:

```text
Connection Name: LibraHub MySQL
Host:            127.0.0.1
Port:            3306
User Name:       root
Password:        123456
```

5. Đánh dấu **Save Password** nếu đây là máy tính cá nhân.
6. Nhấn **Test Connection**.
7. Nếu xuất hiện thông báo **Connection Successful**, nhấn **OK**.
8. Nhấn **OK** lần nữa để lưu kết nối.

Nếu kiểm tra kết nối thất bại, xem phần xử lý lỗi ở cuối tài liệu.

## 5. Import database bằng file SQL

File SQL đã chuẩn bị sẵn tại:

```text
D:\DangNam\database\library_management.sql
```

File này đã chứa:

- Lệnh tạo database `library_management`.
- Cấu trúc toàn bộ bảng.
- Primary key, foreign key và index.
- Phiên bản migration.
- Dữ liệu sách, thể loại và tài khoản mẫu.

Thực hiện import như sau:

1. Trong Navicat, nhấp đúp vào kết nối **LibraHub MySQL** để mở kết nối.
2. Nhấp chuột phải vào tên kết nối **LibraHub MySQL**.
3. Chọn **Execute SQL File**.
4. Tại mục **File**, nhấn nút `...` để chọn file.
5. Chọn:

```text
D:\DangNam\database\library_management.sql
```

6. Nếu Navicat hỏi encoding, chọn **65001 (UTF-8)** hoặc **UTF-8**.
7. Nhấn **Start**.
8. Chờ đến khi cửa sổ kết quả hiển thị quá trình chạy hoàn tất và không có lỗi.
9. Nhấn **Close**.
10. Nhấp chuột phải vào kết nối và chọn **Refresh**.
11. Database `library_management` sẽ xuất hiện trong danh sách.

## 6. Kiểm tra các bảng sau khi import

1. Mở kết nối **LibraHub MySQL**.
2. Mở database `library_management`.
3. Mở mục **Tables**.
4. Kiểm tra các bảng:

```text
alembic_version
authors
book_authors
books
categories
loans
users
```

Nếu có đủ các bảng trên thì cấu trúc database đã được cài thành công.

## 7. Kiểm tra dữ liệu mẫu

### Kiểm tra sách

1. Nhấp đúp vào bảng `books`.
2. Chọn tab **Data**.
3. Bảng phải có các sách mẫu như `Nhà giả kim`, `Clean Code` và `Atomic Habits`.

### Kiểm tra tài khoản

1. Nhấp đúp vào bảng `users`.
2. Chọn tab **Data**.
3. Kiểm tra ba tài khoản mẫu:

| Vai trò | Email | Mật khẩu đăng nhập website |
|---|---|---|
| Quản trị viên | `admin@librahub.vn` | `Admin@123` |
| Thủ thư | `thuthu@librahub.vn` | `Thuthu@123` |
| Độc giả | `docgia@librahub.vn` | `Docgia@123` |

Trong bảng `users`, mật khẩu được lưu dưới dạng hash nên sẽ không hiển thị giống mật khẩu đăng nhập ở trên.

## 8. Kiểm tra bằng câu lệnh SQL trong Navicat

1. Chọn database `library_management`.
2. Chọn **New Query**.
3. Nhập câu lệnh:

```sql
USE library_management;

SHOW TABLES;

SELECT COUNT(*) AS total_books FROM books;
SELECT COUNT(*) AS total_users FROM users;
SELECT id, title, isbn, available_copies, total_copies FROM books;
```

4. Nhấn **Run** hoặc phím `F6`.
5. Kết quả dữ liệu mẫu ban đầu phải có `10` sách và `3` người dùng.

## 9. Chạy website sau khi cài database

Tại terminal trong thư mục dự án, chạy:

```powershell
cd D:\DangNam
python run.py
```

Truy cập:

```text
http://127.0.0.1:5050
```

Ứng dụng đọc và ghi trực tiếp vào database MySQL đang xem trong Navicat. Khi thêm sách hoặc mượn sách trên website, nhấn **Refresh** trong Navicat để xem dữ liệu mới.

## 10. Không muốn import file SQL

Có thể tạo database bằng migration Flask thay cho việc import SQL:

```powershell
cd D:\DangNam
python -m flask --app run.py db upgrade
python seed.py
python run.py
```

Sau đó quay lại Navicat, nhấp chuột phải vào kết nối và chọn **Refresh**.

Chỉ cần chọn một trong hai cách:

- Import `database/library_management.sql` bằng Navicat; hoặc
- Chạy migration và `seed.py` bằng terminal.

Không cần thực hiện cả hai cách trên database đã có dữ liệu.

## 11. Sao lưu database bằng Navicat

1. Chọn database `library_management`.
2. Nhấp chuột phải và chọn **Dump SQL File**.
3. Chọn **Structure and Data**.
4. Chọn vị trí lưu file `.sql`.
5. Nhấn **Start** để xuất bản sao lưu.

Ngoài ra có thể sử dụng chức năng **Backup → New Backup** của Navicat.

## 12. Xử lý lỗi thường gặp

### Lỗi `2003 - Can't connect to MySQL server`

Nguyên nhân thường là MySQL chưa chạy hoặc nhập sai cổng.

1. Chạy lại:

```powershell
cd D:\DangNam
python run.py
```

2. Trong Navicat kiểm tra port phải là `3306`.
3. Host phải là `127.0.0.1`.
4. Nhấn **Test Connection** lại.

### Lỗi `1045 - Access denied for user 'root'`

Kiểm tra chính xác:

```text
User Name: root
Password:  123456
```

Đảm bảo không có khoảng trắng thừa ở đầu hoặc cuối mật khẩu.

### Lỗi `1049 - Unknown database 'library_management'`

Database chưa được tạo. Thực hiện một trong hai cách:

- Import lại file `D:\DangNam\database\library_management.sql`; hoặc
- Chạy `python -m flask --app run.py db upgrade` và `python seed.py`.

### Import báo bảng đã tồn tại

Database đã được cài trước đó. Nếu dữ liệu hiện tại cần được giữ lại thì dừng import.

Nếu chắc chắn muốn cài lại từ đầu:

1. Sao lưu database hiện tại.
2. Nhấp chuột phải vào `library_management`.
3. Chọn **Delete Database**.
4. Xác nhận xóa.
5. Import lại file `library_management.sql`.

Thao tác xóa database sẽ xóa toàn bộ dữ liệu hiện tại và không thể hoàn tác nếu chưa sao lưu.

## 13. Cấu hình đang được Flask sử dụng

Website đọc kết nối từ file `.env`:

```env
DATABASE_URL=mysql+pymysql://root:123456@127.0.0.1:3306/library_management?charset=utf8mb4
```

Thông số trong `.env` và thông số kết nối Navicat phải giống nhau.

## 14. Lưu ý bảo mật

- Mật khẩu `123456` chỉ dùng cho demo local.
- Không đưa file `.env` lên GitHub.
- Khi triển khai thật, tạo user MySQL riêng cho website thay vì sử dụng `root`.
- Đổi mật khẩu của các tài khoản mẫu trước khi sử dụng thật.
- Luôn sao lưu database trước khi xóa bảng hoặc import lại dữ liệu.
