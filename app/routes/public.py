from flask import Blueprint, render_template, request
from sqlalchemy import func, select

from ..extensions import db
from ..models import Book, Category
from ..services.catalog_service import book_query, category_choices


public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def home():
    featured = db.session.scalars(
        select(Book).order_by(Book.created_at.desc()).limit(6)
    ).all()
    stats = {
        "titles": db.session.scalar(select(func.count(Book.id))) or 0,
        "copies": db.session.scalar(select(func.coalesce(func.sum(Book.total_copies), 0))) or 0,
        "categories": db.session.scalar(select(func.count(Category.id))) or 0,
    }
    return render_template("public/home.html", featured=featured, stats=stats)


@public_bp.get("/catalog")
def catalog():
    search = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)
    availability = request.args.get("availability", "")
    page = request.args.get("page", 1, type=int)
    books = db.paginate(
        book_query(search, category_id, availability),
        page=page,
        per_page=12,
        error_out=False,
    )
    return render_template(
        "public/catalog.html",
        books=books,
        categories=category_choices(),
        search=search,
        selected_category=category_id,
        availability=availability,
    )


@public_bp.get("/books/<int:book_id>")
def book_detail(book_id):
    book = db.get_or_404(Book, book_id)
    related = db.session.scalars(
        select(Book)
        .where(Book.category_id == book.category_id, Book.id != book.id)
        .limit(4)
    ).all()
    return render_template("public/book_detail.html", book=book, related=related)
