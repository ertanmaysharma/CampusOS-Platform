from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.workflow_service import get_workflows, get_workflow_by_id
from ..utils.errors import error_response, success_response

workflows_bp = Blueprint("workflows", __name__)


@workflows_bp.route("", methods=["GET"])
@jwt_required()
def list_workflows():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    status = request.args.get("status")

    result = get_workflows(page=page, per_page=per_page, status=status)
    return success_response(result)


@workflows_bp.route("/<int:workflow_id>", methods=["GET"])
@jwt_required()
def get_workflow(workflow_id):
    workflow = get_workflow_by_id(workflow_id)
    if not workflow:
        return error_response("Workflow not found", 404)
    return success_response(workflow.to_dict(include_tasks=True))
