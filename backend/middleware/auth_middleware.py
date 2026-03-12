from functools import wraps

from flask import request, jsonify, g

from models.user_model import User
from utils.jwt_utils import decode_jwt


def jwt_required(optional: bool = False):
    """
    Decorator to protect routes with JWT authentication.
    If optional=True, it will not abort when token is missing/invalid.
    Stores current user on flask.g.current_user when valid.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            token = None
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ", 1)[1].strip()

            if not token:
                if optional:
                    g.current_user = None
                    return fn(*args, **kwargs)
                return (
                    jsonify({"message": "Missing Authorization header"}), 401
                )

            payload = decode_jwt(token)
            if not payload:
                if optional:
                    g.current_user = None
                    return fn(*args, **kwargs)
                return jsonify({"message": "Invalid or expired token"}), 401

            user_id = payload.get("sub")
            if not user_id:
                return jsonify({"message": "Invalid token payload"}), 401
            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                return jsonify({"message": "Invalid token payload"}), 401

            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 401

            g.current_user = user
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def role_required(*roles):
    """
    Decorator that ensures the authenticated user has one of the given roles.
    Must be used after @jwt_required.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if not user:
                return jsonify({"message": "Authentication required"}), 401

            if user.role not in roles:
                return jsonify({"message": "Forbidden"}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator

