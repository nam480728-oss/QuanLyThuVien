# Hướng dẫn cài đặt MySQL và quản lý bằng Navicat

Website LibraHub sử dụng **MySQL 8.x** làm database chính. Navicat là ứng dụng desktop dùng để kết nối, xem bảng, chỉnh sửa dữ liệu, chạy SQL và sao lưu database MySQL.

> Navicat chỉ là công cụ quản trị. Dữ liệu thật vẫn được lưu bởi MySQL Server và ứng dụng Flask kết nối MySQL bằng PyMySQL.

## 1. Thông số đã thiết lập trên máy hiện tại

MySQL Community Server 8.4 đã được cấu hình cho dự án với các thông số:

| Thuộc tính | Giá trị |
|---|---|
| Loại database | MySQL Community Server 8.4 |
| Host | `127.0.0.1` |
| Port | `3306` |
| User | `root` |
| Password | `123456` |
| Database | `library_management` |
| Character set | `utf8mb4` |
| Collation | `utf8mb4_unicode_ci` |

MySQL 8.4 của dự án sử dụng cổng mặc định `3306`. MySQL của XAMPP đã được dừng để tránh xung đột.

Để chạy toàn bộ hệ thống:

```powershell
cd D:\DangNam
python run.py
```

Lệnh trên sẽ:

1. Kiểm tra MySQL tại `127.0.0.1:3306`.
2. Tự khởi động MySQL nền nếu chưa chạy.
3. Áp dụng migration còn thiếu.
4. Tạo dữ liệu mẫu nếu database đang trống.
5. Mở website tại http://127.0.0.1:5050.

## 2. Cài MySQL Server trên máy mới

Trên máy hiện tại MySQL 8.4 đã được thiết lập sẵn. Nếu sao chép dự án sang máy Windows khác:

1. Tải **MySQL Community Server 8.x** từ trang chính thức của MySQL.
2. Chạy bộ cài và chọn loại cài đặt **Server only**.
3. Chọn cấu hình **Standalone MySQL Server**.
4. Bật giao thức TCP/IP.
5. Dùng cổng mặc định `3306` và bảo đảm không có MySQL/XAMPP khác đang chiếm cổng này.
6. Chọn phương thức xác thực mật khẩu mạnh mặc định của MySQL 8.
7. Đặt mật khẩu cho tài khoản `root`.
8. Bật tùy chọn chạy MySQL dưới dạng **Windows Service** và tự khởi động cùng Windows.
9. Hoàn tất cấu hình rồi kiểm tra dịch vụ MySQL đang ở trạng thái **Running**.

Sau khi cài, cập nhật host, port, user và password tương ứng trong `.env`.

## 3. Cài đặt Navicat

1. Tải **Navicat for MySQL** hoặc **Navicat Premium** từ trang chính thức của Navicat.
2. Chạy bộ cài và hoàn thành các bước theo hướng dẫn.
3. Kích hoạt bằng giấy phép hợp lệ hoặc sử dụng bản dùng thử.
4. Mở Navicat và chọn **Connection → MySQL**.

Navicat không cần chạy để website hoạt động. Chỉ mở Navicat khi cần quản lý hoặc kiểm tra dữ liệu.

## 4. Tạo kết nối MySQL trong Navicat

Trong cửa sổ **New Connection - MySQL**, nhập:

```text
Connection Name: LibraHub MySQL
Host:            127.0.0.1
Port:            3306
User Name:       root
Password:        123456
```

Sau đó:

1. Đánh dấu **Save password** nếu đây là máy cá nhân.
2. Nhấn **Test Connection**.
3. Khi xuất hiện thông báo kết nối thành công, nhấn **OK**.
4. Mở kết nối `LibraHub MySQL` và chọn database `library_management`.

Nếu MySQL chưa chạy, mở terminal tại dự án và chạy:

```powershell
python run.py
```

Sau đó nhấn **Test Connection** lại trong Navicat.

## 5. Import database bằng Navicat

File database đầy đủ nằm tại:

```text
D:\DangNam\database\library_management.sql
```

File này chứa cấu trúc bảng, index, khóa ngoại, migration hiện tại và dữ liệu mẫu.

Các bước import:

1. Mở kết nối `LibraHub MySQL` trong Navicat.
2. Nhấp chuột phải vào kết nối và chọn **Execute SQL File**.
3. Chọn file `D:\DangNam\database\library_management.sql`.
4. Chọn encoding **65001 (UTF-8)** nếu Navicat yêu cầu.
5. Nhấn **Start**.
6. Sau khi chạy xong, nhấn **Refresh** để thấy database `library_management`.

File SQL đã chứa lệnh tạo database nên không cần tạo database thủ công trước khi import.

## 6. Tạo database bằng migration Flask

Nếu không import file SQL, có thể tạo schema từ migration của dự án:

```powershell
python -m flask --app run.py db upgrade
python seed.py
```

Migration sẽ tạo các bảng sau trong MySQL:

| Bảng | Chức năng |
|---|---|
| `users` | Tài khoản, vai trò và thông tin độc giả |
| `books` | Thông tin sách và số lượng tồn kho |
| `authors` | Danh sách tác giả |
| `book_authors` | Quan hệ nhiều-nhiều giữa sách và tác giả |
| `categories` | Thể loại sách |
| `loans` | Yêu cầu mượn, trả, gia hạn và tiền phạt |
| `alembic_version` | Phiên bản migration hiện tại |

## 7. Cấu hình Flask kết nối MySQL

File `.env` tại thư mục gốc đã được cấu hình:

```env
DATABASE_URL=mysql+pymysql://root:123456@127.0.0.1:3306/library_management?charset=utf8mb4
SECRET_KEY=6b8af9139e044d8797bc5ca62d76c493880a9217793a4ac4adf4ff86123c5521
LOAN_DAYS=14
MAX_RENEWALS=2
FINE_PER_DAY=5000
```

Không đổi cổng trong Navicat mà quên đổi cổng trong `DATABASE_URL`.

## 8. Dữ liệu đăng nhập mẫu

| Vai trò | Email | Mật khẩu |
|---|---|---|
| Quản trị viên | `admin@librahub.vn` | `Admin@123` |
| Thủ thư | `thuthu@librahub.vn` | `Thuthu@123` |
| Độc giả | `docgia@librahub.vn` | `Docgia@123` |

Mật khẩu website được lưu dưới dạng hash, không lưu văn bản thuần trong MySQL.

## 9. Sao lưu database bằng Navicat

1. Chọn database `library_management`.
2. Chọn **Backup → New Backup**.
3. Đặt tên bản sao lưu và nhấn **Start**.

Để xuất thành file SQL:

1. Nhấp chuột phải vào database `library_management`.
2. Chọn **Dump SQL File → Structure and Data**.
3. Chọn vị trí lưu file `.sql`.

## 10. Lỗi thường gặp

### `2003 - Can't connect to MySQL server`

MySQL chưa chạy hoặc dùng sai cổng. Chạy:

```powershell
python run.py
```

Trong Navicat phải dùng cổng `3306`.

### `1045 - Access denied for user 'root'`

Kiểm tra lại:

```text
User: root
Password: 123456
```

### `1049 - Unknown database 'library_management'`

Chạy migration và seed:

```powershell
python -m flask --app run.py db upgrade
python seed.py
```

Hoặc import `database/library_management.sql` bằng Navicat.

### Cổng `3306` đang bị ứng dụng khác sử dụng

Đổi `port` trong `.mysql/my.ini`, đổi cổng tương ứng trong `.env`, sau đó tạo lại kết nối Navicat với cùng cổng mới.

## 11. Lưu ý bảo mật

Mật khẩu `123456` chỉ phù hợp cho demo local. Khi triển khai thật:

1. Đổi mật khẩu MySQL mạnh hơn.
2. Tạo một MySQL user riêng cho ứng dụng thay vì dùng `root`.
3. Không commit file `.env` lên Git.
4. Chỉ cho MySQL lắng nghe trên mạng nội bộ cần thiết.
5. Đổi các mật khẩu tài khoản mẫu sau lần đăng nhập đầu tiên.
