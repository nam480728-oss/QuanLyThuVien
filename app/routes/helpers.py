import secrets
from functools import wraps

from flask import abort, request, session
from flask_login import current_user


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(24)
    return session["csrf_token"]


def validate_csrf():
    supplied = request.form.get("csrf_token", "")
    if not supplied or not secrets.compare_digest(supplied, session.get("csrf_token", "")):
        abort(400, description="CSRF token không hợp lệ.")
