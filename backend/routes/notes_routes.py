from flask import Blueprint, request, jsonify, current_app, g

from extensions import db
from middleware.auth_middleware import jwt_required, role_required
from models.note_model import Note

notes_bp = Blueprint("notes", __name__)


def _parse_pagination_args():
    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        page = 1
    try:
        page_size = int(request.args.get("page_size", 0))
    except ValueError:
        page_size = 0

    default_size = current_app.config.get("DEFAULT_PAGE_SIZE", 10)
    max_size = current_app.config.get("MAX_PAGE_SIZE", 50)

    if page < 1:
        page = 1
    if page_size <= 0:
        page_size = default_size
    page_size = min(page_size, max_size)

    return page, page_size


@notes_bp.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    note = Note(title=title, content=content, user_id=g.current_user.id)
    db.session.add(note)
    db.session.commit()

    return jsonify({"message": "Note created", "note": note.to_dict()}), 201


@notes_bp.route("/notes", methods=["GET"])
@jwt_required()
def list_notes():
    user = g.current_user
    page, page_size = _parse_pagination_args()
    search = (request.args.get("search") or "").strip()

    query = Note.query
    if user.role != "admin":
        query = query.filter_by(user_id=user.id)

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(Note.title.ilike(like_pattern))

    total = query.count()
    items = (
        query.order_by(Note.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return (
        jsonify(
            {
                "notes": [n.to_dict() for n in items],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                },
            }
        ),
        200,
    )


@notes_bp.route("/notes/<int:note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id: int):
    user = g.current_user
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"message": "Note not found"}), 404

    if user.role != "admin" and note.user_id != user.id:
        return jsonify({"message": "Forbidden"}), 403

    return jsonify(note.to_dict()), 200


@notes_bp.route("/notes/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id: int):
    user = g.current_user
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"message": "Note not found"}), 404

    if user.role != "admin" and note.user_id != user.id:
        return jsonify({"message": "Forbidden"}), 403

    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    note.title = title
    note.content = content
    db.session.commit()

    return jsonify({"message": "Note updated", "note": note.to_dict()}), 200


@notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id: int):
    user = g.current_user
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"message": "Note not found"}), 404

    # Admin can delete any note, normal users only their own
    if user.role != "admin" and note.user_id != user.id:
        return jsonify({"message": "Forbidden"}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted"}), 200

