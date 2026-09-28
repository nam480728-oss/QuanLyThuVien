from flask import Flask, render_template

from config import Config
from .extensions import db, login_manager, migrate


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "Thiếu DATABASE_URL. Hãy sao chép .env.example thành .env và cấu hình MySQL."
        )

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Vui lòng đăng nhập để tiếp tục."
    login_manager.login_message_category = "warning"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .routes.admin import admin_bp
    from .routes.auth import auth_bp
    from .routes.librarian import librarian_bp
    from .routes.public import public_bp
    from .routes.reader import reader_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(reader_bp)
    app.register_blueprint(librarian_bp)
    app.register_blueprint(admin_bp)

    from .routes.helpers import csrf_token
    app.jinja_env.globals["csrf_token"] = csrf_token

    @app.template_filter("currency")
    def currency(value):
        return f"{int(value or 0):,}".replace(",", ".") + " ₫"

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("error.html", code=403, message="Bạn không có quyền truy cập trang này."), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404, message="Không tìm thấy nội dung bạn yêu cầu."), 404

    @app.errorhandler(500)
    def server_error(_error):
        db.session.rollback()
        return render_template("error.html", code=500, message="Hệ thống gặp sự cố. Vui lòng thử lại."), 500

    return app
