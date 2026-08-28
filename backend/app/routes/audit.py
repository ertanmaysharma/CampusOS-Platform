from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..services.audit_service import get_audit_logs
from ..utils.errors import error_response, success_response
from ..utils.security import role_required

audit_bp = Blueprint("audit", __name__)


@audit_bp.route("", methods=["GET"])
@jwt_required()
@role_required("ADMIN", "DEPARTMENT_MANAGER")
def list_audit_logs():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    user_id = request.args.get("user_id", type=int)
    request_id = request.args.get("request_id", type=int)
    workflow_id = request.args.get("workflow_id", type=int)
    action = request.args.get("action")

    result = get_audit_logs(
        user_id=user_id,
        request_id=request_id,
        workflow_id=workflow_id,
        action=action,
        page=page,
        per_page=per_page,
    )
    return success_response(result)
