from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Book, Category, Loan, User
from ..services.catalog_service import category_choices, get_or_create_author
from ..services.loan_service import (
    LoanError,
    approve_loan,
    mark_fine_paid,
    refresh_overdue_loans,
    reject_loan,
    return_loan,
)
from .helpers import role_required, validate_csrf


librarian_bp = Blueprint("librarian", __name__, url_prefix="/librarian")


@librarian_bp.get("/dashboard")
@login_required
@role_required("librarian", "admin")
def dashboard():
    refresh_overdue_loans()
    stats = {
        "books": db.session.scalar(select(func.count(Book.id))) or 0,
        "readers": db.session.scalar(select(func.count(User.id)).where(User.role == "reader")) or 0,
        "pending": db.session.scalar(select(func.count(Loan.id)).where(Loan.status == "pending")) or 0,
        "overdue": db.session.scalar(select(func.count(Loan.id)).where(Loan.status == "overdue")) or 0,
    }
    recent = db.session.scalars(select(Loan).order_by(Loan.requested_at.desc()).limit(8)).all()
    return render_template("librarian/dashboard.html", stats=stats, recent=recent)


@librarian_bp.get("/books")
@login_required
@role_required("librarian", "admin")
def books():
    search = request.args.get("q", "").strip()
    query = select(Book).order_by(Book.updated_at.desc())
    if search:
        query = query.where(Book.title.ilike(f"%{search}%") | Book.isbn.ilike(f"%{search}%"))
    records = db.paginate(query, page=request.args.get("page", 1, type=int), per_page=15, error_out=False)
    return render_template("librarian/books.html", books=records, search=search)


def _fill_book(book):
    title = request.form.get("title", "").strip()
    isbn = request.form.get("isbn", "").strip()
    total = request.form.get("total_copies", type=int)
    if not title or not isbn or total is None or total < 0:
        raise ValueError("Tên sách, ISBN và số lượng hợp lệ là bắt buộc.")
    borrowed = max(0, (book.total_copies or 0) - (book.available_copies or 0))
    if total < borrowed:
        raise ValueError(f"Không thể giảm dưới {borrowed} bản đang được mượn.")
    book.title = title
    book.isbn = isbn
    book.description = request.form.get("description", "").strip() or None
    book.publisher = request.form.get("publisher", "").strip() or None
    book.published_year = request.form.get("published_year", type=int)
    book.location = request.form.get("location", "").strip() or None
    book.cover_url = request.form.get("cover_url", "").strip() or None
    book.category_id = request.form.get("category_id", type=int)
    book.total_copies = total
    book.available_copies = total - borrowed
    names = [name.strip() for name in request.form.get("authors", "").split(",") if name.strip()]
    book.authors = [get_or_create_author(name) for name in dict.fromkeys(names)]


@librarian_bp.route("/books/new", methods=["GET", "POST"])
@login_required
@role_required("librarian", "admin")
def book_create():
    book = Book(total_copies=1, available_copies=1)
    if request.method == "POST":
        validate_csrf()
        try:
            _fill_book(book)
            db.session.add(book)
            db.session.commit()
            flash("Đã thêm sách mới.", "success")
            return redirect(url_for("librarian.books"))
        except (ValueError, IntegrityError) as exc:
            db.session.rollback()
            message = str(exc) if isinstance(exc, ValueError) else "ISBN đã tồn tại trong hệ thống."
            flash(message, "danger")
    return render_template("librarian/book_form.html", book=book, categories=category_choices(), is_edit=False)


@librarian_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("librarian", "admin")
def book_edit(book_id):
    book = db.get_or_404(Book, book_id)
    if request.method == "POST":
        validate_csrf()
        try:
            _fill_book(book)
            db.session.commit()
            flash("Đã cập nhật sách.", "success")
            return redirect(url_for("librarian.books"))
        except (ValueError, IntegrityError) as exc:
            db.session.rollback()
            message = str(exc) if isinstance(exc, ValueError) else "ISBN đã tồn tại trong hệ thống."
            flash(message, "danger")
    return render_template("librarian/book_form.html", book=book, categories=category_choices(), is_edit=True)


@librarian_bp.post("/books/<int:book_id>/delete")
@login_required
@role_required("librarian", "admin")
def book_delete(book_id):
    validate_csrf()
    book = db.get_or_404(Book, book_id)
    if book.loans.count():
        flash("Không thể xóa sách đã phát sinh lịch sử mượn. Hãy đặt số lượng về 0.", "danger")
    else:
        db.session.delete(book)
        db.session.commit()
        flash("Đã xóa sách.", "success")
    return redirect(url_for("librarian.books"))


@librarian_bp.get("/loans")
@login_required
@role_required("librarian", "admin")
def loans():
    refresh_overdue_loans()
    status = request.args.get("status", "")
    query = select(Loan).order_by(Loan.requested_at.desc())
    if status:
        query = query.where(Loan.status == status)
    records = db.paginate(query, page=request.args.get("page", 1, type=int), per_page=15, error_out=False)
    return render_template("librarian/loans.html", loans=records, selected_status=status)


def _loan_action(loan_id, action):
    validate_csrf()
    loan = db.get_or_404(Loan, loan_id)
    try:
        if action == "approve":
            approve_loan(loan, current_user)
            message = "Đã duyệt phiếu mượn."
        elif action == "reject":
            reject_loan(loan, current_user, request.form.get("notes", "").strip() or None)
            message = "Đã từ chối yêu cầu."
        else:
            return_loan(loan, current_user)
            message = "Đã ghi nhận trả sách."
        flash(message, "success")
    except LoanError as exc:
        db.session.rollback()
        flash(str(exc), "danger")
    return redirect(url_for("librarian.loans"))


@librarian_bp.post("/loans/<int:loan_id>/approve")
@login_required
@role_required("librarian", "admin")
def loan_approve(loan_id):
    return _loan_action(loan_id, "approve")


@librarian_bp.post("/loans/<int:loan_id>/reject")
@login_required
@role_required("librarian", "admin")
def loan_reject(loan_id):
    return _loan_action(loan_id, "reject")


@librarian_bp.post("/loans/<int:loan_id>/return")
@login_required
@role_required("librarian", "admin")
def loan_return(loan_id):
    return _loan_action(loan_id, "return")


@librarian_bp.post("/loans/<int:loan_id>/pay-fine")
@login_required
@role_required("librarian", "admin")
def loan_pay_fine(loan_id):
    validate_csrf()
    loan = db.get_or_404(Loan, loan_id)
    try:
        mark_fine_paid(loan, current_user)
        flash("Đã ghi nhận thanh toán tiền phạt.", "success")
    except LoanError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("librarian.loans"))
