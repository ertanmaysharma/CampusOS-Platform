from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.approval_service import (
    get_pending_approvals, get_approval_by_id,
    approve_action, reject_action, request_changes
)
from ..utils.errors import error_response, success_response
from ..utils.security import role_required

approvals_bp = Blueprint("approvals", __name__)


@approvals_bp.route("", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def list_approvals():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    result = get_pending_approvals(page=page, per_page=per_page)
    return success_response(result)


@approvals_bp.route("/<int:approval_id>", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def get_approval(approval_id):
    approval = get_approval_by_id(approval_id)
    if not approval:
        return error_response("Approval not found", 404)
    return success_response(approval.to_dict())


@approvals_bp.route("/<int:approval_id>/approve", methods=["POST"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def approve(approval_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    approval, error = approve_action(approval_id, user_id, data.get("comment"))
    if error:
        return error_response(error, 400)
    return success_response(approval.to_dict(), "Action approved")


@approvals_bp.route("/<int:approval_id>/reject", methods=["POST"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def reject(approval_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    approval, error = reject_action(approval_id, user_id, data.get("comment"))
    if error:
        return error_response(error, 400)
    return success_response(approval.to_dict(), "Action rejected")


@approvals_bp.route("/<int:approval_id>/request-changes", methods=["POST"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def changes(approval_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    if not data.get("comment"):
        return error_response("Comment is required", 422)
    approval, error = request_changes(approval_id, user_id, data["comment"])
    if error:
        return error_response(error, 400)
    return success_response(approval.to_dict(), "Changes requested")
