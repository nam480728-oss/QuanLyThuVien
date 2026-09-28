from datetime import datetime

from ..extensions import db


class Loan(db.Model):
    __tablename__ = "loans"
    __table_args__ = (
        db.Index("ix_loans_status_due", "status", "due_at"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="RESTRICT"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    borrowed_at = db.Column(db.DateTime)
    due_at = db.Column(db.DateTime)
    returned_at = db.Column(db.DateTime)
    renew_count = db.Column(db.Integer, nullable=False, default=0)
    fine_amount = db.Column(db.Integer, nullable=False, default=0)
    fine_paid = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.String(255))
    processed_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))

    user = db.relationship("User", foreign_keys=[user_id], back_populates="loans")
    processor = db.relationship("User", foreign_keys=[processed_by])
    book = db.relationship("Book", back_populates="loans")

    @property
    def is_overdue(self):
        return self.status in {"borrowed", "overdue"} and self.due_at and self.due_at < datetime.utcnow()
