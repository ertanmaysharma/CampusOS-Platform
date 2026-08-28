from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..services.dashboard_service import (
    get_student_dashboard, get_staff_dashboard,
    get_manager_dashboard, get_admin_dashboard
)
from ..utils.errors import error_response, success_response

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/student", methods=["GET"])
@jwt_required()
def student_dashboard():
    user_id = int(get_jwt_identity())
    data = get_student_dashboard(user_id)
    return success_response(data)


@dashboard_bp.route("/staff", methods=["GET"])
@jwt_required()
def staff_dashboard():
    user_id = int(get_jwt_identity())
    data = get_staff_dashboard(user_id)
    return success_response(data)


@dashboard_bp.route("/manager", methods=["GET"])
@jwt_required()
def manager_dashboard():
    user_id = int(get_jwt_identity())
    data = get_manager_dashboard(user_id)
    return success_response(data)


@dashboard_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin_dashboard():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role.name not in ("ADMIN", "DEPARTMENT_MANAGER"):
        return error_response("Not authorized", 403)
    data = get_admin_dashboard()
    return success_response(data)
