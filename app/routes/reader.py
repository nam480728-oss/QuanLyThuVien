from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, select

from ..extensions import db
from ..models import Book, Loan
from ..services.loan_service import LoanError, refresh_overdue_loans, renew_loan, request_loan
from .helpers import role_required, validate_csrf


reader_bp = Blueprint("reader", __name__, url_prefix="/reader")


@reader_bp.get("/dashboard")
@login_required
@role_required("reader")
def dashboard():
    refresh_overdue_loans()
    active_loans = db.session.scalars(
        select(Loan)
        .where(Loan.user_id == current_user.id, Loan.status.in_(["pending", "borrowed", "overdue"]))
        .order_by(Loan.requested_at.desc())
    ).all()
    unpaid_fine = db.session.scalar(
        select(func.coalesce(func.sum(Loan.fine_amount), 0)).where(
            Loan.user_id == current_user.id, Loan.fine_paid.is_(False)
        )
    )
    stats = {
        "active": sum(loan.status in {"borrowed", "overdue"} for loan in active_loans),
        "pending": sum(loan.status == "pending" for loan in active_loans),
        "fine": unpaid_fine or 0,
    }
    recommendations = db.session.scalars(
        select(Book).where(Book.available_copies > 0).order_by(Book.created_at.desc()).limit(4)
    ).all()
    return render_template("reader/dashboard.html", loans=active_loans, stats=stats, recommendations=recommendations)


@reader_bp.get("/loans")
@login_required
@role_required("reader")
def loans():
    refresh_overdue_loans()
    status = request.args.get("status", "")
    query = select(Loan).where(Loan.user_id == current_user.id).order_by(Loan.requested_at.desc())
    if status:
        query = query.where(Loan.status == status)
    page = request.args.get("page", 1, type=int)
    records = db.paginate(query, page=page, per_page=12, error_out=False)
    return render_template("reader/loans.html", loans=records, selected_status=status)


@reader_bp.post("/borrow/<int:book_id>")
@login_required
@role_required("reader")
def borrow(book_id):
    validate_csrf()
    book = db.get_or_404(Book, book_id)
    try:
        request_loan(current_user, book)
        flash("Đã gửi yêu cầu mượn sách. Thủ thư sẽ sớm duyệt yêu cầu.", "success")
    except LoanError as exc:
        flash(str(exc), "danger")
    return redirect(request.referrer or url_for("public.book_detail", book_id=book.id))


@reader_bp.post("/loans/<int:loan_id>/renew")
@login_required
@role_required("reader")
def renew(loan_id):
    validate_csrf()
    loan = db.get_or_404(Loan, loan_id)
    if loan.user_id != current_user.id:
        return "Forbidden", 403
    try:
        renew_loan(loan)
        flash("Gia hạn thành công.", "success")
    except LoanError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("reader.loans"))


@reader_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("reader")
def profile():
    if request.method == "POST":
        validate_csrf()
        full_name = request.form.get("full_name", "").strip()
        if len(full_name) < 2:
            flash("Họ tên phải có ít nhất 2 ký tự.", "danger")
        else:
            current_user.full_name = full_name
            current_user.phone = request.form.get("phone", "").strip() or None
            current_user.address = request.form.get("address", "").strip() or None
            db.session.commit()
            flash("Đã cập nhật hồ sơ.", "success")
            return redirect(url_for("reader.profile"))
    return render_template("reader/profile.html")
