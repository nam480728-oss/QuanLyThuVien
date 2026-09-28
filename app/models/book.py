from datetime import datetime

from ..extensions import db
from .author import book_authors


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.String(255))
    books = db.relationship("Book", back_populates="category", lazy="dynamic")


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False, unique=True, index=True)
    title = db.Column(db.String(220), nullable=False, index=True)
    description = db.Column(db.Text)
    publisher = db.Column(db.String(150))
    published_year = db.Column(db.Integer)
    location = db.Column(db.String(50))
    cover_url = db.Column(db.String(500))
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL"), index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship("Category", back_populates="books")
    authors = db.relationship("Author", secondary=book_authors, backref=db.backref("books", lazy="dynamic"))
    loans = db.relationship("Loan", back_populates="book", lazy="dynamic")

    @property
    def author_names(self):
        return ", ".join(author.name for author in self.authors) or "Chưa cập nhật"

    @property
    def is_available(self):
        return self.available_copies > 0
