from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Book, Category, Loan, User
from .helpers import role_required, validate_csrf


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    stats = {
        "users": db.session.scalar(select(func.count(User.id))) or 0,
        "books": db.session.scalar(select(func.count(Book.id))) or 0,
        "loans": db.session.scalar(select(func.count(Loan.id))) or 0,
        "categories": db.session.scalar(select(func.count(Category.id))) or 0,
    }
    roles = db.session.execute(select(User.role, func.count(User.id)).group_by(User.role)).all()
    return render_template("admin/dashboard.html", stats=stats, roles=roles)


@admin_bp.get("/users")
@login_required
@role_required("admin")
def users():
    search = request.args.get("q", "").strip()
    query = select(User).order_by(User.created_at.desc())
    if search:
        keyword = f"%{search}%"
        query = query.where(User.full_name.ilike(keyword) | User.email.ilike(keyword))
    records = db.paginate(query, page=request.args.get("page", 1, type=int), per_page=15, error_out=False)
    return render_template("admin/users.html", users=records, search=search)


@admin_bp.route("/users/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def user_create():
    if request.method == "POST":
        validate_csrf()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "reader")
        if len(full_name) < 2 or "@" not in email or len(password) < 8 or role not in {"reader", "librarian", "admin"}:
            flash("Vui lòng nhập dữ liệu hợp lệ; mật khẩu tối thiểu 8 ký tự.", "danger")
        else:
            user = User(full_name=full_name, email=email, role=role, phone=request.form.get("phone", "").strip() or None)
            user.set_password(password)
            db.session.add(user)
            try:
                db.session.commit()
                flash("Đã tạo người dùng.", "success")
                return redirect(url_for("admin.users"))
            except IntegrityError:
                db.session.rollback()
                flash("Email đã tồn tại.", "danger")
    return render_template("admin/user_form.html", user=None)


@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def user_edit(user_id):
    user = db.get_or_404(User, user_id)
    if request.method == "POST":
        validate_csrf()
        role = request.form.get("role")
        full_name = request.form.get("full_name", "").strip()
        if len(full_name) < 2 or role not in {"reader", "librarian", "admin"}:
            flash("Dữ liệu không hợp lệ.", "danger")
        elif user.id == current_user.id and role != "admin":
            flash("Bạn không thể tự gỡ quyền quản trị của mình.", "danger")
        else:
            user.full_name = full_name
            user.role = role
            user.phone = request.form.get("phone", "").strip() or None
            user.address = request.form.get("address", "").strip() or None
            password = request.form.get("password", "")
            if password:
                if len(password) < 8:
                    flash("Mật khẩu mới phải có ít nhất 8 ký tự.", "danger")
                    return render_template("admin/user_form.html", user=user)
                user.set_password(password)
            db.session.commit()
            flash("Đã cập nhật người dùng.", "success")
            return redirect(url_for("admin.users"))
    return render_template("admin/user_form.html", user=user)


@admin_bp.post("/users/<int:user_id>/toggle")
@login_required
@role_required("admin")
def user_toggle(user_id):
    validate_csrf()
    user = db.get_or_404(User, user_id)
    if user.id == current_user.id:
        flash("Bạn không thể khóa chính tài khoản đang đăng nhập.", "danger")
    else:
        user.active = not user.active
        db.session.commit()
        flash("Đã cập nhật trạng thái tài khoản.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
@role_required("admin")
def categories():
    if request.method == "POST":
        validate_csrf()
        name = request.form.get("name", "").strip()
        if not name:
            flash("Tên thể loại không được để trống.", "danger")
        else:
            db.session.add(Category(name=name, description=request.form.get("description", "").strip() or None))
            try:
                db.session.commit()
                flash("Đã thêm thể loại.", "success")
                return redirect(url_for("admin.categories"))
            except IntegrityError:
                db.session.rollback()
                flash("Thể loại này đã tồn tại.", "danger")
    records = db.session.scalars(select(Category).order_by(Category.name)).all()
    return render_template("admin/categories.html", categories=records)


@admin_bp.post("/categories/<int:category_id>/delete")
@login_required
@role_required("admin")
def category_delete(category_id):
    validate_csrf()
    category = db.get_or_404(Category, category_id)
    if category.books.count():
        flash("Không thể xóa thể loại đang có sách.", "danger")
    else:
        db.session.delete(category)
        db.session.commit()
        flash("Đã xóa thể loại.", "success")
    return redirect(url_for("admin.categories"))


@admin_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def category_edit(category_id):
    category = db.get_or_404(Category, category_id)
    if request.method == "POST":
        validate_csrf()
        name = request.form.get("name", "").strip()
        if not name:
            flash("Tên thể loại không được để trống.", "danger")
        else:
            category.name = name
            category.description = request.form.get("description", "").strip() or None
            try:
                db.session.commit()
                flash("Đã cập nhật thể loại.", "success")
                return redirect(url_for("admin.categories"))
            except IntegrityError:
                db.session.rollback()
                flash("Tên thể loại đã tồn tại.", "danger")
    return render_template("admin/category_form.html", category=category)
