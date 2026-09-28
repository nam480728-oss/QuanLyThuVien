from sqlalchemy import or_, select

from ..extensions import db
from ..models import Author, Book, Category


def book_query(search=None, category_id=None, availability=None):
    query = select(Book).order_by(Book.created_at.desc())
    if search:
        keyword = f"%{search.strip()}%"
        query = query.outerjoin(Book.authors).where(
            or_(Book.title.ilike(keyword), Book.isbn.ilike(keyword), Author.name.ilike(keyword))
        ).distinct()
    if category_id:
        query = query.where(Book.category_id == category_id)
    if availability == "available":
        query = query.where(Book.available_copies > 0)
    return query


def get_or_create_author(name):
    clean_name = name.strip()
    author = db.session.scalar(select(Author).where(Author.name == clean_name))
    if not author:
        author = Author(name=clean_name)
        db.session.add(author)
    return author


def category_choices():
    return db.session.scalars(select(Category).order_by(Category.name)).all()
