from sqlalchemy import select

from app.extensions import db
from app.models import Book, Loan, User
from app.services.loan_service import approve_loan, mark_fine_paid, renew_loan, request_loan, return_loan


def test_complete_loan_lifecycle(app):
    with app.app_context():
        reader = db.session.scalar(select(User).where(User.role == "reader"))
        staff = db.session.scalar(select(User).where(User.role == "librarian"))
        book = db.session.scalar(select(Book).where(Book.isbn == "TEST-001"))

        loan = request_loan(reader, book)
        assert loan.status == "pending"
        approve_loan(loan, staff)
        assert loan.status == "borrowed"
        assert book.available_copies == 1

        old_due = loan.due_at
        renew_loan(loan)
        assert loan.due_at > old_due
        assert loan.renew_count == 1

        return_loan(loan, staff)
        assert loan.status == "returned"
        assert book.available_copies == 2
        assert db.session.scalar(select(Loan).where(Loan.id == loan.id)) is not None

        loan.fine_amount = 5000
        db.session.commit()
        mark_fine_paid(loan, staff)
        assert loan.fine_paid is True
