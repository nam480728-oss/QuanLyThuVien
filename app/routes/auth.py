from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import User
from .helpers import validate_csrf


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _safe_next(target):
    if not target:
        return None
    base = urlparse(request.host_url)
    candidate = urlparse(urljoin(request.host_url, target))
    return target if candidate.scheme in {"http", "https"} and base.netloc == candidate.netloc else None


def _dashboard_url(user):
    if user.role == "admin":
        return url_for("admin.dashboard")
    if user.role == "librarian":
        return url_for("librarian.dashboard")
    return url_for("reader.dashboard")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(_dashboard_url(current_user))
    if request.method == "POST":
        validate_csrf()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = db.session.scalar(select(User).where(User.email == email))
        if not user or not user.check_password(password):
            flash("Email hoặc mật khẩu không chính xác.", "danger")
        elif not user.active:
            flash("Tài khoản đã bị khóa. Vui lòng liên hệ quản trị viên.", "danger")
        else:
            login_user(user, remember=request.form.get("remember") == "on")
            flash(f"Chào mừng {user.full_name} quay lại!", "success")
            return redirect(_safe_next(request.args.get("next")) or _dashboard_url(user))
    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(_dashboard_url(current_user))
    if request.method == "POST":
        validate_csrf()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        errors = []
        if len(full_name) < 2:
            errors.append("Họ tên phải có ít nhất 2 ký tự.")
        if "@" not in email or len(email) > 190:
            errors.append("Email không hợp lệ.")
        if len(password) < 8:
            errors.append("Mật khẩu phải có ít nhất 8 ký tự.")
        if password != confirm:
            errors.append("Mật khẩu xác nhận không khớp.")
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            user = User(full_name=full_name, email=email, role="reader")
            user.phone = request.form.get("phone", "").strip() or None
            user.set_password(password)
            db.session.add(user)
            try:
                db.session.commit()
                login_user(user)
                flash("Đăng ký tài khoản thành công.", "success")
                return redirect(url_for("reader.dashboard"))
            except IntegrityError:
                db.session.rollback()
                flash("Email này đã được sử dụng.", "danger")
    return render_template("auth/register.html")


@auth_bp.post("/logout")
def logout():
    validate_csrf()
    logout_user()
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("public.home"))
