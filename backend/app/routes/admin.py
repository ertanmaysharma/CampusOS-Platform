from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User
from ..models.role import Role
from ..models.department import Department
from ..utils.errors import error_response, success_response
from ..utils.security import role_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/roles", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def list_roles():
    roles = Role.query.all()
    return success_response([r.to_dict() for r in roles])


@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
@role_required("ADMIN")
def admin_stats():
    return success_response({
        "total_users": User.query.count(),
        "active_users": User.query.filter_by(is_active=True).count(),
        "total_roles": Role.query.count(),
        "total_departments": Department.query.count(),
    })
