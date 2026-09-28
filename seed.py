"""Create initial MySQL data. Run after `flask db upgrade`."""

from sqlalchemy import select

from app import create_app
from app.extensions import db
from app.models import Author, Book, Category, User


CATEGORIES = [
    ("Văn học", "Tiểu thuyết, truyện ngắn và tác phẩm văn chương"),
    ("Khoa học", "Khoa học tự nhiên và khám phá thế giới"),
    ("Kinh tế", "Quản trị, tài chính và khởi nghiệp"),
    ("Công nghệ", "Lập trình, dữ liệu và chuyển đổi số"),
    ("Kỹ năng", "Phát triển bản thân và kỹ năng sống"),
]

BOOKS = [
    ("9786043497244", "Nhà giả kim", "Paulo Coelho", "Văn học", 1988, "Nhã Nam", 5, "A-01"),
    ("9786049631468", "Rừng Na Uy", "Haruki Murakami", "Văn học", 1987, "Hội Nhà Văn", 4, "A-02"),
    ("9786041077615", "Lược sử thời gian", "Stephen Hawking", "Khoa học", 1988, "Trẻ", 3, "B-01"),
    ("9786041126585", "Vũ trụ trong vỏ hạt dẻ", "Stephen Hawking", "Khoa học", 2001, "Trẻ", 3, "B-02"),
    ("9786045555386", "Tư duy nhanh và chậm", "Daniel Kahneman", "Kinh tế", 2011, "Thế Giới", 6, "C-01"),
    ("9786049858209", "Quốc gia khởi nghiệp", "Dan Senor, Saul Singer", "Kinh tế", 2009, "Thế Giới", 4, "C-02"),
    ("9780132350884", "Clean Code", "Robert C. Martin", "Công nghệ", 2008, "Prentice Hall", 5, "D-01"),
    ("9781492056355", "Fluent Python", "Luciano Ramalho", "Công nghệ", 2022, "O'Reilly", 3, "D-02"),
    ("9786045675251", "Đắc nhân tâm", "Dale Carnegie", "Kỹ năng", 1936, "Tổng hợp TP.HCM", 7, "E-01"),
    ("9786045896106", "Atomic Habits", "James Clear", "Kỹ năng", 2018, "Thế Giới", 6, "E-02"),
]


def upsert_user(email, full_name, role, password):
    user = db.session.scalar(select(User).where(User.email == email))
    if not user:
        user = User(email=email, full_name=full_name, role=role)
        user.active = True
        user.set_password(password)
        db.session.add(user)
    return user


def seed():
    categories = {}
    for name, description in CATEGORIES:
        category = db.session.scalar(select(Category).where(Category.name == name))
        if not category:
            category = Category(name=name, description=description)
            db.session.add(category)
        categories[name] = category
    db.session.flush()

    for isbn, title, authors, category_name, year, publisher, copies, location in BOOKS:
        if db.session.scalar(select(Book).where(Book.isbn == isbn)):
            continue
        author_records = []
        for author_name in authors.split(","):
            author_name = author_name.strip()
            author = db.session.scalar(select(Author).where(Author.name == author_name))
            if not author:
                author = Author(name=author_name)
                db.session.add(author)
            author_records.append(author)
        book = Book(
            isbn=isbn,
            title=title,
            authors=author_records,
            category=categories[category_name],
            published_year=year,
            publisher=publisher,
            total_copies=copies,
            available_copies=copies,
            location=location,
            description=f"Một tựa sách nổi bật thuộc thể loại {category_name.lower()}, được tuyển chọn cho kho sách LibraHub.",
        )
        db.session.add(book)

    upsert_user("admin@librahub.vn", "Quản trị LibraHub", "admin", "Admin@123")
    upsert_user("thuthu@librahub.vn", "Thủ thư LibraHub", "librarian", "Thuthu@123")
    upsert_user("docgia@librahub.vn", "Nguyễn Minh An", "reader", "Docgia@123")
    db.session.commit()
    print("Seed data created successfully.")
    print("Admin: admin@librahub.vn / Admin@123")
    print("Librarian: thuthu@librahub.vn / Thuthu@123")
    print("Reader: docgia@librahub.vn / Docgia@123")


if __name__ == "__main__":
    application = create_app()
    with application.app_context():
        seed()
