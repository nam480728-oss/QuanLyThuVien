from datetime import datetime, timedelta

from flask import current_app
from sqlalchemy import select

from ..extensions import db
from ..models import Book, Loan


class LoanError(ValueError):
    pass


def calculate_fine(due_at, returned_at=None):
    if not due_at:
        return 0
    end = returned_at or datetime.utcnow()
    overdue_days = max(0, (end.date() - due_at.date()).days)
    return overdue_days * current_app.config["FINE_PER_DAY"]


def refresh_overdue_loans():
    now = datetime.utcnow()
    loans = db.session.scalars(
        select(Loan).where(Loan.status == "borrowed", Loan.due_at < now)
    ).all()
    for loan in loans:
        loan.status = "overdue"
        loan.fine_amount = calculate_fine(loan.due_at)
    if loans:
        db.session.commit()
    return len(loans)


def request_loan(user, book):
    if not user.active:
        raise LoanError("Tài khoản đang bị khóa.")
    if not book.is_available:
        raise LoanError("Sách hiện đã hết bản có thể mượn.")
    existing = db.session.scalar(
        select(Loan).where(
            Loan.user_id == user.id,
            Loan.book_id == book.id,
            Loan.status.in_(["pending", "borrowed", "overdue"]),
        )
    )
    if existing:
        raise LoanError("Bạn đã có yêu cầu hoặc đang mượn cuốn sách này.")
    loan = Loan(user=user, book=book, status="pending")
    db.session.add(loan)
    db.session.commit()
    return loan


def approve_loan(loan, staff_user):
    if loan.status != "pending":
        raise LoanError("Yêu cầu này đã được xử lý.")
    # Lock the MySQL row to prevent two approvals consuming the same copy.
    book = db.session.scalar(select(Book).where(Book.id == loan.book_id).with_for_update())
    if not book or book.available_copies <= 0:
        raise LoanError("Không còn bản sách sẵn có để duyệt.")
    now = datetime.utcnow()
    book.available_copies -= 1
    loan.status = "borrowed"
    loan.borrowed_at = now
    loan.due_at = now + timedelta(days=current_app.config["LOAN_DAYS"])
    loan.processed_by = staff_user.id
    db.session.commit()
    return loan


def reject_loan(loan, staff_user, notes=None):
    if loan.status != "pending":
        raise LoanError("Chỉ có thể từ chối yêu cầu đang chờ.")
    loan.status = "rejected"
    loan.processed_by = staff_user.id
    loan.notes = notes
    db.session.commit()
    return loan


def return_loan(loan, staff_user):
    if loan.status not in {"borrowed", "overdue"}:
        raise LoanError("Phiếu mượn này không ở trạng thái có thể trả.")
    now = datetime.utcnow()
    book = db.session.scalar(select(Book).where(Book.id == loan.book_id).with_for_update())
    book.available_copies = min(book.total_copies, book.available_copies + 1)
    loan.fine_amount = calculate_fine(loan.due_at, now)
    loan.returned_at = now
    loan.status = "returned"
    loan.processed_by = staff_user.id
    db.session.commit()
    return loan


def renew_loan(loan):
    if loan.status != "borrowed":
        raise LoanError("Chỉ có thể gia hạn phiếu đang mượn và chưa quá hạn.")
    if loan.is_overdue:
        raise LoanError("Sách đã quá hạn, vui lòng trả tại quầy.")
    if loan.renew_count >= current_app.config["MAX_RENEWALS"]:
        raise LoanError("Phiếu mượn đã đạt số lần gia hạn tối đa.")
    loan.due_at += timedelta(days=current_app.config["LOAN_DAYS"])
    loan.renew_count += 1
    db.session.commit()
    return loan


def mark_fine_paid(loan, staff_user):
    if loan.status != "returned" or loan.fine_amount <= 0:
        raise LoanError("Phiếu này không có khoản phạt cần thanh toán.")
    if loan.fine_paid:
        raise LoanError("Khoản phạt đã được thanh toán trước đó.")
    loan.fine_paid = True
    loan.processed_by = staff_user.id
    db.session.commit()
    return loan
