from pathlib import Path

from flask_migrate import upgrade
from sqlalchemy import select

from app.local_mysql import ensure_local_mysql


ensure_local_mysql()

from app import create_app
from app.extensions import db
from app.models import Book


app = create_app()


def prepare_database():
    """Apply migrations and add demo data on a fresh database."""
    with app.app_context():
        upgrade(directory=str(Path(__file__).resolve().parent / "migrations"))
        if db.session.scalar(select(Book.id).limit(1)) is None:
            from seed import seed

            seed()


if __name__ == "__main__":
    prepare_database()
    # The Werkzeug reloader restarts the parent process on Windows. Because
    # this project also owns a local MySQL child process, that restart can
    # interrupt the database connection. Keep one stable process instead.
    app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False)
