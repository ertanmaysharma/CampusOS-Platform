from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User
from ..models.role import Role
from ..utils.errors import error_response, success_response
from ..utils.security import role_required

users_bp = Blueprint("users", __name__)


@users_bp.route("", methods=["GET"])
@jwt_required()
def list_users():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    role_name = request.args.get("role")
    department_id = request.args.get("department_id", type=int)

    query = User.query
    if role_name:
        role = Role.query.filter_by(name=role_name).first()
        if role:
            query = query.filter_by(role_id=role.id)
    if department_id:
        query = query.filter_by(department_id=department_id)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return success_response({
        "items": [u.to_dict() for u in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
    })


@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)
    return success_response(user.to_dict())


@users_bp.route("", methods=["POST"])
@role_required("ADMIN")
def create_user():
    data = request.get_json()
    if not data:
        return error_response("Request body required", 400)

    required = ["name", "email", "password", "role"]
    for field in required:
        if not data.get(field):
            return error_response(f"{field} is required", 422)

    if User.query.filter_by(email=data["email"]).first():
        return error_response("Email already exists", 409)

    role = Role.query.filter_by(name=data["role"]).first()
    if not role:
        return error_response("Invalid role", 422)

    user = User(
        name=data["name"],
        email=data["email"],
        phone=data.get("phone"),
        role_id=role.id,
        department_id=data.get("department_id"),
        is_active=data.get("is_active", True),
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return success_response(user.to_dict(), "User created", 201)


@users_bp.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)

    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)

    # Only admin or self can update
    if current_user.role.name != "ADMIN" and current_user_id != user_id:
        return error_response("Not authorized", 403)

    data = request.get_json()
    updatable = ["name", "phone", "department_id"]
    if current_user.role.name == "ADMIN":
        updatable.extend(["role_id", "is_active"])

    for field in updatable:
        if field in data:
            if field == "role_id":
                role = Role.query.get(data[field])
                if not role:
                    return error_response("Invalid role", 422)
            setattr(user, field, data[field])

    db.session.commit()
    return success_response(user.to_dict(), "User updated")


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@role_required("ADMIN")
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)
    user.is_active = False
    db.session.commit()
    return success_response(None, "User deactivated")
