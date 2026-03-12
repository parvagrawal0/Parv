from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.user_model import User
from utils.jwt_utils import generate_jwt
from utils.supabase_client import insert_user_to_supabase, supabase_is_configured

auth_bp = Blueprint("auth", __name__)


def _validate_register_payload(payload):
    errors = []
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not name:
        errors.append("Name is required.")
    if not email:
        errors.append("Email is required.")
    if not password:
        errors.append("Password is required.")
    elif len(password) < 6:
        errors.append("Password must be at least 6 characters.")

    return errors, name, email, password


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    errors, name, email, password = _validate_register_payload(data)

    if errors:
        return jsonify({"message": "Invalid input", "errors": errors}), 400

    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"message": "Email already registered"}), 400

    password_hash = generate_password_hash(password)
    user = User(name=name, email=email, password=password_hash, role="user")
    db.session.add(user)
    db.session.commit()

    # Also write user to Supabase (public.users)
    if supabase_is_configured():
        try:
            insert_user_to_supabase(
                {
                    "name": user.name,
                    "email": user.email,
                    "password": user.password,
                    "role": user.role,
                }
            )
        except Exception as e:
            # If Supabase sync is configured, keep the two data stores consistent.
            db.session.delete(user)
            db.session.commit()
            msg = str(e)
            if "duplicate key value" in msg or "23505" in msg:
                return jsonify({"message": "Email already registered"}), 400
            return (
                jsonify(
                    {"message": "Failed to create user in Supabase", "details": msg}
                ),
                500,
            )

    return (
        jsonify(
            {
                "message": "User registered successfully",
                "user": user.to_dict(),
            }
        ),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_jwt({"sub": user.id, "role": user.role})

    return (
        jsonify(
            {
                "message": "Login successful",
                "token": token,
                "user": user.to_dict(),
            }
        ),
        200,
    )

