# 3 chức năng nổi bật của website quản lý thư viện

## 1. Duyệt yêu cầu mượn sách và cập nhật tồn kho an toàn

### Mô tả

Độc giả gửi yêu cầu mượn sách, sau đó thủ thư hoặc quản trị viên duyệt yêu cầu. Khi duyệt, hệ thống khóa bản ghi sách trong MySQL bằng `SELECT ... FOR UPDATE`, kiểm tra số lượng còn lại, giảm tồn kho và thiết lập hạn trả.

Cơ chế khóa bản ghi giúp tránh trường hợp hai thủ thư cùng duyệt một bản sách cuối cùng, bảo đảm `available_copies` không bị âm.

### Backend rút gọn

```python
from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy import select

from app.extensions import db
from app.models import Book


def approve_loan(loan, staff_user):
    if loan.status != "pending":
        raise ValueError("Yêu cầu đã được xử lý.")

    book = db.session.scalar(
        select(Book).where(Book.id == loan.book_id).with_for_update()
    )
    if not book or book.available_copies <= 0:
        raise ValueError("Không còn bản sách sẵn có.")

    now = datetime.utcnow()
    book.available_copies -= 1
    loan.status = "borrowed"
    loan.borrowed_at = now
    loan.due_at = now + timedelta(days=current_app.config["LOAN_DAYS"])
    loan.processed_by = staff_user.id
    db.session.commit()
```

Code đầy đủ: `app/services/loan_service.py`.

---

## 2. Trả sách và tự động tính tiền phạt quá hạn

### Mô tả

Khi thủ thư nhận sách trả, hệ thống tự động:

- Kiểm tra phiếu có đang ở trạng thái mượn hoặc quá hạn hay không.
- Tính số ngày quá hạn.
- Tính tiền phạt theo cấu hình `FINE_PER_DAY`.
- Cập nhật ngày trả và trạng thái phiếu.
- Tăng lại số lượng sách có thể mượn.

Toàn bộ thay đổi được commit trong cùng một transaction MySQL để tồn kho và phiếu mượn luôn đồng bộ.

### Backend rút gọn

```python
from datetime import datetime
from flask import current_app
from sqlalchemy import select

from app.extensions import db
from app.models import Book


def calculate_fine(due_at, returned_at):
    overdue_days = max(0, (returned_at.date() - due_at.date()).days)
    return overdue_days * current_app.config["FINE_PER_DAY"]


def return_loan(loan, staff_user):
    if loan.status not in {"borrowed", "overdue"}:
        raise ValueError("Phiếu không thể trả ở trạng thái hiện tại.")

    book = db.session.scalar(
        select(Book).where(Book.id == loan.book_id).with_for_update()
    )
    returned_at = datetime.utcnow()

    book.available_copies = min(book.total_copies, book.available_copies + 1)
    loan.fine_amount = calculate_fine(loan.due_at, returned_at)
    loan.returned_at = returned_at
    loan.status = "returned"
    loan.processed_by = staff_user.id
    db.session.commit()
```

Code đầy đủ: `app/services/loan_service.py`.

---

## 3. Đăng nhập và phân quyền theo vai trò

### Mô tả

Hệ thống có ba vai trò:

- `reader`: tìm kiếm, mượn sách, gia hạn và xem lịch sử.
- `librarian`: quản lý sách và xử lý mượn trả.
- `admin`: quản lý toàn bộ hệ thống, tài khoản và thể loại.

Mật khẩu được kiểm tra bằng password hash của Werkzeug. Decorator `role_required` bảo vệ route backend, nên người dùng không thể truy cập chức năng trái phép chỉ bằng cách nhập URL trực tiếp.

### Backend rút gọn

```python
from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if current_user.role not in allowed_roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator
```

Ví dụ bảo vệ route quản lý sách:

```python
@librarian_bp.get("/books")
@login_required
@role_required("librarian", "admin")
def books():
    records = db.paginate(
        select(Book).order_by(Book.updated_at.desc()),
        per_page=15,
        error_out=False,
    )
    return render_template("librarian/books.html", books=records)
```

Code đầy đủ: `app/routes/auth.py`, `app/routes/helpers.py` và `app/routes/librarian.py`.
