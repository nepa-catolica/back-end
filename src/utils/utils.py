from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify


def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            current_user = get_jwt_identity()
            if isinstance(roles, list):
                if current_user['role'] not in roles:
                    return jsonify({"message": "Access denied"}), 403
            else:
                if current_user['role'] != roles:
                    return jsonify({"message": "Access denied"}), 403
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper
