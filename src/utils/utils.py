from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify


def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] != role:
                return jsonify({"message": "Access denied"}), 403
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper
